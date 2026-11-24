from pathlib import Path
import streamlit as st
import requests

# --------------------------------
# CONFIGURATION
# --------------------------------

API_URL = "http://127.0.0.1:8000"


# --------------------------------
# PERSISTENT DATASET FILE LOOKUP
# --------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "backend" / "data"


def get_latest_dataset_filename(dataset_type):
    """Return the newest CSV filename saved by the backend."""
    dataset_folder = DATA_DIR / dataset_type

    if not dataset_folder.exists():
        return None

    csv_files = list(dataset_folder.glob("*.csv"))

    if not csv_files:
        return None

    newest_file = max(csv_files, key=lambda file: file.stat().st_mtime)
    return newest_file.name


st.set_page_config(
    page_title="DriftShield",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# CUSTOM DESIGN
# --------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #050505;
    color: #FFFFFF;
}

[data-testid="stSidebar"] {
    background-color: #080808;
    border-right: 1px solid #242424;
}

h1, h2, h3 {
    color: #FF6B22 !important;
}

p, label, span {
    color: #A0A0A0;
}

.metric-box {
    background: #0B0B0B;
    border: 1px solid #242424;
    padding: 22px;
    min-height: 120px;
}

.metric-label {
    color: #A0A0A0;
    font-size: 13px;
    letter-spacing: 1px;
}

.metric-value {
    color: #FF6B22;
    font-size: 32px;
    font-weight: 700;
    margin-top: 10px;
}

.section-line {
    border-top: 1px solid #242424;
    margin: 25px 0;
}

.stButton > button {
    background-color: #FF6B22;
    color: #050505;
    border: none;
    border-radius: 2px;
    font-weight: 700;
}

.stButton > button:hover {
    background-color: #FF854A;
    color: #050505;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# API CONNECTION
# --------------------------------

def api_get(endpoint):

    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=5
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return None


# --------------------------------
# SIDEBAR NAVIGATION
# --------------------------------

st.sidebar.markdown("# ◈ DRIFTSHIELD")

st.sidebar.caption("MODEL MONITORING PLATFORM")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Projects",
        "Data Ingestion",
        "Drift Monitor",
        "Alerts",
        "Monitoring History",
        "Reports"
    ]
)

st.sidebar.markdown("---")

health = api_get("/health")

if health:
    st.sidebar.success("SYSTEM ONLINE")
else:
    st.sidebar.error("BACKEND OFFLINE")

st.sidebar.caption("DRIFTSHIELD · VERSION 1.0")


# --------------------------------
# OVERVIEW PAGE
# --------------------------------

if page == "Overview":

    st.markdown("# DRIFTSHIELD")
    st.caption("DETECT THE DRIFT. PROTECT THE PERFORMANCE.")

    st.markdown(
        '<div class="section-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown("### MONITORING OVERVIEW")

    history = api_get("/monitoring/history")
    alerts = api_get("/alerts/")
    projects = api_get("/projects/")

    total_runs = history.get("total_runs", 0) if history else 0

    total_alerts = alerts.get("total_alerts", 0) if alerts else 0

    total_projects = (
        len(projects) if isinstance(projects, list) else
        projects.get("total_projects", 0) if projects else 0
    )

    if history:
        runs = history.get("history", [])
        drifted_runs = sum(
            1 for run in runs
            if run.get("status") == "Drift Detected"
        )
    else:
        drifted_runs = 0

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "MONITORING RUNS", total_runs),
        (col2, "DRIFT DETECTED", drifted_runs),
        (col3, "TOTAL ALERTS", total_alerts),
        (col4, "PROJECTS", total_projects)
    ]

    for column, label, value in metrics:

        with column:

            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="section-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown("### LATEST MONITORING ACTIVITY")

    if history and history.get("history"):

        recent_runs = history["history"][:5]

        for run in recent_runs:

            st.write(
                f"Run #{run['run_id']}  |  "
                f"{run['status']}  |  "
                f"Drifted features: {run['drifted_features']}"
            )

    else:
        st.info("No monitoring activity available yet.")

    st.markdown(
        '<div class="section-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown("### SYSTEM INFORMATION")

    if health:

        st.success(
            f"Backend connected: {health.get('application', 'DriftShield')}"
        )

    else:

        st.error(
            "Cannot connect to FastAPI. Make sure the backend is running."
        )


# --------------------------------
# OTHER PAGE PLACEHOLDERS
# --------------------------------

elif page == "Projects":

    st.markdown("# PROJECT MANAGEMENT")
    st.caption("CREATE · ORGANIZE · CONTROL YOUR MONITORING PROJECTS")

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    # CREATE PROJECT
    st.markdown("### + CREATE NEW PROJECT")

    with st.form("create_project_form"):

        project_name = st.text_input(
            "PROJECT NAME",
            placeholder="e.g. Customer Behaviour Monitoring"
        )

        project_description = st.text_area(
            "PROJECT DESCRIPTION",
            placeholder="Describe the purpose of this monitoring project..."
        )

        create_button = st.form_submit_button("CREATE PROJECT")

        if create_button:

            if not project_name.strip():
                st.error("Project name is required.")

            else:

                try:
                    response = requests.post(
                        f"{API_URL}/projects/",
                        json={
                            "name": project_name.strip(),
                            "description": project_description.strip()
                        },
                        timeout=10
                    )

                    if response.status_code in [200, 201]:
                        st.success("Project created successfully!")
                        st.rerun()

                    else:
                        st.error(f"Creation failed: {response.text}")

                except requests.RequestException as error:
                    st.error(f"Backend connection error: {error}")

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    # VIEW PROJECTS
    st.markdown("### EXISTING PROJECTS")

    try:

        response = requests.get(
            f"{API_URL}/projects/",
            timeout=10
        )

        response.raise_for_status()

        project_data = response.json()

        if isinstance(project_data, list):
            project_list = project_data

        elif isinstance(project_data, dict):
            project_list = project_data.get("projects", [])

        else:
            project_list = []

        if not project_list:

            st.info("No projects found. Create your first project above.")

        else:

            st.caption(f"TOTAL PROJECTS: {len(project_list)}")

            for project in project_list:

                project_id = project.get("id")

                with st.container(border=True):

                    col1, col2 = st.columns([4, 1])

                    with col1:

                        st.markdown(
                            f"### {project.get('name', 'Unnamed Project')}"
                        )

                        st.caption(f"PROJECT ID: {project_id}")

                        st.write(
                            project.get("description") or
                            "No description provided."
                        )

                        st.caption(
                            f"STATUS: {project.get('status', 'Active')}"
                        )

                    with col2:

                        if st.button(
                            "DELETE",
                            key=f"delete_{project_id}"
                        ):

                            try:

                                delete_response = requests.delete(
                                    f"{API_URL}/projects/{project_id}",
                                    timeout=10
                                )

                                if delete_response.status_code in [200, 204]:
                                    st.success("Project deleted.")
                                    st.rerun()

                                else:
                                    st.error(delete_response.text)

                            except requests.RequestException as error:
                                st.error(str(error))

        st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

        # UPDATE PROJECT
        if project_list:

            st.markdown("### EDIT PROJECT")

            project_options = {
                f"{p.get('id')} — {p.get('name')}": p
                for p in project_list
            }

            selected_project_name = st.selectbox(
                "SELECT PROJECT",
                list(project_options.keys())
            )

            selected_project = project_options[selected_project_name]

            with st.form("update_project_form"):

                updated_name = st.text_input(
                    "PROJECT NAME",
                    value=selected_project.get("name", "")
                )

                updated_description = st.text_area(
                    "PROJECT DESCRIPTION",
                    value=selected_project.get("description") or ""
                )

                update_button = st.form_submit_button("SAVE CHANGES")

                if update_button:

                    if not updated_name.strip():

                        st.error("Project name cannot be empty.")

                    else:

                        update_response = requests.put(
                            f"{API_URL}/projects/{selected_project.get('id')}",
                            json={
                                "name": updated_name.strip(),
                                "description": updated_description.strip()
                            },
                            timeout=10
                        )

                        if update_response.status_code == 200:

                            st.success("Project updated successfully!")
                            st.rerun()

                        else:

                            st.error(
                                f"Update failed: {update_response.text}"
                            )

    except requests.RequestException as error:

        st.error(f"Unable to load projects: {error}")

elif page == "Data Ingestion":

    st.markdown("# DATA INGESTION")
    st.caption("UPLOAD · VALIDATE · PREPARE DATASETS FOR MONITORING")

    st.markdown(
        '<div class="section-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown("### DATASET CONFIGURATION")

    st.write(
        "Upload a reference dataset and an incoming dataset "
        "to prepare them for drift monitoring."
    )

    col1, col2 = st.columns(2)

    # REFERENCE DATASET

    with col1:

        st.markdown("### 01 / REFERENCE DATASET")

        st.caption("BASELINE DATA")

        reference_file = st.file_uploader(
            "Upload reference CSV",
            type=["csv"],
            key="reference_upload"
        )

        if reference_file is not None:

            st.write(f"Filename: {reference_file.name}")

            st.write(
                f"File size: {reference_file.size / 1024:.2f} KB"
            )

            if st.button(
                "UPLOAD REFERENCE DATA",
                key="upload_reference"
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/datasets/upload/reference",
                        files={
                            "file": (
                                reference_file.name,
                                reference_file.getvalue(),
                                "text/csv"
                            )
                        },
                        timeout=30
                    )

                    if response.status_code in [200, 201]:

                        st.session_state["reference_filename"] = (
                            reference_file.name
                        )

                        st.success("Reference dataset uploaded successfully!")

                        st.json(response.json())

                    else:

                        st.error(
                            f"Upload failed: {response.text}"
                        )

                except requests.RequestException as error:

                    st.error(f"Backend connection error: {error}")

    # INCOMING DATASET

    with col2:

        st.markdown("### 02 / INCOMING DATASET")

        st.caption("NEW DATA FOR MONITORING")

        incoming_file = st.file_uploader(
            "Upload incoming CSV",
            type=["csv"],
            key="incoming_upload"
        )

        if incoming_file is not None:

            st.write(f"Filename: {incoming_file.name}")

            st.write(
                f"File size: {incoming_file.size / 1024:.2f} KB"
            )

            if st.button(
                "UPLOAD INCOMING DATA",
                key="upload_incoming"
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/datasets/upload/incoming",
                        files={
                            "file": (
                                incoming_file.name,
                                incoming_file.getvalue(),
                                "text/csv"
                            )
                        },
                        timeout=30
                    )

                    if response.status_code in [200, 201]:

                        st.session_state["incoming_filename"] = (
                            incoming_file.name
                        )

                        st.success("Incoming dataset uploaded successfully!")

                        st.json(response.json())

                    else:

                        st.error(
                            f"Upload failed: {response.text}"
                        )

                except requests.RequestException as error:

                    st.error(f"Backend connection error: {error}")

    st.markdown(
        '<div class="section-line"></div>',
        unsafe_allow_html=True
    )

    # UPLOAD STATUS - READ FROM SAVED FILES

    st.markdown("### DATASET STATUS")

    reference_filename = get_latest_dataset_filename("reference")
    incoming_filename = get_latest_dataset_filename("incoming")

    status_col1, status_col2 = st.columns(2)

    with status_col1:
        if reference_filename:
            st.success(f"REFERENCE READY: {reference_filename}")
        else:
            st.warning("REFERENCE DATASET NOT UPLOADED")

    with status_col2:
        if incoming_filename:
            st.success(f"INCOMING READY: {incoming_filename}")
        else:
            st.warning("INCOMING DATASET NOT UPLOADED")

elif page == "Drift Monitor":

    st.markdown("# DRIFT MONITOR")
    st.caption("DETECT DISTRIBUTION CHANGES · MONITOR MODEL INPUTS")

    st.markdown(
        '<div class="section-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown("### MONITORING CONFIGURATION")

    # Read dataset names from disk so they remain available after refresh.
    reference_file = get_latest_dataset_filename("reference")
    incoming_file = get_latest_dataset_filename("incoming")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**REFERENCE DATASET**")
        st.success(reference_file if reference_file else "Not uploaded")

    with col2:
        st.markdown("**INCOMING DATASET**")
        st.success(incoming_file if incoming_file else "Not uploaded")

    if not reference_file or not incoming_file:

        st.warning("Upload both datasets before starting monitoring.")

    else:

        st.markdown("---")

        if st.button("RUN DRIFT DETECTION"):

            with st.spinner("Analysing datasets..."):

                try:

                    response = requests.post(
                        f"{API_URL}/monitoring/run",
                        json={
                            "reference_filename": reference_file,
                            "current_filename": incoming_file
                        },
                        timeout=60
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.session_state["latest_monitoring_result"] = result

                        st.success("Monitoring completed successfully!")

                    else:

                        st.error(
                            f"Monitoring failed: {response.text}"
                        )

                except requests.RequestException as error:

                    st.error(f"Backend connection error: {error}")

    # DISPLAY RESULTS

    result = st.session_state.get("latest_monitoring_result")

    if result:

        st.markdown("---")

        st.markdown("### MONITORING RESULTS")

        st.write(f"RUN ID: {result.get('run_id')}")

        monitoring = result.get("monitoring_results", {})

        drift = monitoring.get("data_drift", {})

        total = drift.get("total_features", 0)
        drifted = drift.get("drifted_features", 0)
        stable = drift.get("stable_features", 0)

        c1, c2, c3 = st.columns(3)

        c1.metric("TOTAL FEATURES", total)
        c2.metric("DRIFTED FEATURES", drifted)
        c3.metric("STABLE FEATURES", stable)

        st.markdown("### FEATURE-LEVEL ANALYSIS")

        feature_results = drift.get("feature_results", {})

        if feature_results:

            rows = []

            for feature, details in feature_results.items():

                rows.append({
                    "Feature": feature,
                    "PSI Score": details.get("psi_score", "N/A"),
                    "KS Statistic": details.get("ks_statistic", "N/A"),
                    "KS P-Value": details.get("ks_p_value", "N/A"),
                    "Status": details.get("status", "N/A")
                })

            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No feature-level results available.")

        st.markdown("### PERFORMANCE STATUS")

        st.info(
            monitoring.get(
                "performance_status",
                "Unavailable"
            )
        )

        st.markdown("### GENERATED ALERTS")

        st.write(
            f"Alerts generated: {result.get('alerts_generated', 0)}"
        )

        for alert in result.get("alerts", []):

            st.warning(
                f"{alert.get('feature_name')} — "
                f"{alert.get('severity')} — "
                f"{alert.get('status')}"
            )

elif page == "Alerts":

    st.markdown("# ALERT MANAGEMENT")
    st.caption("MONITOR · INVESTIGATE · ACKNOWLEDGE")

    st.markdown(
        '<div class="section-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown("### GENERATED ALERTS")

    try:
        response = requests.get(
            f"{API_URL}/alerts/",
            timeout=15
        )

        if response.status_code == 200:

            alerts = response.json()

            if isinstance(alerts, dict):
                alerts = alerts.get("alerts", [])

            if not alerts:
                st.info("No alerts available yet.")

            else:
                total_alerts = len(alerts)
                new_alerts = sum(
                    1 for alert in alerts
                    if alert.get("status") == "New"
                )
                acknowledged = sum(
                    1 for alert in alerts
                    if alert.get("status") == "Acknowledged"
                )

                col1, col2, col3 = st.columns(3)

                col1.metric("TOTAL ALERTS", total_alerts)
                col2.metric("NEW ALERTS", new_alerts)
                col3.metric("ACKNOWLEDGED", acknowledged)

                st.markdown("---")
                st.markdown("### ALERT REGISTER")

                for alert in alerts:

                    alert_id = alert.get("id")
                    feature = alert.get("feature_name", "Unknown")
                    severity = alert.get("severity", "Unknown")
                    status = alert.get("status", "Unknown")
                    run_id = alert.get("run_id", "N/A")
                    message = alert.get("message", "No description available.")

                    with st.container(border=True):

                        col1, col2 = st.columns([3, 1])

                        with col1:
                            st.markdown(f"**{feature.upper()}**")
                            st.caption(f"ALERT ID: {alert_id} | RUN ID: {run_id}")

                        with col2:
                            st.markdown(f"**{severity}**")
                            st.caption(f"STATUS: {status}")

                        st.write(message)

                        if status == "New":

                            if st.button(
                                "ACKNOWLEDGE ALERT",
                                key=f"ack_{alert_id}"
                            ):

                                ack_response = requests.patch(
                                    f"{API_URL}/alerts/{alert_id}/acknowledge",
                                    timeout=15
                                )

                                if ack_response.status_code == 200:
                                    st.success("Alert acknowledged successfully!")
                                    st.rerun()
                                else:
                                    st.error(
                                        f"Unable to acknowledge alert: "
                                        f"{ack_response.text}"
                                    )

                        else:
                            st.success("This alert has been acknowledged.")

        else:
            st.error(f"Unable to load alerts: {response.text}")

    except requests.RequestException as error:
        st.error(f"Backend connection error: {error}")
elif page == "Monitoring History":

    st.markdown("# MONITORING HISTORY")
    st.caption("TRACK · REVIEW · INVESTIGATE PREVIOUS MONITORING RUNS")

    st.markdown(
        '<div class="section-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown("### HISTORICAL MONITORING RECORDS")

    try:
        response = requests.get(
            f"{API_URL}/monitoring/history",
            timeout=15
        )

        if response.status_code == 200:

            history_data = response.json()

            if isinstance(history_data, dict):
                history = history_data.get("history", [])
                total_runs = history_data.get("total_runs", len(history))
            else:
                history = history_data
                total_runs = len(history)

            if not history:
                st.info("No monitoring history available yet.")

            else:
                total_drifted = sum(
                    run.get("drifted_features", 0)
                    for run in history
                )

                total_stable = sum(
                    run.get("stable_features", 0)
                    for run in history
                )

                col1, col2, col3 = st.columns(3)

                col1.metric("TOTAL RUNS", total_runs)
                col2.metric("DRIFTED FEATURES", total_drifted)
                col3.metric("STABLE FEATURES", total_stable)

                st.markdown("---")
                st.markdown("### RUN REGISTER")

                rows = []

                for run in history:
                    rows.append({
                        "Run ID": run.get("run_id"),
                        "Reference Dataset": run.get("reference_dataset", "N/A"),
                        "Incoming Dataset": run.get("incoming_dataset", "N/A"),
                        "Total Features": run.get("total_features", 0),
                        "Drifted": run.get("drifted_features", 0),
                        "Stable": run.get("stable_features", 0)
                    })

                st.dataframe(
                    rows,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("---")
                st.markdown("### INSPECT MONITORING RUN")

                run_ids = [
                    run.get("run_id")
                    for run in history
                    if run.get("run_id") is not None
                ]

                selected_run = st.selectbox(
                    "SELECT RUN ID",
                    run_ids
                )

                if st.button("VIEW RUN DETAILS"):

                    detail_response = requests.get(
                        f"{API_URL}/monitoring/history/{selected_run}",
                        timeout=15
                    )

                    if detail_response.status_code == 200:

                        details = detail_response.json()

                        st.success(
                            f"Monitoring Run #{selected_run} loaded successfully!"
                        )

                        st.markdown("### COMPLETE RUN DETAILS")
                        st.json(details)

                    else:
                        st.error(
                            f"Unable to load run details: "
                            f"{detail_response.text}"
                        )

        else:
            st.error(f"Unable to load history: {response.text}")

    except requests.RequestException as error:
        st.error(f"Backend connection error: {error}")
    st.title("MONITORING HISTORY")
    st.info("Monitoring history interface is coming next.")

elif page == "Reports":

    st.markdown("# MONITORING REPORTS")
    st.caption("GENERATE · REVIEW · EXPORT MONITORING REPORTS")

    st.markdown(
        '<div class="section-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown("### REPORT CONFIGURATION")

    try:
        response = requests.get(
            f"{API_URL}/monitoring/history",
            timeout=15
        )

        if response.status_code == 200:

            history_data = response.json()

            if isinstance(history_data, dict):
                history = history_data.get("history", [])
            else:
                history = history_data

            run_ids = [
                run.get("run_id")
                for run in history
                if run.get("run_id") is not None
            ]

            if not run_ids:
                st.info("No monitoring runs available for reporting.")

            else:
                selected_run = st.selectbox(
                    "SELECT MONITORING RUN",
                    run_ids
                )

                if st.button("GENERATE REPORT"):

                    report_response = requests.get(
                        f"{API_URL}/reports/{selected_run}",
                        timeout=30
                    )

                    if report_response.status_code == 200:

                        report = report_response.json()

                        st.session_state["generated_report"] = report
                        st.session_state["report_run_id"] = selected_run

                        st.success("Monitoring report generated successfully!")

                    else:
                        st.error(
                            f"Report generation failed: "
                            f"{report_response.text}"
                        )

                report = st.session_state.get("generated_report")
                report_run_id = st.session_state.get("report_run_id")

                if report and report_run_id == selected_run:

                    st.markdown("---")
                    st.markdown("### REPORT PREVIEW")

                    st.json(report)

                    st.markdown("---")
                    st.markdown("### PDF EXPORT")

                    pdf_response = requests.get(
                        f"{API_URL}/reports/pdf/{selected_run}",
                        timeout=30
                    )

                    if pdf_response.status_code == 200:

                        st.download_button(
                            label="DOWNLOAD PDF REPORT",
                            data=pdf_response.content,
                            file_name=f"DriftShield_Report_Run_{selected_run}.pdf",
                            mime="application/pdf"
                        )

                        st.success("PDF report is ready for download!")

                    else:
                        st.error(
                            f"PDF generation failed: "
                            f"{pdf_response.text}"
                        )

        else:
            st.error(f"Unable to load monitoring history: {response.text}")

    except requests.RequestException as error:
        st.error(f"Backend connection error: {error}")
    st.title("REPORT GENERATION")
    st.info("Report download interface is coming next.")
    