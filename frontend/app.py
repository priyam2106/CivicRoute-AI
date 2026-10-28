import html
import requests
import pandas as pd
import streamlit as st

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="CivicRoute AI | Smart City Dashboard",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primary: #155eef;
        --primary-dark: #1047b8;
        --navy: #101828;
        --muted: #667085;
        --border: #e4e7ec;
        --background: #f5f8fc;
        --cyan: #06b6d4;
        --green: #12b76a;
    }

    .stApp {
        background: var(--background);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] { background: transparent; }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    [data-testid="stSidebar"] {
        background: #101828;
        border-right: 1px solid #26334b;
    }

    [data-testid="stSidebar"] * { color: #eaf0ff; }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 7px 4px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 0 25px 0;
    }

    .brand-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #155eef, #06b6d4);
        border-radius: 15px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 25px;
    }

    .brand-name {
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
    }

    .brand-subtitle {
        font-size: 11px;
        color: #aab8d0;
        margin-top: 3px;
    }

    .sidebar-label {
        color: #98a9c7;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin: 12px 0 10px 0;
    }

    .sidebar-note {
        background: #1c2940;
        border: 1px solid #34445f;
        padding: 16px;
        border-radius: 14px;
        margin-top: 35px;
        color: #eaf0ff;
        font-size: 12px;
        line-height: 1.7;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 38px;
        border-radius: 24px;
        background: linear-gradient(115deg, #102a56 0%, #155eef 65%, #087eaa 100%);
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 12px 35px rgba(21, 94, 239, 0.15);
    }

    .hero::after {
        content: "🏙️";
        position: absolute;
        right: 7%;
        top: 20px;
        font-size: 100px;
        opacity: 0.20;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 30px;
        padding: 7px 13px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .hero h1 {
        color: white;
        font-size: clamp(28px, 4vw, 42px);
        line-height: 1.2;
        font-weight: 800;
        letter-spacing: -1.4px;
        margin: 0 0 14px 0;
        max-width: 650px;
    }

    .hero p {
        color: #e0eaff;
        font-size: 15px;
        line-height: 1.8;
        max-width: 600px;
        margin-bottom: 0;
    }

    .section-title {
        color: #101828;
        font-size: 23px;
        font-weight: 800;
        letter-spacing: -0.6px;
        margin-top: 14px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #667085;
        font-size: 13px;
        margin-bottom: 22px;
    }

    .metric-card {
        background: white;
        border: 1px solid #e4e7ec;
        border-radius: 18px;
        padding: 22px;
        min-height: 145px;
        box-shadow: 0 3px 10px rgba(16, 24, 40, 0.025);
    }

    .metric-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 17px;
    }

    .metric-label {
        color: #667085;
        font-size: 12px;
        font-weight: 600;
    }

    .metric-icon {
        width: 39px;
        height: 39px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }

    .metric-value {
        color: #101828;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .metric-caption {
        color: #667085;
        font-size: 11px;
        margin-top: 5px;
    }

    .panel {
        background: white;
        border: 1px solid #e4e7ec;
        border-radius: 18px;
        padding: 25px;
        margin-top: 22px;
        margin-bottom: 18px;
    }

    .panel-heading {
        color: #101828;
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .panel-description {
        color: #667085;
        font-size: 12px;
        line-height: 1.8;
    }

    .feature-card {
        background: white;
        border: 1px solid #e4e7ec;
        border-radius: 17px;
        padding: 22px;
        height: 100%;
    }

    .feature-icon { font-size: 28px; margin-bottom: 15px; }

    .feature-title {
        color: #101828;
        font-weight: 750;
        font-size: 15px;
        margin-bottom: 9px;
    }

    .feature-text {
        color: #667085;
        font-size: 12px;
        line-height: 1.8;
    }

    .ai-card {
        background: linear-gradient(135deg, #eff6ff, #f0fdff);
        border: 1px solid #c7ddff;
        border-radius: 18px;
        padding: 22px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .ai-card-title {
        color: #1047b8;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .ai-card-description {
        color: #475467;
        font-size: 12px;
        line-height: 1.8;
    }

    .sidebar-note strong { color: #ffffff; }

    .footer {
        border-top: 1px solid #e4e7ec;
        padding-top: 20px;
        margin-top: 40px;
        color: #98a2b3;
        font-size: 11px;
        text-align: center;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 650;
        min-height: 43px;
        transition: all 0.2s ease;
    }

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button {
        background: #155eef;
        color: white;
        border: 1px solid #155eef;
    }

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {
        background: #1047b8;
        border-color: #1047b8;
        color: white;
        box-shadow: 0 5px 15px rgba(21, 94, 239, 0.2);
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        border-radius: 10px;
    }

    div[data-testid="stSelectbox"] > div > div { border-radius: 10px; }
    hr { border-color: #e4e7ec; }

    @media (max-width: 768px) {
        .hero { padding: 25px; }
        .hero::after { font-size: 55px; right: 5%; top: 10px; }
        .metric-card { padding: 16px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# API HELPERS
# --------------------------------------------------
def api_get_reports():
    response = requests.get(f"{API_URL}/reports", timeout=10)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict):
        data = data.get("reports", [])

    return data if isinstance(data, list) else []


def api_is_online():
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.ok
    except requests.RequestException:
        return False


def display_metric(label, value, icon, color, caption):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <span class="metric-label">{html.escape(str(label))}</span>
                <div class="metric-icon" style="background:{color}18;">
                    {icon}
                </div>
            </div>
            <div class="metric-value">{html.escape(str(value))}</div>
            <div class="metric-caption">{html.escape(str(caption))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title, subtitle=None):
    st.markdown(
        f'<div class="section-title">{html.escape(title)}</div>',
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(
            f'<div class="section-subtitle">{html.escape(subtitle)}</div>',
            unsafe_allow_html=True,
        )


def go_to_page(target_page):
    """Change the sidebar radio's value and rerun the Streamlit app."""
    st.session_state["navigation_target"] = target_page
    st.rerun()


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
PAGE_OPTIONS = ["Dashboard", "Submit Complaint", "View Reports", "About Project"]

if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🛣️</div>
            <div>
                <div class="brand-name">CivicRoute AI</div>
                <div class="brand-subtitle">SMART CITY INTELLIGENCE</div>
            </div>
        </div>
        <div class="sidebar-label">WORKSPACE</div>
        """,
        unsafe_allow_html=True,
    )

    PAGES = [
    "Dashboard",
    "Submit Complaint",
    "View Reports",
    "About Project",
    ]

    if "page" not in st.session_state:
        st.session_state["page"] = "Dashboard"

    if "navigation_target" not in st.session_state:
        st.session_state["navigation_target"] = None

    # Apply navigation requests before creating the radio widget.
    target = st.session_state["navigation_target"]

    if target in PAGES:
        st.session_state["page"] = target
        st.session_state["navigation_target"] = None

    st.radio(
        "Navigate",
        PAGES,
        key="page",
        label_visibility="collapsed",
    )

    st.markdown("---")
    online = api_is_online()

    if online:
        st.success("Backend connected")
    else:
        st.error("Backend disconnected")

    st.caption("API: 127.0.0.1:8000")

    st.markdown(
        """
        <div class="sidebar-note">
            <strong>💡 Civic intelligence</strong><br><br>
            Helping communities report road hazards and helping
            authorities organize maintenance priorities.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Always read the current value after rendering the radio.
page = st.session_state["page"]

# --------------------------------------------------
# FETCH REPORTS
# --------------------------------------------------
try:
    reports = api_get_reports()
    reports_error = None
except requests.RequestException as error:
    reports = []
    reports_error = str(error)

total_reports = len(reports)
pending_reports = sum(
    1 for report in reports
    if str(report.get("status", "")).upper()
    in ["PENDING", "OPEN", "SUBMITTED"]
)
resolved_reports = sum(
    1 for report in reports
    if str(report.get("status", "")).upper() in ["RESOLVED", "CLOSED"]
)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
if page == "Dashboard":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">✦ AI-POWERED CIVIC INTELLIGENCE</div>
            <h1>Building safer roads.<br>Creating smarter cities.</h1>
            <p>
                Transform citizen complaints into actionable road
                maintenance insights. Report hazards, organize issues,
                and support smarter infrastructure decisions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_title(
        "Overview",
        "A snapshot of complaints registered in the system.",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        display_metric("Total complaints", total_reports, "📋", "#155eef",
                       "All registered reports")
    with c2:
        display_metric("Pending review", pending_reports, "⏳", "#f79009",
                       "Awaiting further action")
    with c3:
        display_metric("Resolved reports", resolved_reports, "✓", "#12b76a",
                       "Marked resolved or closed")
    with c4:
        display_metric("AI-assisted reports", total_reports, "🤖", "#06b6d4",
                       "Reports submitted to the system")

    section_title(
        "Get started",
        "Choose an action to continue working with CivicRoute AI.",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <div class="feature-title">Report an issue</div>
                <div class="feature-text">
                    Submit potholes, flooding, damaged roads, broken traffic
                    signals, and other civic issues.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Submit a complaint →",
            key="dashboard_submit",
            width="stretch",
            on_click=go_to_page,
            args=("Submit Complaint",),
        ):
            pass
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Explore reports</div>
                <div class="feature-text">
                    Review registered complaints, inspect their locations,
                    and monitor their current statuses.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "View reports →",
            key="dashboard_reports",
            width="stretch",
            on_click=go_to_page,
            args=("View Reports",),
        ):
            pass

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI-assisted analysis</div>
                <div class="feature-text">
                    Organize complaint information with predicted categories,
                    urgency levels, and recommendations.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Learn about the AI →",
            key="dashboard_about",
            width="stretch",
            on_click=go_to_page,
            args=("About Project",),
        ):
            pass

    st.markdown(
        """
        <div class="footer">
            CivicRoute AI · Smart Cities, IoT & Transportation<br>
            AI recommendations are advisory and require human review.
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# SUBMIT COMPLAINT
# --------------------------------------------------
elif page == "Submit Complaint":
    section_title(
        "Submit a complaint",
        "Tell us about a road or transportation issue in your area. "
        "The system will record your report and request an analysis.",
    )

    left, right = st.columns([1.7, 1])

    with left:
        st.markdown(
            '<div class="panel-heading">📍 Complaint details</div>',
            unsafe_allow_html=True,
        )
        st.caption("Fields marked with * are required.")

        with st.form("complaint_form", clear_on_submit=False):
            category = st.selectbox(
                "Issue category *",
                [
                    "pothole", "road_damage", "open_manhole", "flooding",
                    "traffic_signal", "signage", "debris", "drainage",
                    "public_transport", "other",
                ],
                format_func=lambda x: x.replace("_", " ").title(),
            )
            location = st.text_input(
                "Location or area *",
                placeholder="e.g., Shankar Nagar, Raipur",
            )
            description = st.text_area(
                "Describe the issue *",
                placeholder=(
                    "What happened? Where is the hazard? "
                    "Does it affect pedestrians or vehicles?"
                ),
                height=180,
                max_chars=3000,
            )
            st.caption(
                f"Description length: {len(description)} / 3000 characters"
            )
            submitted = st.form_submit_button(
                "🚀 Submit complaint",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            if not online:
                st.error(
                    "The backend is offline. Start FastAPI in another "
                    "terminal before submitting your complaint."
                )
            elif not location.strip():
                st.warning("Please enter the location of the issue.")
            elif not 5 <= len(description.strip()) <= 3000:
                st.warning(
                    "Your description must contain between 5 and 3000 characters."
                )
            else:
                payload = {
                    "category": category,
                    "location_zone": location.strip(),
                    "description": description.strip(),
                }

                try:
                    with st.spinner(
                        "Submitting complaint and requesting analysis..."
                    ):
                        response = requests.post(
                            f"{API_URL}/reports",
                            json=payload,
                            timeout=30,
                        )

                    if not response.ok:
                        st.error(
                            f"Backend returned HTTP {response.status_code}."
                        )
                        st.code(response.text[:1500])
                    else:
                        try:
                            result = response.json()
                        except ValueError:
                            result = {}

                        st.success("Complaint submitted successfully!")
                        report_id = result.get(
                            "report_id", result.get("id", "See reports")
                        )
                        status = result.get("status", "PENDING")

                        st.markdown(
                            f"""
                            <div class="ai-card">
                                <div class="ai-card-title">✓ Complaint registered</div>
                                <div class="ai-card-description">
                                    Complaint ID: <strong>{html.escape(str(report_id))}</strong><br>
                                    Current status: <strong>{html.escape(str(status))}</strong>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        analysis = result.get("ai_analysis")
                        if isinstance(analysis, dict) and analysis:
                            st.markdown(
                                """
                                <div class="ai-card">
                                    <div class="ai-card-title">🤖 AI analysis</div>
                                    <div class="ai-card-description">
                                        This is an advisory analysis. A human reviewer
                                        should verify it.
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            a1, a2 = st.columns(2)
                            with a1:
                                st.metric(
                                    "Predicted category",
                                    str(analysis.get(
                                        "predicted_category", "N/A"
                                    )).replace("_", " ").title(),
                                )
                            with a2:
                                st.metric(
                                    "Urgency (1–5)",
                                    analysis.get("urgency", "N/A"),
                                )

                            st.markdown("#### Severity")
                            st.write(analysis.get("severity", "Not available"))
                            st.markdown("#### Summary")
                            st.write(analysis.get("summary", "Not available"))
                            st.markdown("#### Recommended action")
                            st.info(
                                analysis.get(
                                    "recommended_action",
                                    "No recommendation provided.",
                                )
                            )
                            st.caption(
                                "Analysis is not a confirmed assessment of "
                                "real-world danger."
                            )
                        else:
                            st.info(
                                "The complaint was submitted, but the backend "
                                "did not return an AI analysis."
                            )

                        st.cache_data.clear()

                except requests.RequestException as error:
                    st.error("Could not submit the complaint.")
                    st.caption(str(error))

    with right:
        st.markdown(
            """
            <div class="panel">
                <div class="panel-heading">💡 Reporting tips</div><br>
                <div class="panel-description">
                    <strong>Be specific</strong><br>
                    Describe the problem clearly.<br><br>
                    <strong>Include the location</strong><br>
                    Mention the street, area, or nearby landmark.<br><br>
                    <strong>Explain the impact</strong><br>
                    Describe how the issue affects traffic or safety.<br><br>
                    <strong>AI-assisted review</strong><br>
                    Recommendations are advisory and should be reviewed
                    by a responsible human.
                </div>
            </div>
            <div class="panel">
                <div class="panel-heading">🛡️ Your report matters</div><br>
                <div class="panel-description">
                    Citizen reports can help organize infrastructure
                    problems and support better maintenance planning.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --------------------------------------------------
# VIEW REPORTS
# --------------------------------------------------
elif page == "View Reports":
    section_title(
        "Complaint management",
        "Explore registered complaints and their current status.",
    )

    if st.button("🔄 Refresh reports", key="refresh_reports"):
        st.rerun()

    if not online:
        st.error(
            "Backend is disconnected. Start FastAPI to load the reports."
        )
    elif reports_error:
        st.error("Could not load reports from the backend.")
        st.caption(reports_error)
    elif not reports:
        st.info(
            "No reports were returned by the backend. Submit a complaint "
            "or check the backend response."
        )
    else:
        df = pd.DataFrame(reports)

        search = st.text_input(
            "🔎 Search reports",
            placeholder=(
                "Search by location, category, description, or status..."
            ),
        )

        if search.strip():
            mask = df.astype(str).apply(
                lambda col: col.str.contains(
                    search.strip(), case=False, na=False, regex=False
                )
            ).any(axis=1)
            df = df[mask]

        if "status" in df.columns:
            statuses = sorted(
                df["status"].dropna().astype(str).unique().tolist()
            )
            selected_statuses = st.multiselect(
                "Filter by status",
                statuses,
                default=statuses,
            )
            df = df[df["status"].astype(str).isin(selected_statuses)]

        st.caption(f"Showing {len(df)} complaint(s)")
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Export reports as CSV",
            data=csv_data,
            file_name="civicroute_reports.csv",
            mime="text/csv",
        )

# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------
elif page == "About Project":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">SMART CITIES · TRANSPORTATION</div>
            <h1>Technology for better roads.</h1>
            <p>
                CivicRoute AI organizes citizen complaints and uses
                AI-assisted analysis to support more informed road
                maintenance decisions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_title("Project capabilities")
    a, b, c = st.columns(3)

    with a:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <div class="feature-title">Citizen reporting</div>
                <div class="feature-text">
                    Collect road and transport complaints with location
                    and description details.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI-assisted classification</div>
                <div class="feature-text">
                    Estimate complaint categories, urgency, summaries,
                    and suggested first actions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Report monitoring</div>
                <div class="feature-text">
                    Display registered complaints and help users
                    organize and review information.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="panel">
            <div class="panel-heading">Technology stack</div><br>
            <div class="panel-description">
                <strong>Frontend:</strong> Streamlit<br>
                <strong>Backend:</strong> FastAPI<br>
                <strong>Database:</strong> SQLite<br>
                <strong>Language:</strong> Python<br>
                <strong>AI service:</strong> Rule-based/mock analyzer unless
                connected to a real AI service
            </div>
        </div>
        <div class="panel">
            <div class="panel-heading">⚠️ Responsible AI</div><br>
            <div class="panel-description">
                AI predictions are preliminary recommendations, not verified
                facts. They require human review. Complaints should not be
                automatically dispatched, merged, or rejected solely on the
                basis of AI output.
            </div>
        </div>
        <div class="footer">CivicRoute AI · Academic project prototype</div>
        """,
        unsafe_allow_html=True,
    )
