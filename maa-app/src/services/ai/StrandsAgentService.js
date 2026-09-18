/**
 * StrandsAgentService.js
 * 
 * React Native service layer for the AWS Strands Agents SDK backend.
 * Replaces the direct Gemini/Sarvam/Groq calls for conversational chat.
 * 
 * Architecture:
 *   AIChatbotScreen.js
 *     → StrandsAgentService (this file)
 *       → FastAPI backend (janani_agent_server)
 *         → AWS Strands Agent + Amazon Bedrock (Claude Sonnet 3.5 v2)
 * 
 * NOTE: Voice transcription (STT) still happens at the app layer via
 *       GeminiService.transcribeAudio() BEFORE calling this service.
 *       Only the chat/reasoning step is replaced.
 */

import { generateMultimodalPregnancyChatResponse as _transcribeAndChat } from './GeminiService';

// ── Configuration ──────────────────────────────────────────────────────────────
// Set EXPO_PUBLIC_STRANDS_AGENT_URL in maa-app/.env
// Example: EXPO_PUBLIC_STRANDS_AGENT_URL=http://192.168.1.10:8000
const STRANDS_BASE_URL = process.env.EXPO_PUBLIC_STRANDS_AGENT_URL || '';

const TIMEOUT_MS = 30000; // 30 second timeout

// ── Health check ───────────────────────────────────────────────────────────────
/**
 * Verify the Strands Agent backend is reachable.
 * @returns {Promise<boolean>}
 */
export async function isStrandsBackendAvailable() {
    if (!STRANDS_BASE_URL) return false;
    try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 5000);
        const response = await fetch(`${STRANDS_BASE_URL}/health`, {
            method: 'GET',
            signal: controller.signal,
        });
        clearTimeout(timer);
        return response.ok;
    } catch {
        return false;
    }
}

// ── Core chat call ─────────────────────────────────────────────────────────────
/**
 * Send a message to the Strands Agent backend and get a response.
 * 
 * @param {string} message - The (transcribed) user message text
 * @param {Array<{role: string, text: string}>} history - Chat history
 * @param {string} language - Language code: 'hi', 'en', 'bilingual', etc.
 * @param {string} [sessionId] - Session ID for conversation continuity
 * @param {string} [userId] - Patient user ID for personalized responses
 * @returns {Promise<string>} The agent's response text
 */
export async function callStrandsAgent(
    message,
    history = [],
    language = 'hi',
    sessionId = 'default',
    userId = null,
) {
    if (!STRANDS_BASE_URL) {
        throw new Error(
            'Strands Agent URL not configured. ' +
            'Set EXPO_PUBLIC_STRANDS_AGENT_URL in maa-app/.env. ' +
            'Example: EXPO_PUBLIC_STRANDS_AGENT_URL=http://192.168.1.10:8000'
        );
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

    try {
        const payload = {
            message,
            history: history.map(msg => ({ role: msg.role, text: msg.text })),
            language,
            session_id: sessionId,
            user_id: userId,
        };

        console.log(`[StrandsAgent] Sending to ${STRANDS_BASE_URL}/chat`, {
            message: message.substring(0, 50) + '...',
            language,
            session_id: sessionId,
        });

        const response = await fetch(`${STRANDS_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            signal: controller.signal,
        });

        clearTimeout(timer);

        if (!response.ok) {
            const errBody = await response.text();
            throw new Error(`Strands Agent HTTP ${response.status}: ${errBody}`);
        }

        const data = await response.json();
        console.log('[StrandsAgent] Response received successfully.');
        return data.response || '';

    } catch (err) {
        clearTimeout(timer);
        if (err.name === 'AbortError') {
            throw new Error('Strands Agent request timed out (30s). Check if the backend server is running.');
        }
        throw err;
    }
}

// ── Multimodal: Voice → Transcribe → Strands Agent ────────────────────────────
/**
 * Full pipeline: transcribe voice audio, then send to Strands Agent.
 * 
 * Transcription still uses the existing Sarvam/Gemini/Groq chain.
 * Only the chat response generation is replaced with Strands Agent.
 * 
 * @param {Array<{role: string, text: string}>} messages - Chat history
 * @param {string} base64Audio - Base64 encoded audio data
 * @param {string} langCode - Language code ('hi', 'en', etc.)
 * @param {string} [userId] - Patient user ID
 * @returns {Promise<{transcript: string, response: string}>}
 */
export async function generateMultimodalChatWithStrands(
    messages,
    base64Audio,
    langCode = 'hi',
    userId = null,
) {
    // Step 1: Transcribe voice to text using the existing service chain
    // (Sarvam STT → Gemini STT → Groq Whisper)
    console.log('[StrandsAgent] Step 1: Transcribing audio...');
    
    let transcript;
    try {
        // Import only transcribeAudio to avoid circular dependency
        const { transcribeAudio } = require('./GeminiService');
        transcript = await transcribeAudio(base64Audio, langCode);
    } catch (sttError) {
        console.error('[StrandsAgent] Transcription failed:', sttError);
        throw sttError;
    }

    if (!transcript || transcript === 'NO_SPEECH') {
        return { transcript: 'NO_SPEECH', response: '' };
    }

    console.log('[StrandsAgent] Transcript:', transcript);

    // Step 2: Send transcribed text to Strands Agent
    console.log('[StrandsAgent] Step 2: Calling Strands Agent backend...');
    
    // Generate a stable session ID from user ID or use default
    const sessionId = userId ? `janani_${userId}` : 'janani_default';

    let response;
    try {
        response = await callStrandsAgent(
            transcript,
            messages,
            langCode,
            sessionId,
            userId,
        );
    } catch (agentError) {
        console.warn('[StrandsAgent] Backend failed, falling back to Gemini:', agentError.message);
        // Fallback: use the original Gemini-based pipeline
        const fallbackResult = await _transcribeAndChat(messages, base64Audio, langCode);
        return fallbackResult;
    }

    return { transcript, response };
}

// ── Clear session ──────────────────────────────────────────────────────────────
/**
 * Clear conversation history on the backend for a session.
 * Call this when the user starts a new conversation.
 * 
 * @param {string} sessionId
 */
export async function clearStrandsSession(sessionId = 'janani_default') {
    if (!STRANDS_BASE_URL) return;
    try {
        await fetch(`${STRANDS_BASE_URL}/session/${sessionId}`, { method: 'DELETE' });
        console.log('[StrandsAgent] Session cleared:', sessionId);
    } catch (err) {
        console.warn('[StrandsAgent] Could not clear session:', err.message);
    }
}
