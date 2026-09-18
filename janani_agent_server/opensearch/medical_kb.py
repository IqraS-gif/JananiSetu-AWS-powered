"""
janani_agent_server/opensearch/medical_kb.py

Curated bilingual pregnancy medical Q&A knowledge base.
These documents are indexed into OpenSearch for RAG-based answers.
Covers: danger signs, trimester guidance, symptoms, vaccines, postpartum.
"""

MEDICAL_DOCUMENTS = [
    # ── DANGER SIGNS ──────────────────────────────────────────────────────────
    {
        "doc_id": "med_001",
        "category": "danger_signs",
        "question_en": "What are the danger signs in pregnancy that need immediate attention?",
        "answer_en": (
            "Seek emergency care immediately for any of these: "
            "1. Heavy vaginal bleeding. "
            "2. Severe headache that does not go away. "
            "3. Blurred or disturbed vision. "
            "4. Fits or convulsions. "
            "5. High fever (above 38.5C). "
            "6. Severe abdominal pain. "
            "7. Baby not moving or reduced movements after 28 weeks. "
            "8. Sudden severe swelling of face, hands or feet. "
            "9. Difficulty breathing. "
            "10. Foul-smelling vaginal discharge. "
            "Do NOT wait — go to the nearest hospital or call your ASHA worker immediately."
        ),
        "question_hi": "गर्भावस्था में कौन से खतरे के संकेत हैं जिन पर तुरंत ध्यान देना चाहिए?",
        "answer_hi": (
            "इन लक्षणों में से कोई भी हो तो तुरंत डॉक्टर के पास जाएं: "
            "1. योनि से भारी रक्तस्राव। "
            "2. तेज सिरदर्द जो ठीक न हो। "
            "3. धुंधला दिखना या आंखों में कोई बदलाव। "
            "4. दौरा पड़ना। "
            "5. तेज बुखार (38.5°C से ऊपर)। "
            "6. पेट में तेज दर्द। "
            "7. 28 हफ्तों के बाद बच्चे का हिलना-डुलना कम होना। "
            "8. चेहरे, हाथ या पैरों में अचानक सूजन। "
            "9. सांस लेने में कठिनाई। "
            "10. योनि से बदबूदार स्राव। "
            "देर न करें — तुरंत नजदीकी अस्पताल जाएं या अपनी आशा कार्यकर्ता को बुलाएं।"
        ),
        "trimester": 0,
        "is_emergency": True,
        "text": "danger signs pregnancy emergency bleeding headache vision fits fever pain baby movement swelling preeclampsia",
    },
    {
        "doc_id": "med_002",
        "category": "danger_signs",
        "question_en": "What is preeclampsia and how do I know if I have it?",
        "answer_en": (
            "Preeclampsia is high blood pressure in pregnancy that can be dangerous. "
            "Warning signs: BP above 140/90, severe headache, swelling of face and hands, "
            "blurred vision, upper right stomach pain, sudden weight gain. "
            "It usually appears after 20 weeks. If you have BP above 140/90 with any of these symptoms "
            "go to hospital immediately. It can harm both you and your baby if untreated."
        ),
        "question_hi": "प्रीक्लेम्पसिया क्या है और मुझे कैसे पता चलेगा कि मुझे यह है?",
        "answer_hi": (
            "प्रीक्लेम्पसिया गर्भावस्था में उच्च रक्तचाप है जो खतरनाक हो सकता है। "
            "संकेत: बीपी 140/90 से ऊपर, तेज सिरदर्द, चेहरे और हाथों में सूजन, "
            "धुंधला दिखना, पेट के ऊपरी दाहिने हिस्से में दर्द, अचानक वजन बढ़ना। "
            "यह आमतौर पर 20 सप्ताह के बाद होता है। यदि बीपी 140/90 से ऊपर हो और "
            "ये लक्षण हों तो तुरंत अस्पताल जाएं।"
        ),
        "trimester": 3,
        "is_emergency": True,
        "text": "preeclampsia high blood pressure headache swelling vision pregnancy 140/90",
    },

    # ── TRIMESTER 1 ───────────────────────────────────────────────────────────
    {
        "doc_id": "med_010",
        "category": "trimester_1",
        "question_en": "What should I do in the first trimester (weeks 1-12)?",
        "answer_en": (
            "First trimester key steps: "
            "1. Confirm pregnancy and register at your nearest PHC or hospital. "
            "2. Start folic acid (400mcg/day) immediately — prevents neural tube defects. "
            "3. Get your first antenatal checkup (blood test, urine test, blood group). "
            "4. Avoid alcohol, smoking, and self-medication. "
            "5. Eat iron-rich foods: leafy greens, dal, jaggery. "
            "6. Rest well — fatigue and nausea are normal in first trimester. "
            "7. Register for PMMVY scheme at Anganwadi to get Rs.6,000 benefit."
        ),
        "question_hi": "पहली तिमाही (1-12 सप्ताह) में क्या करना चाहिए?",
        "answer_hi": (
            "पहली तिमाही में जरूरी कदम: "
            "1. गर्भावस्था की पुष्टि करें और नजदीकी PHC या अस्पताल में रजिस्टर करें। "
            "2. तुरंत फोलिक एसिड (400mcg/दिन) लेना शुरू करें। "
            "3. पहली एंटेनेटल जांच करवाएं (खून, पेशाब, ब्लड ग्रुप टेस्ट)। "
            "4. शराब, धूम्रपान और बिना डॉक्टर की सलाह के दवाएं न लें। "
            "5. आयरन से भरपूर खाना खाएं: हरी पत्तेदार सब्जियां, दाल, गुड़। "
            "6. थकान और जी मिचलाना पहली तिमाही में सामान्य है — आराम करें। "
            "7. आंगनवाड़ी में PMMVY योजना में रजिस्ट्रेशन करें।"
        ),
        "trimester": 1,
        "is_emergency": False,
        "text": "first trimester weeks 1-12 folic acid antenatal checkup registration PMMVY nausea fatigue",
    },

    # ── TRIMESTER 2 ───────────────────────────────────────────────────────────
    {
        "doc_id": "med_020",
        "category": "trimester_2",
        "question_en": "What happens in the second trimester (weeks 13-26)?",
        "answer_en": (
            "Second trimester is usually the most comfortable. Key things: "
            "1. Anomaly scan (Level 2 ultrasound) at 18-20 weeks to check baby's development. "
            "2. Take iron and folic acid tablets daily. "
            "3. Tetanus toxoid (TT) injection — get both doses. "
            "4. Eat protein-rich foods: eggs, milk, dal, paneer. "
            "5. Walk 20-30 minutes daily — safe and beneficial. "
            "6. You may feel baby movements (quickening) around 18-20 weeks. "
            "7. Monitor blood pressure and report any headache or swelling."
        ),
        "question_hi": "दूसरी तिमाही (13-26 सप्ताह) में क्या होता है?",
        "answer_hi": (
            "दूसरी तिमाही आमतौर पर सबसे आरामदायक होती है। "
            "1. 18-20 सप्ताह में एनोमली स्कैन (Level 2 अल्ट्रासाउंड) करवाएं। "
            "2. रोज आयरन और फोलिक एसिड की गोलियां लें। "
            "3. टेटनस का टीका (TT) लगवाएं — दोनों डोज जरूरी हैं। "
            "4. प्रोटीन से भरपूर खाना: अंडे, दूध, दाल, पनीर। "
            "5. रोज 20-30 मिनट पैदल चलें। "
            "6. 18-20 सप्ताह के आसपास बच्चे की हलचल महसूस होने लगती है। "
            "7. बीपी पर नजर रखें।"
        ),
        "trimester": 2,
        "is_emergency": False,
        "text": "second trimester weeks 13-26 anomaly scan ultrasound TT injection iron protein baby movements",
    },

    # ── TRIMESTER 3 ───────────────────────────────────────────────────────────
    {
        "doc_id": "med_030",
        "category": "trimester_3",
        "question_en": "What should I know in the third trimester (weeks 27-40)?",
        "answer_en": (
            "Third trimester — preparing for delivery: "
            "1. Visit doctor every 2 weeks after 28 weeks, every week after 36 weeks. "
            "2. Count baby kicks daily — at least 10 movements in 2 hours. "
            "3. Know your hospital's location and have a delivery plan ready. "
            "4. Pack your hospital bag by 36 weeks. "
            "5. Watch for preeclampsia signs: headache, swelling, blurred vision. "
            "6. Rest on your left side — improves blood flow to baby. "
            "7. Continue iron, calcium tablets. "
            "8. Do NOT travel long distances after 36 weeks."
        ),
        "question_hi": "तीसरी तिमाही (27-40 सप्ताह) में क्या जानना जरूरी है?",
        "answer_hi": (
            "तीसरी तिमाही — प्रसव की तैयारी: "
            "1. 28 सप्ताह के बाद हर 2 हफ्ते, 36 सप्ताह के बाद हर हफ्ते डॉक्टर से मिलें। "
            "2. रोज बच्चे की हलचल गिनें — 2 घंटे में कम से कम 10 हलचल। "
            "3. अस्पताल का रास्ता जानें और डिलीवरी की तैयारी करें। "
            "4. 36 सप्ताह तक अस्पताल बैग तैयार रखें। "
            "5. प्रीक्लेम्पसिया के संकेत देखें: सिरदर्द, सूजन, धुंधला दिखना। "
            "6. बायीं करवट लेकर आराम करें। "
            "7. आयरन और कैल्शियम की गोलियां लेते रहें। "
            "8. 36 सप्ताह के बाद लंबी यात्रा न करें।"
        ),
        "trimester": 3,
        "is_emergency": False,
        "text": "third trimester weeks 27-40 delivery plan kick count hospital preeclampsia left side rest",
    },

    # ── COMMON SYMPTOMS ───────────────────────────────────────────────────────
    {
        "doc_id": "med_040",
        "category": "symptoms",
        "question_en": "How to manage morning sickness and nausea in pregnancy?",
        "answer_en": (
            "Morning sickness is very common in early pregnancy. Tips to manage: "
            "1. Eat small, frequent meals every 2-3 hours instead of 3 large meals. "
            "2. Keep dry crackers or biscuits by your bed — eat before getting up. "
            "3. Ginger tea or ginger candy helps many women. "
            "4. Avoid spicy, oily, or strong-smelling foods. "
            "5. Stay hydrated — sip water, coconut water, or lemon water throughout the day. "
            "6. Rest as needed — fatigue makes nausea worse. "
            "See a doctor if you cannot keep any food down for more than 24 hours."
        ),
        "question_hi": "गर्भावस्था में मतली और उल्टी को कैसे कम करें?",
        "answer_hi": (
            "गर्भावस्था की शुरुआत में मतली बहुत आम है। इससे राहत के उपाय: "
            "1. दिन में 5-6 बार थोड़ा-थोड़ा खाएं। "
            "2. सुबह उठने से पहले बिस्तर पर ही बिस्किट या टोस्ट खाएं। "
            "3. अदरक की चाय या अदरक कैंडी मतली में मदद करती है। "
            "4. तेज मसालेदार और तेल वाले खाने से बचें। "
            "5. पानी, नींबू पानी, नारियल पानी पीते रहें। "
            "6. आराम करें — थकान से मतली बढ़ती है। "
            "24 घंटे से ज्यादा कुछ न खा पाएं तो डॉक्टर से मिलें।"
        ),
        "trimester": 1,
        "is_emergency": False,
        "text": "morning sickness nausea vomiting pregnancy ginger crackers frequent meals hydration",
    },
    {
        "doc_id": "med_041",
        "category": "symptoms",
        "question_en": "Is back pain normal in pregnancy? How to manage it?",
        "answer_en": (
            "Back pain is very common — affects 50-70% of pregnant women. Management: "
            "1. Maintain good posture — sit straight, use a back support pillow. "
            "2. Sleep on your left side with a pillow between your knees. "
            "3. Gentle stretching and prenatal yoga. "
            "4. Warm (not hot) compress on the sore area. "
            "5. Avoid lifting heavy objects. "
            "6. Wear flat, supportive footwear — avoid high heels. "
            "7. Pelvic tilts can help strengthen lower back. "
            "See a doctor if pain is severe, comes with fever, or spreads down the leg."
        ),
        "question_hi": "क्या गर्भावस्था में कमर दर्द सामान्य है? इसे कैसे कम करें?",
        "answer_hi": (
            "कमर दर्द बहुत सामान्य है — 50-70% गर्भवती महिलाओं को होता है। उपाय: "
            "1. सीधे बैठें, पीठ के सहारे तकिया रखें। "
            "2. बायीं करवट सोएं, घुटनों के बीच तकिया रखें। "
            "3. हल्की स्ट्रेचिंग और प्रसवपूर्व योग करें। "
            "4. दर्द वाली जगह पर गुनगुने पानी की सिकाई करें। "
            "5. भारी सामान न उठाएं। "
            "6. फ्लैट, आरामदायक जूते पहनें। "
            "अगर दर्द बहुत तेज हो, बुखार हो या पैर में फैले तो डॉक्टर से मिलें।"
        ),
        "trimester": 2,
        "is_emergency": False,
        "text": "back pain pregnancy posture sleep left side pillow yoga stretching heels",
    },
    {
        "doc_id": "med_042",
        "category": "symptoms",
        "question_en": "How to deal with swelling (edema) in pregnancy?",
        "answer_en": (
            "Mild swelling of feet and ankles is normal in pregnancy. Tips: "
            "1. Rest with feet elevated above heart level for 30 minutes twice daily. "
            "2. Avoid standing for long periods. "
            "3. Reduce salt intake. "
            "4. Stay hydrated — drink 8-10 glasses of water daily. "
            "5. Wear comfortable, loose footwear. "
            "6. Walk gently to improve circulation. "
            "EMERGENCY SIGNS: Sudden severe swelling of face, hands, or legs — "
            "this may be preeclampsia. See a doctor immediately."
        ),
        "question_hi": "गर्भावस्था में सूजन (एडिमा) से कैसे निपटें?",
        "answer_hi": (
            "पैरों और टखनों में हल्की सूजन सामान्य है। उपाय: "
            "1. दिन में दो बार 30 मिनट पैर ऊपर करके आराम करें। "
            "2. लंबे समय तक खड़े न रहें। "
            "3. नमक कम खाएं। "
            "4. दिन में 8-10 गिलास पानी पिएं। "
            "5. आरामदायक, ढीले जूते पहनें। "
            "खतरे के संकेत: चेहरे, हाथों या पैरों में अचानक तेज सूजन — "
            "यह प्रीक्लेम्पसिया हो सकता है। तुरंत डॉक्टर को दिखाएं।"
        ),
        "trimester": 3,
        "is_emergency": False,
        "text": "swelling edema feet ankles pregnancy elevate rest salt water preeclampsia",
    },

    # ── NUTRITION ─────────────────────────────────────────────────────────────
    {
        "doc_id": "med_050",
        "category": "nutrition",
        "question_en": "What foods should a pregnant woman eat for iron?",
        "answer_en": (
            "Iron is critical in pregnancy to prevent anemia. Best iron-rich Indian foods: "
            "1. Dark leafy greens: palak (spinach), methi (fenugreek), sarson. "
            "2. Legumes: chana, rajma, masoor dal, moong dal. "
            "3. Jaggery (gud) — traditional iron-rich sweetener. "
            "4. Til (sesame seeds). "
            "5. Dry fruits: raisins, dates, figs. "
            "6. Pomegranate (anar). "
            "7. Eggs and lean meat. "
            "TIP: Eat vitamin C rich food with iron foods to absorb iron better. "
            "Example: squeeze lemon on palak sabzi, or eat amla with dal. "
            "AVOID: Tea or coffee with iron-rich meals — they block iron absorption."
        ),
        "question_hi": "गर्भवती महिला को आयरन के लिए क्या खाना चाहिए?",
        "answer_hi": (
            "गर्भावस्था में खून की कमी से बचने के लिए आयरन बहुत जरूरी है। "
            "आयरन से भरपूर भारतीय खाद्य पदार्थ: "
            "1. हरी पत्तेदार सब्जियां: पालक, मेथी, सरसों के पत्ते। "
            "2. दालें: चना, राजमा, मसूर दाल, मूंग दाल। "
            "3. गुड़ — पारंपरिक आयरन से भरपूर मिठाई। "
            "4. तिल। "
            "5. सूखे मेवे: किशमिश, खजूर, अंजीर। "
            "6. अनार। "
            "7. अंडे। "
            "सुझाव: आयरन वाले खाने के साथ विटामिन C लें — जैसे पालक पर नींबू। "
            "बचें: आयरन वाले खाने के साथ चाय या कॉफी न पिएं।"
        ),
        "trimester": 0,
        "is_emergency": False,
        "text": "iron anemia pregnancy spinach dal jaggery sesame lemon vitamin C absorption tea avoid",
    },
    {
        "doc_id": "med_051",
        "category": "nutrition",
        "question_en": "What foods are good for calcium during pregnancy?",
        "answer_en": (
            "Calcium builds your baby's bones and teeth. Daily requirement: 1000-1200mg. "
            "Best calcium foods: "
            "1. Milk (1 glass = 300mg calcium). "
            "2. Dahi/curd (1 cup = 200mg). "
            "3. Paneer (100g = 480mg). "
            "4. Ragi (finger millet) — highest calcium grain, 344mg/100g. "
            "5. Sesame seeds (til). "
            "6. Rajma and chana. "
            "7. Drumstick leaves (moringa/sahjan) — excellent source. "
            "TIP: Vitamin D is needed to absorb calcium. Get 20-30 minutes of morning sunlight daily."
        ),
        "question_hi": "गर्भावस्था में कैल्शियम के लिए क्या खाएं?",
        "answer_hi": (
            "कैल्शियम बच्चे की हड्डियां और दांत बनाता है। रोज 1000-1200mg चाहिए। "
            "कैल्शियम से भरपूर खाना: "
            "1. दूध (1 गिलास = 300mg)। "
            "2. दही (1 कप = 200mg)। "
            "3. पनीर (100g = 480mg)। "
            "4. रागी — सबसे ज्यादा कैल्शियम वाला अनाज। "
            "5. तिल। "
            "6. राजमा और चना। "
            "7. सहजन (मोरिंगा) के पत्ते। "
            "सुझाव: कैल्शियम सोखने के लिए विटामिन D जरूरी है — रोज सुबह 20-30 मिनट धूप लें।"
        ),
        "trimester": 0,
        "is_emergency": False,
        "text": "calcium pregnancy milk dahi paneer ragi ragi sesame drumstick vitamin D sunlight bone teeth",
    },

    # ── VACCINES ──────────────────────────────────────────────────────────────
    {
        "doc_id": "med_060",
        "category": "vaccines",
        "question_en": "What vaccines (injections) are needed during pregnancy?",
        "answer_en": (
            "Essential vaccines in pregnancy: "
            "1. Tetanus Toxoid (TT): 2 doses. First dose as soon as pregnancy confirmed. "
            "   Second dose 4 weeks after first dose. Protects mother and baby from tetanus. "
            "2. Influenza (flu) vaccine: Recommended in any trimester — protects from severe flu. "
            "3. Covid-19 booster if applicable. "
            "All vaccines at government hospitals and PHCs are FREE for pregnant women."
        ),
        "question_hi": "गर्भावस्था में कौन से टीके जरूरी हैं?",
        "answer_hi": (
            "गर्भावस्था में जरूरी टीके: "
            "1. टेटनस टॉक्सॉइड (TT): 2 खुराकें। पहली खुराक गर्भावस्था की पुष्टि होते ही। "
            "   दूसरी खुराक पहली खुराक के 4 सप्ताह बाद। माँ और बच्चे को टेटनस से बचाता है। "
            "2. इन्फ्लुएंजा (फ्लू) टीका: किसी भी तिमाही में लगवाएं। "
            "3. कोविड-19 बूस्टर यदि लागू हो। "
            "सरकारी अस्पतालों और PHC में ये सभी टीके गर्भवती महिलाओं को मुफ्त मिलते हैं।"
        ),
        "trimester": 0,
        "is_emergency": False,
        "text": "vaccine injection TT tetanus toxoid influenza flu covid pregnancy free PHC",
    },

    # ── POSTPARTUM ────────────────────────────────────────────────────────────
    {
        "doc_id": "med_070",
        "category": "postpartum",
        "question_en": "What care is needed after delivery (postpartum)?",
        "answer_en": (
            "After delivery, care for yourself and your baby: "
            "1. Breastfeed within 1 hour of birth — colostrum (first milk) is vital for baby. "
            "2. Rest as much as possible — at least 6-8 weeks recovery. "
            "3. Eat nutritious foods: dal, green vegetables, dry fruits, milk. "
            "4. Take iron and calcium tablets as prescribed. "
            "5. Postnatal checkup at 7 days and 42 days after delivery. "
            "6. Baby's first vaccines: BCG, OPV, Hep-B at birth. "
            "7. Watch for warning signs: heavy bleeding, fever, foul smell, severe sadness/depression. "
            "8. Register for JSY (Janani Suraksha Yojana) to get Rs.1400 delivery benefit."
        ),
        "question_hi": "प्रसव के बाद (प्रसवोत्तर) क्या देखभाल जरूरी है?",
        "answer_hi": (
            "प्रसव के बाद अपनी और बच्चे की देखभाल: "
            "1. जन्म के 1 घंटे के भीतर स्तनपान शुरू करें — कोलोस्ट्रम बहुत जरूरी है। "
            "2. कम से कम 6-8 हफ्ते पूरा आराम करें। "
            "3. पौष्टिक खाना खाएं: दाल, हरी सब्जियां, सूखे मेवे, दूध। "
            "4. बताई गई आयरन और कैल्शियम की गोलियां लें। "
            "5. 7 दिन और 42 दिन बाद प्रसवोत्तर जांच करवाएं। "
            "6. बच्चे को जन्म पर: BCG, OPV, हेप-B टीके लगवाएं। "
            "7. खतरे के संकेत: ज्यादा खून बहना, बुखार, बदबूदार स्राव, अत्यधिक उदासी। "
            "8. JSY योजना में रजिस्ट्रेशन करें — 1400 रुपये का लाभ।"
        ),
        "trimester": 0,
        "is_emergency": False,
        "text": "postpartum after delivery breastfeeding colostrum rest nutrition BCG OPV vaccine JSY postnatal checkup depression",
    },
]
