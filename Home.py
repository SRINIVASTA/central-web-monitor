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
        SENDER = st.secrets["email_credentials"]["sender_account"]
        PASSWORD = st.secrets["email_credentials"]["app_password"]
        RECEIVER = st.secrets["email_credentials"]["receiver_account"]
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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
        
        # 👑 FIXED DOMAIN PATH: Clean connection to Gmail servers
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
if "github_setup" in st.secrets and "app_name" in st.secrets["github_setup"]:
    MY_CURRENT_APP_ID = st.secrets["github_setup"]["app_name"]
else:
    MY_CURRENT_APP_ID = "Fallback-Analytics-Hub"

if 'initial_load_sent' not in st.session_state:
    st.session_state['initial_load_sent'] = True
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

with st.expander("🔐 View Configured Operational Infrastructure Enclaves"):
    if "github_setup" in st.secrets:
        st.write(f"📁 Target Endpoint Hub Link: `{st.secrets['github_setup']['github_webhook_endpoint']}`")
        st.write(f"🔑 Auth Token Masked Status: `✓ ghp_... Protected Matrix Loaded`")
    else:
        st.error("⚠️ Global config file missing profile attributes inside Streamlit context layer.")

st.info("💡 Use the sidebar navigation menu on the left side of your screen to swap between workspace dashboards.")


# =============================================================================
# 🎯 ABSOLUTE LAST LINE OF HOME.PY (GUARANTEED FOOTER INJECTION)
# =============================================================================
st.markdown( 
 """ 
 <style> 
 .footer { 
     position: fixed; 
     left: 0; 
     bottom: 0; 
     width: 100%; 
     background-color: #262730; 
     color: #FAFAFA; 
     text-align: center; 
     font-size: 13px; 
     padding: 12px 0; 
     z-index: 9999999 !important; 
     border-top: 1px solid #FF4B4B; 
 } 
 .footer a { 
     color: #FF4B4B; 
     text-decoration: none; 
     margin: 0 10px; 
     font-weight: bold; 
 } 
 .footer a:hover { 
     text-decoration: underline; 
     color: #FAFAFA; 
 } 
 .footer-separator { 
     color: #666; 
     margin: 0 5px; 
     font-weight: bold;
 } 
 [data-testid="stMainBlockContainer"] { 
     padding-bottom: 120px !important; 
 } 
 .main .block-container {
     padding-bottom: 120px !important;
 }
 </style> 
 <div class="footer"> 
     <span><strong>© 2026 T A Srinivas.</strong> All Rights Reserved. Prototype for portfolio display. For commercial licensing requests, please use the contact channels.</span> 
     <span class="footer-separator">|</span> 
     <a href="https://linkedin.com" target="_blank">LinkedIn Profile</a> 
     <span class="footer-separator">|</span> 
     <a href="mailto:tasrinivass@gmail.com">Contact Me</a> 
 </div> 
 """, 
 unsafe_allow_html=True 
)
