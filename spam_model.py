"""Multilingual Spam Shield - model (no Streamlit code here).
N-Gram model + cross-lingual (shared concept token) processing for English, Hindi, Telugu."""
import re
import math
from collections import Counter

# ---------- 1. Cross-lingual lexicon: word stems -> shared concept ----------
LEX = {
    "OTP": ["otp", "ఓటీపీ", "ओटीपी"],
    "BLOCK": ["block", "suspend", "బ్లాక్", "గడువు", "ब्लॉक", "बंद"],
    "WIN": ["won", "win", "winner", "prize", "lottery", "congratulation", "గెల", "బహుమతి", "లాటరీ", "అభినందన", "जीत", "इनाम", "लॉटरी", "बधाई"],
    "FREE": ["free", "ఉచిత", "मुफ्त", "मुफ़्त"],
    "CLICK": ["click", "tap", "క్లిక్", "क्लिक"],
    "LINK": ["link", "లింక్", "लिंक"],
    "URGENT": ["urgent", "immediately", "now", "today", "వెంటనే", "ఈరోజు", "ఇప్పుడే", "तुरंत", "अभी", "आज", "जल्दी"],
    "SEND": ["send", "share", "provide", "give", "పంప", "ఇవ్వ", "భేజ", "भेज", "बताएं", "बताए", "दीजिए"],
    "BANK": ["bank", "account", "kyc", "card", "atm", "బ్యాంక్", "ఖాత", "కార్డ్", "केवाईसी", "खाता", "बैंक", "अकाउंट", "कार्ड"],
    "MONEY": ["rs", "rupee", "cash", "loan", "₹", "రూపాయ", "रुपये", "रुपए"],
    "MEET": ["meeting", "meet", "సమావేశ", "बैठक"],
    "FOOD": ["lunch", "dinner", "భోజన", "खाना", "खाने"],
    "THANKS": ["thank", "ధన్యవాద", "धन्यवाद", "शुक्रिया"],
    "TOMORROW": ["tomorrow", "రేపు", "कल"],
    "GREET": ["birthday", "శుభాకాంక్ష", "जन्मदिन"],
}


def concept(tok):
    for c, stems in LEX.items():
        for s in stems:
            if re.match(r"[a-z]", s):
                if tok in (s, s + "s", s + "ed", s + "d"):
                    return c
            elif tok.startswith(s):
                return c
    return None


# ---------- 2. Language detection + text processing ----------
def detect_lang(t):
    te = len(re.findall(r"[\u0C00-\u0C7F]", t))
    hi = len(re.findall(r"[\u0900-\u097F]", t))
    en = len(re.findall(r"[A-Za-z]", t))
    if not (te or hi or en):
        return "Unknown"
    if te >= hi and te >= en / 2:
        return "Telugu"
    if hi >= en / 2:
        return "Hindi"
    return "English"


URL_RE = re.compile(r"(https?://\S+|www\.\S+|\b[a-z0-9-]+\.(?:ly|co|xyz|top|click|link|in|com)/\S*)", re.I)
# word characters: letters/digits plus the whole Telugu block and Devanagari (without the danda marks)
WORD_SPLIT = re.compile(r"[^\w\u0900-\u0963\u0966-\u097F\u0C00-\u0C7F₹]+")


def process(text):
    urls = [m.group(0) for m in URL_RE.finditer(text)]
    t = URL_RE.sub(" urltoken ", text.lower()).replace("₹", " ₹ ")
    toks = []
    for w in WORD_SPLIT.split(t):
        if not w:
            continue
        if w == "urltoken":
            toks.append("URL")
        elif w.isdigit():
            toks.append("NUM")
        else:
            toks.append(concept(w) or w)
    return urls, toks


def ngrams(toks):
    out = []
    for n in (1, 2, 3):
        for i in range(len(toks) - n + 1):
            out.append((n, " ".join(toks[i:i + n])))
    return out


# ---------- 3. Training data (small demo corpus) ----------
DATA = {
    "spam": [
        "Congratulations! You won a free prize. Click the link now.",
        "Your account will be blocked. Send OTP immediately.",
        "You won Rs 50000 lottery. Click this link and share your OTP.",
        "Urgent: your bank KYC expired. Click the link to update your account.",
        "Free gift card! Claim your prize today, click here.",
        "Your card is suspended. Provide your OTP to unblock.",
        "आपका अकाउंट बंद हो जाएगा। OTP भेजें।",
        "बधाई हो! आपने ₹50,000 का इनाम जीता है। लिंक पर क्लिक करें।",
        "आपका KYC अपडेट करें, वरना खाता ब्लॉक होगा। तुरंत लिंक पर क्लिक करें।",
        "मुफ्त लॉटरी जीतें। अभी क्लिक करें और बैंक खाता बताएं।",
        "आपका कार्ड बंद हो जाएगा। तुरंत OTP बताएं।",
        "మీ ఖాతా బ్లాక్ అవుతుంది. వెంటనే OTP పంపండి.",
        "అభినందనలు! మీరు ₹50,000 లాటరీ గెలుచుకున్నారు. ఈ లింక్ క్లిక్ చేయండి.",
        "మీ KYC గడువు ముగిసింది. వెంటనే లింక్ క్లిక్ చేసి వివరాలు ఇవ్వండి.",
        "ఉచిత బహుమతి గెలవండి. ఇప్పుడే క్లిక్ చేయండి.",
        "మీ కార్డ్ బ్లాక్ అవుతుంది. OTP ఇవ్వండి.",
    ],
    "ham": [
        "Meeting is tomorrow at 10. Thanks.",
        "Please send me the report today.",
        "Can you share the notes with me today?",
        "I will send the file tomorrow. Thanks.",
        "Please give me the book tomorrow.",
        "Send me the photos now, I want to see them.",
        "कृपया आज रिपोर्ट भेज दो। धन्यवाद।",
        "कृपया मुझे आज फाइल भेजें।",
        "కృపయా ఈరోజు నోట్స్ పంపండి. ధన్యవాదాలు.",
        "దయచేసి ఈరోజు రిపోర్ట్ పంపండి. ధన్యవాదాలు.",
        "ఇప్పుడే ఫోటోలు పంపండి, చూడాలి.",
        "Are we having lunch tomorrow?",
        "Happy birthday! See you tomorrow.",
        "I reviewed your report, it looks good. Thanks.",
        "Dinner at home tonight, mom made your favourite.",
        "कल शाम को बैठक है। धन्यवाद।",
        "खाना खाने घर आ जाओ।",
        "मैं कल ऑफिस आऊंगा।",
        "जन्मदिन मुबारक! कल मिलते हैं।",
        "तुम्हारी रिपोर्ट देखी, अच्छी है। धन्यवाद।",
        "రేపు సాయంత్రం సమావేశం ఉంది. ధన్యవాదాలు.",
        "భోజనానికి ఇంటికి రండి.",
        "నేను రేపు ఆఫీసుకి వస్తాను.",
        "పుట్టినరోజు శుభాకాంక్షలు! రేపు కలుద్దాం.",
        "నీ రిపోర్ట్ చూశాను, బాగుంది. ధన్యవాదాలు.",
    ],
}
W = {1: 0.5, 2: 1.0, 3: 1.2}
COUNTS = {"spam": Counter(), "ham": Counter()}
TOTALS = {"spam": Counter(), "ham": Counter()}
VOCAB = set()
for _cls, _msgs in DATA.items():
    for _m in _msgs:
        for _n, _g in ngrams(process(_m)[1]):
            COUNTS[_cls][_g] += 1
            TOTALS[_cls][_n] += 1
            VOCAB.add(_g)

# ---------- 4. Scoring (channel-aware) ----------
SIGNALS = [
    ("Prize / winning claim", lambda c: "WIN" in c or "FREE" in c, 0.6),
    ("Urgent action", lambda c: "URGENT" in c, 0.2),
    ("Link request", lambda c: "CLICK" in c or "LINK" in c, 0.5),
    ("OTP request", lambda c: "OTP" in c, 1.0),
    ("Account threat", lambda c: "BLOCK" in c and ("BANK" in c or "OTP" in c), 0.7),
    ("Money mentioned", lambda c: "MONEY" in c, 0.2),
]
TRUSTED = ["whatsapp.com", "google.com", "youtube.com", "github.com", "wikipedia.org", "microsoft.com", "amazon.in",
           "amazon.com", "claude.ai", "anthropic.com", "linkedin.com", "instagram.com", "facebook.com", "apple.com",
           "netflix.com", "paypal.com", "flipkart.com", "paytm.com", "sbi.co.in", "onlinesbi.sbi", "hdfcbank.com",
           "icicibank.com"]
BRANDS = ["whatsapp", "google", "paytm", "sbi", "hdfc", "icici", "amazon", "flipkart", "paypal", "microsoft",
          "netflix", "apple", "instagram", "facebook"]
FREE_MAIL = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "rediffmail.com"]
SHORTENER = re.compile(r"^(bit\.ly|tinyurl\.com|t\.co|goo\.gl|rb\.gy|cutt\.ly|is\.gd)$", re.I)
RISKY_TLD = re.compile(r"\.(xyz|top|click|link|buzz|icu|cfd|rest|gq|tk)$", re.I)

PROFILE = {
    "SMS": {"urlW": 1.3, "otpW": 1.0, "ngram": 0.6, "note": "SMS rules: links count more, because most scam texts push a link."},
    "Call": {"urlW": 0.5, "otpW": 1.4, "ngram": 0.6, "note": "Call rules: asking for an OTP or bank details on a call is a strong warning sign."},
    "Email": {"urlW": 1.0, "otpW": 1.1, "ngram": 0.6, "note": "Email rules: the sender address is checked if you enter it."},
    "Chat": {"urlW": 0.9, "otpW": 1.0, "ngram": 0.6, "note": "Chat rules: being asked to send money is a warning sign, and links count a little less."},
    "Link": {"urlW": 2.2, "otpW": 1.0, "ngram": 0.3, "note": "Link rules: the web address itself is checked in detail."},
}


def host_of(u):
    h = re.sub(r"^[a-z]+://", "", u, flags=re.I)
    h = re.split(r"[/?#]", h)[0]
    h = re.sub(r"^.*@", "", h)
    h = re.sub(r":\d+$", "", h)
    h = re.sub(r"^www\.", "", h, flags=re.I)
    return h.lower()


def is_trusted(h):
    return any(h == d or h.endswith("." + d) for d in TRUSTED)


def url_checks(u):
    h = host_of(u)
    r = []
    r.append(("Known site: " + h, -0.5) if is_trusted(h) else ("Unverified link", 0.4))
    if re.match(r"http://", u, re.I):
        r.append(("Not secure (http)", 0.3))
    if SHORTENER.search(h):
        r.append(("Shortened link hides the real site", 0.8))
    if RISKY_TLD.search(h):
        r.append(("Risky domain ending (." + h.split(".")[-1] + ")", 0.8))
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", h):
        r.append(("IP address instead of a name", 1.0))
    if re.match(r"[a-z]+://[^/?#]*@", u, re.I):
        r.append(("'@' in the address hides the real site", 0.8))
    if h.count("-") >= 2:
        r.append(("Many hyphens in the domain", 0.4))
    if len(h.split(".")) > 4:
        r.append(("Too many subdomains", 0.4))
    if re.search(r"(^|\.)xn--", h):
        r.append(("Look-alike characters in the domain", 0.8))
    b = next((x for x in BRANDS if x in h), None)
    if b and not is_trusted(h):
        r.append(("Uses the name '" + b + "' but is not the real site", 1.0))
    return r


def analyze(text, channel="SMS", sender=""):
    channel = channel if channel in PROFILE else "SMS"
    P = PROFILE[channel]
    text = text.strip()
    if channel == "Link" and re.match(r"^\S+\.\S+$", text) and not re.match(r"^(https?://|www\.)", text, re.I):
        text = "https://" + text
    lang = detect_lang(text)
    urls, toks = process(text)
    present = {t for t in toks if t in LEX}
    lo = 0.0
    contrib = []
    for n, g in ngrams(toks):
        s, h = COUNTS["spam"][g], COUNTS["ham"][g]
        if not s and not h:
            continue
        ps = (s + 1) / (TOTALS["spam"][n] + len(VOCAB))
        ph = (h + 1) / (TOTALS["ham"][n] + len(VOCAB))
        v = math.log(ps / ph) * W[n]
        lo += v
        contrib.append((g, v))
    sig = []
    bonus = 0.0
    for name, f, b in SIGNALS:
        if f(present):
            sig.append(name)
            bonus += b * P["otpW"] if name == "OTP request" else b
    if channel == "Call" and "SEND" in present and ("OTP" in present or "BANK" in present):
        sig.append("Asks for secret details on a call")
        bonus += 0.6
    if channel == "Chat" and "SEND" in present and "MONEY" in present:
        sig.append("Asks you to send money")
        bonus += 0.8
    links = [{"url": u, "host": host_of(u), "checks": url_checks(u)} for u in urls]
    ub = 0.0
    for l in links:
        for name, b in l["checks"]:
            ub += b
            if name not in sig:
                sig.append(name)
    bonus += ub * P["urlW"]
    if channel == "Email" and sender:
        sh = sender.lower().split("@")[-1].strip()
        brand = next((x for x in BRANDS if x in sh), None)
        if sh in FREE_MAIL and ("BANK" in present or "OTP" in present):
            sig.append("Bank or OTP message from a free email address")
            bonus += 1.0
        elif brand and not is_trusted(sh):
            sig.append("Sender looks like '" + brand + "' but is not the real domain")
            bonus += 1.2
        elif is_trusted(sh):
            sig.append("Sender domain is known: " + sh)
            bonus -= 0.3
    z = max(-50.0, min(50.0, lo * P["ngram"] + bonus - 1.5))
    p = min(0.99, max(0.01, 1 / (1 + math.exp(-z))))
    top = [g for g, v in sorted([c for c in contrib if c[1] > 0.3], key=lambda x: -x[1])[:6]]
    return {"lang": lang, "toks": toks, "urls": urls, "links": links, "sig": sig, "p": p,
            "channel": channel, "note": P["note"], "top": top}


# ---------- 5. Does the text fit the chosen tab? ----------
def looks_like_link(t):
    if re.search(r"\s", t):
        return False
    if re.match(r"^(https?://|www\.|ftp://|file://)", t, re.I):
        return True
    if re.search(r"\.(pdf|docx?|xlsx?|pptx?|txt|png|jpe?g|gif|zip|mp3|mp4|js|css|html?)$", t, re.I):
        return False
    return bool(re.match(r"^[\w-]+(\.[\w-]+)+(/\S*)?$", t))


EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def guess_channel(t, cur):
    def hit(pat, w, flags=re.I):
        return w if re.search(pat, t, flags) else 0
    lines = len([x for x in t.split("\n") if x.strip()])
    s = {
        "Email": hit(r"^\s*subject\s*:", 2, re.I | re.M) + hit(r"^\s*(from|to)\s*:", 2, re.I | re.M)
        + hit(r"\bdear\s+(customer|sir|madam|user|member|valued|account)", 1)
        + hit(r"\b(regards|sincerely|yours faithfully)\b", 1)
        + hit(r"[\w.+-]+@[\w-]+\.[\w.-]+", 1) + hit(r"\bunsubscribe\b", 1)
        + (1 if lines >= 3 else 0) + (1 if len(t) > 500 else 0) + hit(r"प्रिय ग्राहक|ప్రియమైన", 1),
        "Call": hit(r"\b(calling from|i am calling|i'm calling|this call|on the call|hold the line|customer care|our executive|can you hear me|am i speaking)\b", 2)
        + hit(r"\b(hello|hi|good (morning|afternoon|evening))\s+(sir|madam|ma'am)\b", 1)
        + hit(r"नमस्ते|मैडम|कॉल पर|నమస్కారం", 1),
        "Chat": hit(r"^\s*(hi+|hey+|hello+|yo)\b", 1) + hit(r"\b(bro|bhai|yaar|dude|buddy|machan)\b", 1)
        + (1 if EMOJI.search(t) else 0)
        + hit(r"\b(i am in trouble|i'm in trouble|it'?s me|new number|lost my phone|are you there|u there|dm me|text me|whatsapp me)\b", 1)
        + hit(r"भाई|यार|హాయ్|అన్నా|బ్రో", 1),
        "SMS": hit(r"\ba/c\b", 1) + hit(r"\btxn\b", 1) + hit(r"\bref(erence)?\.? ?(no|id)\b", 1)
        + hit(r"\breply (stop|yes|y)\b", 1) + hit(r"\bdo not share\b", 1) + hit(r"-\s?[A-Z]{3,8}\s*$", 1, 0),
    }
    best = None
    for k in s:
        if k != cur and (best is None or s[k] > s[best]):
            best = k
    return best if best and s[best] >= 2 and s[best] > s[cur] else None


KIND = {"SMS": "an SMS", "Call": "a call transcript", "Email": "an email", "Chat": "a chat message"}


def check(text, channel, sender="", force=False):
    """Main entry point used by the Streamlit app. Returns a dict with a 'status' key:
    empty | error | redirect | ok"""
    text = text.strip()
    if not text:
        return {"status": "empty"}
    link = looks_like_link(text)
    if channel == "Link":
        if text.lower().startswith("file://"):
            return {"status": "error", "title": "Not a web link",
                    "msg": "That is a file on your computer, not a web address. Paste a link that starts with http, https or www."}
        if not link:
            return {"status": "redirect", "title": "Link tab needs a link", "targets": ["SMS", "Chat"], "anyway": False,
                    "msg": "This looks like a message, not a single web link. Messages are checked in the SMS, Call, Email and Chat tabs."}
    elif link:
        return {"status": "redirect", "title": "That is a link", "targets": ["Link"], "anyway": False,
                "msg": f"You typed only a web link. Links are checked in the Link tab, where the address is inspected in detail. The {channel} tab is for message text."}
    if channel != "Link" and not force:
        g = guess_channel(text, channel)
        if g:
            return {"status": "redirect", "title": "This looks like " + KIND[g], "targets": [g], "anyway": True,
                    "msg": f"The style of this text matches the {g} tab, not {channel}. Each tab uses its own rules, so you get a better result in the right one."}
    r = analyze(text, channel, sender)
    r["status"] = "ok"
    return r
