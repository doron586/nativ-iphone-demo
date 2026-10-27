import streamlit as st

st.set_page_config(
    page_title="נתיב | הדגמת אייפון",
    page_icon="🛡️",
    layout="centered",
)

st.markdown("""
<style>
div[data-testid="stMain"] {
    direction: rtl;
    text-align: right;
    overflow-wrap: anywhere;
}
div[data-testid="stRadio"] > div {
    flex-wrap: wrap;
    gap: 0.5rem;
}
div[data-testid="stRadio"] label {
    min-height: 48px;
    padding: 0.5rem;
}
div[data-testid="stButton"] button {
    min-height: 48px;
}
@media (max-width: 600px) {
    .block-container {
        padding: 1rem 0.8rem 3rem;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ נתיב | יום העבודה שלי")
st.warning(
    "גרסת הדגמה בלבד — כל הנתונים פיקטיביים. "
    "אין חיבור למערכת האמיתית."
)

section = st.radio(
    "מעבר מהיר",
    ["לטיפול עכשיו", "משימות בהמשך", "רענונים והכשרות"],
)

if section == "לטיפול עכשיו":
    st.error("דחוף | בדיקת שער כניסה — בית ספר הדגמה א׳")
    st.warning("ליקוי פתוח | תאורה — בית ספר הדגמה ב׳")
    st.info("להיום | בדיקת תיק ביטחון — גן הדגמה ג׳")

elif section == "משימות בהמשך":
    st.info("בדיקת מצלמות — בית ספר הדגמה א׳")
    st.info("תיאום ביקור — גן הדגמה ג׳")

else:
    st.warning(
        "רענון רכז ביטחון — דוגמה בלבד, "
        "לא מועד חובה רשמי"
    )
    st.info("הכשרת רכז טיולים — פריט הדגמה בלבד")

st.divider()
st.caption(
    "תצוגת ניסיון בלבד. אין התחברות, GPS, "
    "שליחת משימות או שמירת מידע."
)

