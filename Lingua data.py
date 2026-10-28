"""LinguaShield - training data and test data.
DATA     = messages the n-gram model learns from.
TEST_SET = different messages the model has NOT seen (used on the Evaluation tab).
Languages: English, Hindi, Telugu, Tamil, Kannada, plus Hinglish and Tenglish (romanized)."""

DATA = {
    "spam": [
        # English
        "Congratulations! You won a free prize. Click the link now.",
        "Your account will be blocked. Send OTP immediately.",
        "You won Rs 50000 lottery. Click this link and share your OTP.",
        "Urgent: your bank KYC expired. Click the link to update your account.",
        "Free gift card! Claim your prize today, click here.",
        "Your card is suspended. Provide your OTP to unblock.",
        # Hindi
        "आपका अकाउंट बंद हो जाएगा। OTP भेजें।",
        "बधाई हो! आपने ₹50,000 का इनाम जीता है। लिंक पर क्लिक करें।",
        "आपका KYC अपडेट करें, वरना खाता ब्लॉक होगा। तुरंत लिंक पर क्लिक करें।",
        "मुफ्त लॉटरी जीतें। अभी क्लिक करें और बैंक खाता बताएं।",
        "आपका कार्ड बंद हो जाएगा। तुरंत OTP बताएं।",
        # Telugu
        "మీ ఖాతా బ్లాక్ అవుతుంది. వెంటనే OTP పంపండి.",
        "అభినందనలు! మీరు ₹50,000 లాటరీ గెలుచుకున్నారు. ఈ లింక్ క్లిక్ చేయండి.",
        "మీ KYC గడువు ముగిసింది. వెంటనే లింక్ క్లిక్ చేసి వివరాలు ఇవ్వండి.",
        "ఉచిత బహుమతి గెలవండి. ఇప్పుడే క్లిక్ చేయండి.",
        "మీ కార్డ్ బ్లాక్ అవుతుంది. OTP ఇవ్వండి.",
        # Tamil
        "உங்கள் கணக்கு முடக்கப்படும். உடனே OTP அனுப்பவும்.",
        "நீங்கள் பரிசு வென்றுள்ளீர்கள்! இந்த இணைப்பை கிளிக் செய்யவும்.",
        "இலவச பரிசு பெற உடனே கிளிக் செய்யவும்.",
        "உங்கள் அட்டை தடை செய்யப்படும். OTP பகிரவும்.",
        # Kannada
        "ನಿಮ್ಮ ಖಾತೆ ಬ್ಲಾಕ್ ಆಗುತ್ತದೆ. ತಕ್ಷಣ OTP ಕಳುಹಿಸಿ.",
        "ನೀವು ಬಹುಮಾನ ಗೆದ್ದಿದ್ದೀರಿ! ಈ ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಿ.",
        "ಉಚಿತ ಉಡುಗೊರೆ ಪಡೆಯಲು ಈಗಲೇ ಕ್ಲಿಕ್ ಮಾಡಿ.",
        "ನಿಮ್ಮ ಕಾರ್ಡ್ ಬ್ಲಾಕ್ ಆಗುತ್ತದೆ. OTP ನೀಡಿ.",
        # Hinglish (Hindi in English letters)
        "Aapka account block ho jayega. OTP bhejiye abhi.",
        "Aapne lottery jeeta hai! Inaam ke liye link par click karein.",
        "Free gift paane ke liye turant click karein aur bank khata batayein.",
        "Aapka card band ho jayega. Jaldi OTP bhejo.",
        # Tenglish (Telugu in English letters)
        "Mee account block avutundi. Ventane OTP ivvandi.",
        "Meeru lottery gelichaaru! Ee link click cheyandi.",
        "Free bahumathi kosam ippude click cheyandi.",
    ],
    "ham": [
        # English
        "Meeting is tomorrow at 10. Thanks.",
        "Please send me the report today.",
        "Can you share the notes with me today?",
        "I will send the file tomorrow. Thanks.",
        "Please give me the book tomorrow.",
        "Send me the photos now, I want to see them.",
        "Are we having lunch tomorrow?",
        "Happy birthday! See you tomorrow.",
        "I reviewed your report, it looks good. Thanks.",
        "Dinner at home tonight, mom made your favourite.",
        # Hindi
        "कृपया आज रिपोर्ट भेज दो। धन्यवाद।",
        "कृपया मुझे आज फाइल भेजें।",
        "कल शाम को बैठक है। धन्यवाद।",
        "खाना खाने घर आ जाओ।",
        "मैं कल ऑफिस आऊंगा।",
        "जन्मदिन मुबारक! कल मिलते हैं।",
        "तुम्हारी रिपोर्ट देखी, अच्छी है। धन्यवाद।",
        # Telugu
        "కృపయా ఈరోజు నోట్స్ పంపండి. ధన్యవాదాలు.",
        "దయచేసి ఈరోజు రిపోర్ట్ పంపండి. ధన్యవాదాలు.",
        "ఇప్పుడే ఫోటోలు పంపండి, చూడాలి.",
        "రేపు సాయంత్రం సమావేశం ఉంది. ధన్యవాదాలు.",
        "భోజనానికి ఇంటికి రండి.",
        "నేను రేపు ఆఫీసుకి వస్తాను.",
        "పుట్టినరోజు శుభాకాంక్షలు! రేపు కలుద్దాం.",
        "నీ రిపోర్ట్ చూశాను, బాగుంది. ధన్యవాదాలు.",
        # Tamil
        "நாளை மாலை கூட்டம் உள்ளது. நன்றி.",
        "உணவு சாப்பிட வீட்டுக்கு வாருங்கள்.",
        "பிறந்தநாள் வாழ்த்துக்கள்! நாளை சந்திக்கலாம்.",
        # Kannada
        "ನಾಳೆ ಸಂಜೆ ಸಭೆ ಇದೆ. ಧನ್ಯವಾದ.",
        "ಊಟಕ್ಕೆ ಮನೆಗೆ ಬನ್ನಿ.",
        "ಹುಟ್ಟುಹಬ್ಬದ ಶುಭಾಶಯಗಳು! ನಾಳೆ ಭೇಟಿಯಾಗೋಣ.",
        # Hinglish
        "Kal shaam ko meeting hai. Dhanyavad.",
        "Khana ghar par hai, aa jao.",
        "Janamdin ki shubhkamnayein! Kal milte hain.",
        "Aaj ka report bhej do please, shukriya.",
        # Tenglish
        "Repu sayantram meeting undi. Thanks.",
        "Bhojanam intlo cheddam, randi.",
        "Puttinaroju subhakankshalu! Repu kaladdam.",
    ],
}

# (label, language tag, text) - none of these appear in DATA
TEST_SET = [
    # English spam
    ("spam", "English", "Hurry! You have won a lottery of Rs 25 lakh. Click the link to claim your prize."),
    ("spam", "English", "Your bank account is suspended. Share your OTP now to reactivate."),
    ("spam", "English", "Free recharge offer! Click here today and win cash prizes."),
    ("spam", "English", "Dear customer your KYC is pending. Update immediately or your card will be blocked."),
    ("spam", "English", "Congratulations winner! Send your bank account details to get your free gift."),
    ("spam", "English", "Your SIM will be blocked today. Provide OTP to continue service."),
    # English normal
    ("ham", "English", "Don't forget the meeting tomorrow morning."),
    ("ham", "English", "Thanks for the lunch, it was great."),
    ("ham", "English", "I will call you tomorrow after dinner."),
    ("ham", "English", "Happy birthday! Wishing you a wonderful year."),
    ("ham", "English", "Please share the notes from today's class."),
    ("ham", "English", "Your OTP for login is 4821. Do not share it with anyone."),
    # Hindi
    ("spam", "Hindi", "आपका बैंक खाता आज ब्लॉक होगा। अभी अपना OTP बताएं।"),
    ("spam", "Hindi", "बधाई! आपने मुफ्त इनाम जीता है। अभी लिंक पर क्लिक करें।"),
    ("spam", "Hindi", "आपका कार्ड बंद हो गया है। तुरंत केवाईसी अपडेट करें और OTP दीजिए।"),
    ("ham", "Hindi", "कल दोपहर को खाना साथ खाएंगे।"),
    ("ham", "Hindi", "आज की बैठक के नोट्स भेज दो, धन्यवाद।"),
    ("ham", "Hindi", "जन्मदिन की बहुत बधाई! कल मिलते हैं।"),
    # Telugu
    ("spam", "Telugu", "అభినందనలు! మీరు ఉచిత లాటరీ గెలిచారు. ఈ లింక్ క్లిక్ చేసి బ్యాంక్ వివరాలు పంపండి."),
    ("spam", "Telugu", "మీ KYC ఈరోజు ముగుస్తుంది. వెంటనే లింక్ క్లిక్ చేయండి."),
    ("ham", "Telugu", "రేపు ఉదయం సమావేశం ఉంది, మర్చిపోవద్దు. ధన్యవాదాలు."),
    ("ham", "Telugu", "ఈరోజు భోజనం ఇంట్లో చేద్దాం."),
    ("ham", "Telugu", "పుట్టినరోజు శుభాకాంక్షలు! రేపు పార్టీకి రండి."),
    # Tamil
    ("spam", "Tamil", "உங்கள் வங்கி கணக்கு இன்று முடக்கப்படும். உடனே OTP அனுப்பவும்."),
    ("spam", "Tamil", "வாழ்த்துக்கள்! நீங்கள் இலவச பரிசு வென்றுள்ளீர்கள். இந்த இணைப்பை கிளிக் செய்யவும்."),
    ("ham", "Tamil", "நாளை கூட்டம் உள்ளது. நன்றி."),
    ("ham", "Tamil", "இன்று மதிய உணவு வீட்டில் சாப்பிடலாம்."),
    # Kannada
    ("spam", "Kannada", "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆ ಇಂದು ಬ್ಲಾಕ್ ಆಗುತ್ತದೆ. ತಕ್ಷಣ OTP ಕಳುಹಿಸಿ."),
    ("spam", "Kannada", "ಅಭಿನಂದನೆಗಳು! ನೀವು ಉಚಿತ ಬಹುಮಾನ ಗೆದ್ದಿದ್ದೀರಿ. ಈ ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಿ."),
    ("ham", "Kannada", "ನಾಳೆ ಸಭೆ ಇದೆ. ಧನ್ಯವಾದ."),
    ("ham", "Kannada", "ಇಂದು ಊಟ ಮನೆಯಲ್ಲಿ ಮಾಡೋಣ."),
    # Hinglish
    ("spam", "Hinglish", "Aapka account band ho jayega. Turant OTP bhejein."),
    ("spam", "Hinglish", "Badhai ho! Aapne lottery jeeti hai. Abhi link par click karein."),
    ("spam", "Hinglish", "Aapka bank khata block ho gaya hai. Abhi KYC update karein link par click karke."),
    ("ham", "Hinglish", "Kal meeting hai, dhanyavad."),
    ("ham", "Hinglish", "Aaj dinner ghar par karenge."),
    ("ham", "Hinglish", "Janamdin mubarak! Kal milte hain."),
    # Tenglish
    ("spam", "Tenglish", "Mee bank account ee roju block avutundi. Ventane OTP pampandi."),
    ("spam", "Tenglish", "Abhinandanalu! Meeru free bahumathi gelichaaru. Link click cheyandi."),
    ("ham", "Tenglish", "Repu meeting undi, dhanyavadalu."),
    ("ham", "Tenglish", "Ee roju lunch intlo cheddam."),
]