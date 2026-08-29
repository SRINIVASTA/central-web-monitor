import streamlit as st
import smtplib
from email.mime.text import MIMEText
import datetime

# Must be the absolute first line of Streamlit code execution
st.set_page_config(page_title="Central App Monitor", page_icon="🚀", layout="centered")

# ==========================================
# SECURE CLOUD EMAIL ENGINE (SMTP)
# ==========================================
def fire_page_load_alert(app_identifier):
    try:
        # Secure extraction directly from Streamlit Cloud Dashboard Secrets Console
        SENDER = st.secrets["email_credentials"]["sender_account"]
        PASSWORD = st.secrets["email_credentials"]["app_password"]
        RECEIVER = st.secrets["email_credentials"]["receiver_account"]
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Construct clean email metadata properties
        subject = f"🌐 [Streamlit Open] View Registered on: {app_identifier}"
        body = (
            f"Hello,\n\nA new user loaded your online app layout environment.\n\n"
            f"• App Tracking ID: {app_identifier}\n"
            f"• Action Log Time: {timestamp}\n"
            f"• Platform: Streamlit Community Cloud Engine Server Cluster"
        )
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = f"Streamlit Monitor Core <{SENDER}>"
        msg['To'] = RECEIVER
        
        # Establish an encrypted connection directly to Gmail servers over SSL Port 465
        with smtplib.SMTP_SSL("://gmail.com", 465) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, [RECEIVER], msg.as_string())
        return True
    except Exception as e:
        print(f"Background SMTP Error: {str(e)}")
        return False

# ==========================================
# OPEN DETECTOR RUNTIME TRIGGER
# ==========================================
# Give this specific website instance a unique tracking name
MY_CURRENT_APP_ID = "Production-Analytics-Hub"

# Streamlit updates top-to-bottom on actions. session_state locks notifications to page-open events only.
if 'initial_load_sent' not in st.session_state:
    st.session_state['initial_load_sent'] = True
    # Fire secure email alert web-only cloud-to-cloud instantly
    fire_page_load_alert(MY_CURRENT_APP_ID)

# ==========================================
# VISUAL USER INTERFACE (WEB SURFACE)
# ==========================================
st.title("🚀 Centralized Production Matrix Platform")
st.markdown("---")

st.markdown("""
### Welcome to your Universal Cloud Workspace Dashboard
This entire architecture is configured **web-only (serverless)**. All logging metrics, analytics charts, and webhook integrations execute directly cloud-to-cloud.

#### 📊 Active Utilities:
* **Real-time Open Notifications:** Opening this URL sends a background security trigger straight to your email inbox.
* **Account Analytics Engine:** Click the **`Admin Setup`** page inside the left sidebar menu to explore repo creation trends and activity spikes.
* **Mass Webhook Infrastructure:** Use the admin array to push webhook listeners across your entire list of code repositories concurrently in one click.
""")

st.success(f"✔️ Active Telemetry Tracking Node initiated for: **{MY_CURRENT_APP_ID}**")
st.info("💡 Use the sidebar navigation menu on the left side of your screen to swap between workspace dashboards.")
