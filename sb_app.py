"""
SchoolsBuddy Activity Fetcher
Run: python3 -m streamlit run sb_app.py
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date, timezone, timedelta

# ── CONFIG ───────────────────────────────────────────────────
DEFAULT_CLIENT_ID     = "ian"
DEFAULT_CLIENT_SECRET = ""
DEFAULT_ORG_ID        = "297"
AUTH_URL  = "https://accounts2.schoolsbuddy.net/connect/token"
BASE_URL  = "https://publicapi-asia.schoolsbuddy.net"
LOGO_B64  = "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"
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SchoolsBuddy Activity Fetcher",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

[data-testid="stAppViewContainer"] { background: #f5f3fb; }
[data-testid="stHeader"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

[data-testid="stSidebar"] {
    background: #3b1a5e !important;
    min-width: 270px !important;
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.9) !important; }
[data-testid="stSidebar"] input {
    background: white !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 8px !important;
    color: #1a1a1a !important;
}
[data-testid="stSidebar"] input::placeholder { color: #aaaaaa !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #d4489a, #7c3abf) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 0.55rem 1rem !important;
    width: 100% !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.87 !important; }
.stButton > button:not([kind="primary"]) {
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 8px !important;
    width: 100% !important;
}

[data-testid="metric-container"] {
    background: white !important;
    border: 1px solid #e2daf2 !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
}
[data-testid="stMetricLabel"] p { color: #8b75b8 !important; font-size: 12px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.06em !important; }
[data-testid="stMetricValue"] { color: #3b1a5e !important; font-weight: 700 !important; }

[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    border: 1px solid #e2daf2 !important;
    overflow: hidden !important;
}

.stTextInput label { color: #3b1a5e !important; font-weight: 600 !important; font-size: 13px !important; }
.stTextInput input { border: 1.5px solid #d6cef0 !important; border-radius: 8px !important; }
.stTextInput input:focus { border-color: #7c3abf !important; box-shadow: 0 0 0 3px rgba(124,58,191,0.1) !important; }

[data-testid="stDownloadButton"] button {
    background: #3b1a5e !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.stProgress > div > div { background: linear-gradient(90deg, #7c3abf, #d4489a) !important; border-radius: 99px !important; }
hr { border-color: #e2daf2 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1.25rem 0 1rem; border-bottom: 1px solid rgba(255,255,255,0.15); margin-bottom: 1rem; text-align: center;">
        <img src="data:image/png;base64,{LOGO_B64}" style="width: 64px; height: 64px; border-radius: 50%;" />
        <p style="font-size: 16px; font-weight: 700; color: white; margin: 8px 0 2px;">SchoolsBuddy</p>
        <p style="font-size: 11px; color: rgba(255,255,255,0.5); margin: 0; text-transform: uppercase; letter-spacing: 0.08em;">Activity Fetcher</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**API Settings**")
    client_id     = st.text_input("Client ID",       value=DEFAULT_CLIENT_ID)
    client_secret = st.text_input("Client Secret",   type="password", value=DEFAULT_CLIENT_SECRET)
    org_id        = st.text_input("Organisation ID", value=DEFAULT_ORG_ID)

    st.divider()
    st.markdown("**Search**")
    mode = st.radio("Fetch Mode", ["All Students", "Specific Students"])
    student_search_input = ""
    if mode == "Specific Students":
        student_search_input = st.text_input("Last Name or Email", placeholder="e.g. Disney or ian+flynn@...")

    st.divider()
    st.markdown("**Date Range** *(required)*")
    today      = date.today()
    start_date = st.date_input("From", value=today)
    end_date   = st.date_input("To",   value=today)

    st.divider()
    fetch_btn = st.button("Fetch Activities", type="primary")
    stop_btn  = st.button("⛔  Stop")
    if stop_btn:
        st.session_state["stop"] = True

# ── Page header ───────────────────────────────────────────────
st.markdown("""
<div style="background: white; border-radius: 14px; border: 1px solid #e2daf2; padding: 1.25rem 1.75rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem;">
    <div style="background: linear-gradient(135deg, #d4489a, #7c3abf); border-radius: 12px; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0;">🎓</div>
    <div>
        <p style="font-size: 20px; font-weight: 700; color: #3b1a5e; margin: 0;">Activity Fetcher</p>
        <p style="font-size: 13px; color: #8b75b8; margin: 0;">Pull student CCA activities and parent contacts from SchoolsBuddy</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────
def get_token(cid, csecret):
    resp = requests.post(AUTH_URL, data={
        "grant_type": "client_credentials",
        "client_id": cid,
        "client_secret": csecret,
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

def api_get(token, path, params=None):
    resp = requests.get(
        f"{BASE_URL}{path}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
    )
    resp.raise_for_status()
    return resp.json()

def fetch_all_pages(token, path, base_params=None):
    results, page = [], 1
    while True:
        params = {**(base_params or {}), "PageNumber": page, "PageSize": 100}
        data   = api_get(token, path, params)
        results.extend(data.get("data") or [])
        if page >= (data.get("totalPages") or 1):
            break
        page += 1
    return results

def fetch_events(token, sc_student_id, org_id, start_date, end_date):
    params = {
        "SCStudentId":      sc_student_id,
        "PageSize":         200,
        "IsArchived":       False,
        "IsCancelled":      False,
        "IncludeAttendees": True,
        "StartDateTime":    f"{start_date}T00:00:00Z",
        "EndDateTime":      f"{end_date}T23:59:59Z",
    }
    if org_id: params["OrganisationIds"] = org_id
    data   = api_get(token, "/api/v1/Events", params)
    events = data.get("data") or []
    active = []
    for ev in events:
        attendees = ev.get("attendees") or []
        if any(str(a.get("id")) == str(sc_student_id) for a in attendees):
            active.append(ev)
    return active

def fetch_parent_emails(token, related_ids):
    emails = []
    for cid in (related_ids or []):
        try:
            c = api_get(token, f"/api/v1/Contacts/{cid}")
            if c.get("emailAddress"):
                emails.append(c["emailAddress"])
        except Exception:
            pass
    return emails

WEEKDAYS  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
TZ_UTC    = timezone(timedelta(0))
TZ_PLUS8  = timezone(timedelta(hours=8))

def to_plus8(dt_str):
    if not dt_str: return None
    try:
        clean  = dt_str.replace("Z","").split("+")[0]
        dt_utc = datetime.fromisoformat(clean).replace(tzinfo=TZ_UTC)
        return dt_utc.astimezone(TZ_PLUS8)
    except Exception:
        return None

def fmt_time(dt_str):
    dt = to_plus8(dt_str)
    return dt.strftime("%H:%M") if dt else ""

def fmt_weekday(dt_str):
    dt = to_plus8(dt_str)
    return WEEKDAYS[dt.weekday()] if dt else ""


# ── Fetch logic ───────────────────────────────────────────────
if fetch_btn:
    st.session_state["stop"]    = False
    st.session_state["fetched"] = False

    if not client_id or not client_secret:
        st.error("Please enter your Client ID and Client Secret.")
        st.stop()

    if start_date > end_date:
        st.error("'From' date must be before 'To' date.")
        st.stop()

    with st.spinner("Authenticating..."):
        try:
            token = get_token(client_id, client_secret)
        except Exception as e:
            st.error(f"Authentication failed: {e}")
            st.stop()

    with st.spinner("Fetching students..."):
        try:
            if mode == "Specific Students":
                query = student_search_input.strip()
                if not query:
                    st.error("Please enter a last name or email to search.")
                    st.stop()
                params = {"Search": query, "PageSize": 50}
                if org_id: params["OrganisationIds"] = org_id
                data     = api_get(token, "/api/v1/Students", params)
                students = data.get("data") or []
                if not students:
                    st.warning(f"No students found matching: **{query}**")
                    st.stop()
            else:
                params = {}
                if org_id: params["OrganisationIds"] = org_id
                students = fetch_all_pages(token, "/api/v1/Students", params)
        except Exception as e:
            st.error(f"Failed to fetch students: {e}")
            st.stop()

    st.info(f"Found **{len(students)}** student(s) — fetching activities and parent info...")

    rows        = []
    progress    = st.progress(0)
    status_text = st.empty()

    for i, student in enumerate(students):
        sc_id    = student.get("id")
        first    = student.get("firstName", "")
        last     = student.get("lastName", "")
        grade    = student.get("grade", "")
        homeroom = student.get("homeroomClass", "")
        email    = student.get("email", "")
        related  = student.get("relatedPeople") or []

        status_text.text(f"Processing {i+1}/{len(students)}: {first} {last}")

        if st.session_state.get("stop"):
            status_text.warning(f"⛔ Stopped after processing {i} student(s).")
            break

        try:
            events = fetch_events(token, sc_id, org_id, start_date, end_date)
        except Exception:
            events = []

        try:
            parent_emails = fetch_parent_emails(token, related)
        except Exception:
            parent_emails = []

        parent_str = "; ".join(parent_emails)

        if not events:
            rows.append({
                "First Name":      first,
                "Last Name":       last,
                "Student Email":   email,
                "Grade":           grade,
                "Homeroom":        homeroom,
                "Parent Email(s)": parent_str,
                "Activity Name":   "(Pending Group API)",
                "Event Type":      "",
                "Day":             "",
                "Day Order":       99,
                "Start Time":      "",
                "End Time":        "",
                "Location":        "",
                "Teacher":         "",
            })
        else:
            for ev in events:
                day_str   = fmt_weekday(ev.get("eventStartTime"))
                day_order = WEEKDAYS.index(day_str) if day_str in WEEKDAYS else 99
                rows.append({
                    "First Name":      first,
                    "Last Name":       last,
                    "Student Email":   email,
                    "Grade":           grade,
                    "Homeroom":        homeroom,
                    "Parent Email(s)": parent_str,
                    "Activity Name":   "(Pending Group API)",
                    "Event Type":      ev.get("eventName", ""),
                    "Day":             day_str,
                    "Day Order":       day_order,
                    "Start Time":      fmt_time(ev.get("eventStartTime")),
                    "End Time":        fmt_time(ev.get("eventEndTime")),
                    "Location":        ev.get("location") or ev.get("meetingLocation") or "",
                    "Teacher":         ev.get("leadStaffMember", ""),
                })

        progress.progress((i + 1) / len(students))

    status_text.empty()
    progress.empty()

    df = pd.DataFrame(rows)
    st.session_state["df"]      = df
    st.session_state["fetched"] = True


# ── Results ───────────────────────────────────────────────────
if st.session_state.get("fetched") and "df" in st.session_state:
    df = st.session_state["df"]

    total_students = df["Student Email"].nunique()
    total_events   = len(df[df["Start Time"] != ""])

    col1, col2 = st.columns(2)
    col1.metric("Students", total_students)
    col2.metric("Activities Found", total_events)

    st.divider()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        search_first = st.text_input("🔎 First Name", placeholder="e.g. Flynn")
    with col_b:
        search_last  = st.text_input("🔎 Last Name",  placeholder="e.g. Disney")
    with col_c:
        search_email = st.text_input("✉️ Student Email", placeholder="e.g. ian+flynn@schoolsbuddy.com")

    filtered = df.copy()
    if search_first:
        filtered = filtered[filtered["First Name"].str.contains(search_first, case=False, na=False)]
    if search_last:
        filtered = filtered[filtered["Last Name"].str.contains(search_last, case=False, na=False)]
    if search_email:
        filtered = filtered[filtered["Student Email"].str.contains(search_email, case=False, na=False)]

    filtered = filtered.sort_values("Day Order").drop(columns=["Day Order"])
    st.dataframe(filtered, use_container_width=True, hide_index=True, height=500)

    st.divider()

    export_df = df.drop(columns=["Day Order"])
    csv = export_df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="⬇️ Export to CSV",
        data=csv,
        file_name=f"sb_activities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )
    st.caption("⚠️ 'Activity Name' will be populated once the Group API is available.")
