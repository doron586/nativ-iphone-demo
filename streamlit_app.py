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

from datetime import date, timedelta

if "demo_completed" not in st.session_state:
    st.session_state.demo_completed = set()
if "demo_defects" not in st.session_state:
    st.session_state.demo_defects = {"lighting": "פתוח"}
if "demo_training" not in st.session_state:
    st.session_state.demo_training = {"security": "ממתין לביצוע", "trips": "ממתין לביצוע"}

today = date.today()
tasks = [
    {"id": "gate", "title": "בדיקת שער כניסה", "school": "בית ספר הדגמה א׳", "due": today, "urgent": True, "details": "בדיקת תקינות שער הכניסה והעברת דיווח דוגמה."},
    {"id": "file", "title": "בדיקת תיק ביטחון", "school": "גן הדגמה ג׳", "due": today - timedelta(days=2), "urgent": False, "details": "בדיקת מסמכי תיק הביטחון לדוגמה."},
    {"id": "camera", "title": "בדיקת מצלמות", "school": "בית ספר הדגמה א׳", "due": today + timedelta(days=5), "urgent": False, "details": "בדיקת מצלמות ותיעוד ממצאים פיקטיביים."},
    {"id": "visit", "title": "תיאום ביקור", "school": "גן הדגמה ג׳", "due": today + timedelta(days=9), "urgent": False, "details": "תיאום ביקור עתידי לדוגמה."},
]

st.title("🛡️ נתיב | יום העבודה שלי")
st.warning("גרסת הדגמה בלבד — כל הנתונים פיקטיביים. אין חיבור למערכת האמיתית.")
st.caption("סימון משימות נשמר זמנית בדפדפן במהלך השימוש בלבד, ולא במאגר נתונים.")

open_tasks = [t for t in tasks if t["id"] not in st.session_state.demo_completed]
st.metric("משימות פתוחות לדוגמה", len(open_tasks))

def show_task(task):
    overdue = task["due"] < today
    prefix = "דחוף" if task["urgent"] else ("באיחור" if overdue else "משימה")
    heading = f'{prefix} | {task["title"]} — {task["school"]}'
    if task["urgent"]:
        st.error(heading)
    elif overdue:
        st.warning(heading)
    else:
        st.info(heading)
    with st.expander("פרטי המשימה"):
        st.write(task["details"])
        st.caption("מועד לדוגמה: " + task["due"].strftime("%d/%m/%Y"))
        if st.button("סמן כבוצע", key="done_" + task["id"], use_container_width=True):
            st.session_state.demo_completed.add(task["id"])
            st.rerun()

section = st.radio("מעבר מהיר", ["לטיפול עכשיו", "משימות בהמשך", "ליקויים", "רענונים והכשרות"])

if section == "לטיפול עכשיו":
    due_now = [t for t in open_tasks if t["urgent"] or t["due"] <= today]
    if not due_now:
        st.success("אין משימות פתוחות לטיפול מיידי בהדגמה.")
    for task in due_now:
        show_task(task)
    if st.session_state.demo_defects["lighting"] != "טופל":
        st.warning("ליקוי לדוגמה | תאורה — בית ספר הדגמה ב׳ | " + st.session_state.demo_defects["lighting"])

elif section == "משימות בהמשך":
    future = [t for t in open_tasks if not t["urgent"] and t["due"] > today]
    if not future:
        st.success("אין משימות עתידיות פתוחות בהדגמה.")
    for task in future:
        show_task(task)

elif section == "ליקויים":
    st.subheader("מעקב ליקויים — הדגמה")
    st.warning("תאורה בחצר — בית ספר הדגמה ב׳")
    status = st.selectbox("סטטוס הטיפול", ["פתוח", "בטיפול", "טופל"], index=["פתוח", "בטיפול", "טופל"].index(st.session_state.demo_defects["lighting"]))
    if st.button("עדכן סטטוס ליקוי", use_container_width=True):
        st.session_state.demo_defects["lighting"] = status
        st.success("סטטוס הליקוי עודכן בהדגמה בלבד.")
    st.caption("אין דיווח למנהל ואין שמירה במסד נתונים.")

else:
    st.subheader("רענונים והכשרות — הדגמה")
    st.caption("המועדים והחובות אינם מבוססים על חוזרי מנכ״ל. אין כאן אימות אסמכתאות אמיתי.")
    for key, title in [("security", "רענון רכז ביטחון"), ("trips", "הכשרת רכז טיולים")]:
        with st.expander(title + " — " + st.session_state.demo_training[key]):
            st.write("סטטוס נוכחי: " + st.session_state.demo_training[key])
            if st.session_state.demo_training[key] == "ממתין לביצוע":
                if st.button("סמן שבוצע — ממתין לאימות", key="training_" + key, use_container_width=True):
                    st.session_state.demo_training[key] = "ממתין לאימות אסמכתה"
                    st.rerun()
            else:
                st.warning("נדרש אימות אסמכתה על ידי גורם מוסמך. אין אישור אוטומטי.")

if st.session_state.demo_completed:
    with st.expander("משימות שסומנו כבוצעו בהדגמה"):
        for task in tasks:
            if task["id"] in st.session_state.demo_completed:
                st.success(task["title"] + " — " + task["school"])
        if st.button("אפס נתוני הדגמה", use_container_width=True):
            st.session_state.demo_completed.clear()
            st.session_state.demo_defects = {"lighting": "פתוח"}
            st.session_state.demo_training = {"security": "ממתין לביצוע", "trips": "ממתין לביצוע"}
            st.rerun()

st.divider()
st.caption("אין התחברות, GPS, התראות דחיפה, שליחת משימות או שמירת מידע קבועה.")
