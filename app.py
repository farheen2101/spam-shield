import streamlit as st
from spam_model import check

st.set_page_config(page_title="Multilingual Spam Shield", page_icon="🛡️", layout="centered")

CH = {
    "SMS": ("📱", "Paste the text message."),
    "Call": ("📞", "Paste the transcript from speech-to-text. Voice is not analysed, only the words."),
    "Email": ("📧", "Paste the subject and body together. Add the sender address if you have it."),
    "Chat": ("💬", "Paste the chat message."),
    "Link": ("🔗", "Paste one web link only. For a message that contains a link, use SMS, Call, Email or Chat."),
}
SAMPLES = [
    ("English scam", "SMS", "Congratulations! You won ₹50,000. Click the link and provide your OTP.", ""),
    ("Hindi scam", "SMS", "आपका अकाउंट बंद हो जाएगा। OTP भेजें।", ""),
    ("Telugu scam", "SMS", "మీ బ్యాంక్ ఖాతా ఈరోజు బ్లాక్ అవుతుంది. వెంటనే OTP పంపండి.", ""),
    ("Call scam", "Call", "Hello sir, I am calling from your bank. Your card will be blocked today. Please share the OTP you just received.", ""),
    ("Email scam", "Email", "Your account will be suspended. Click the link to verify your bank account now: http://sbi-secure-login.xyz/verify", "alert@sbi-help.xyz"),
    ("Chat scam", "Chat", "Hi, I am in trouble. Please send Rs 5000 now, it is urgent.", ""),
    ("Link scam", "Link", "http://bit.ly/kyc-upd8", ""),
    ("Safe message", "SMS", "Meeting is tomorrow at 10. Thanks.", ""),
]
ADVICE = {
    "SMS": "Do not tap the link or reply with codes. Block the number and report it at cybercrime.gov.in or call 1930.",
    "Call": "Hang up. A bank never asks for your OTP or PIN on a call. Call the bank on the number printed on your card.",
    "Email": "Do not open links or attachments. Mark the email as phishing and delete it.",
    "Chat": "Do not send money or codes. Block and report the account.",
    "Link": "Do not open this link. If you already did, do not enter any details and change your passwords.",
}

ss = st.session_state
for k, v in {"channel": "SMS", "msg": "", "sender": "", "checked": False, "force": False}.items():
    ss.setdefault(k, v)


# ---- callbacks (they run before the page redraws) ----
def load_example(i):
    _, ch, text, sender = SAMPLES[i]
    ss.channel, ss.msg, ss.sender, ss.checked, ss.force = ch, text, sender, True, False


def switch_tab(ch):
    ss.channel, ss.force = ch, False


def check_anyway():
    ss.force = True


def do_check():
    ss.checked, ss.force = True, False


def clear_all():
    ss.msg, ss.sender, ss.checked, ss.force = "", "", False, False


# ---- page ----
st.title("🛡️ Multilingual Spam Shield")
st.write("Paste an SMS, call transcript, email or chat message in English, Hindi or Telugu. "
         "The app finds the language, turns the text into word patterns, and shows how risky it is.")

st.radio("Message type", list(CH), key="channel", horizontal=True,
         format_func=lambda k: f"{CH[k][0]} {k}")
if ss.channel == "Email":
    st.text_input("Sender email (optional)", key="sender", placeholder="e.g. alert@bank-help.xyz")
st.text_area("Message", key="msg", height=150, placeholder="Paste here…")
st.caption(CH[ss.channel][1])

c1, c2, _ = st.columns([1, 1, 3])
c1.button("Check message", type="primary", on_click=do_check)
c2.button("Clear", on_click=clear_all)

st.caption("Try an example:")
cols = st.columns(4)
for i, s in enumerate(SAMPLES):
    cols[i % 4].button(s[0], key=f"ex{i}", on_click=load_example, args=(i,), use_container_width=True)

st.divider()

if not ss.checked:
    st.info("Your result will appear here. Type a message and press **Check message**.")
else:
    res = check(ss.msg, ss.channel, ss.sender, ss.force)
    status = res["status"]
    if status == "empty":
        st.info("Type or paste a message first, then press Check message.")
    elif status == "error":
        st.error(f"**{res['title']}**\n\n{res['msg']}")
    elif status == "redirect":
        st.warning(f"**{res['title']}**\n\n{res['msg']}")
        cols = st.columns(len(res["targets"]) + (1 if res["anyway"] else 0))
        for i, t in enumerate(res["targets"]):
            cols[i].button(f"Check in {t} tab", key=f"go{t}", type="primary", on_click=switch_tab, args=(t,))
        if res["anyway"]:
            cols[-1].button("Check here anyway", on_click=check_anyway)
    else:
        pct = int(res["p"] * 100 + 0.5)
        if pct < 35:
            verdict, colour = "🟢 Safe", "green"
            advice = ("No warning signs found in this address. Still, only open links from people you trust."
                      if ss.channel == "Link" else "No common scam patterns found. Stay careful with unknown senders.")
        elif pct < 65:
            verdict, colour = "🟡 Suspicious", "orange"
            advice = "Some risky patterns found. Check with the sender through an official channel before you click or reply."
        else:
            verdict, colour = "🔴 Spam / scam", "red"
            advice = ADVICE[ss.channel]
        st.markdown(f"## :{colour}[{verdict}]")
        st.caption(f"{CH[ss.channel][0]} {ss.channel} · Language: **{res['lang']}** · Risk: **{pct}%**")
        st.progress(pct / 100)
        st.write(advice)
        st.caption(res["note"])

        def chips(items):
            return " ".join(f"`{x}`" for x in items) if items else "_None_"

        if ss.channel == "Link":
            st.markdown("**Link check**")
            for l in res["links"]:
                st.markdown(f"`{l['host']}`  \n" + chips([c[0] for c in l["checks"]]))
        st.markdown("**Detected patterns**")
        st.markdown(chips(res["sig"]))
        st.markdown("**Top spam n-grams**")
        st.markdown(chips(res["top"]))
        st.markdown("**Shared representation (cross-lingual tokens)**")
        st.code(" ".join(res["toks"]), language=None)

with st.expander("How it works"):
    st.markdown(
        "1. **Language**: found from the Unicode script (Telugu, Devanagari/Hindi, Latin/English).\n"
        "2. **Cross-lingual step**: words with the same meaning in all three languages (OTP, block, prize, click…) "
        "are mapped to one shared concept token.\n"
        "3. **N-grams**: single words, word pairs and word triples are taken from the shared tokens.\n"
        "4. **Scoring**: counts from spam and normal training messages give a log-odds score (add-one smoothing). "
        "Rule signals add a small boost.\n"
        "5. **Channels**: each tab has its own rules. SMS weighs links more, Call weighs OTP requests more, "
        "Email checks the sender address, Chat flags money requests, Link inspects the web address.\n"
        "6. **Result**: Safe under 35%, Suspicious 35–65%, Spam above 65%."
    )
