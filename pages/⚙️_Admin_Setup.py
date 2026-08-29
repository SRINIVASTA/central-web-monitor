import streamlit as st
from github import Github
import pandas as pd

st.set_page_config(page_title="Ecosystem Analytics", page_icon="⚙️", layout="wide")

# =========================================================================
# 🔒 1. SECURE SIDEBAR LOGIN / LOGOUT CONTROLLER
# =========================================================================
correct_password = st.secrets["admin_security"]["admin_password"]

# Initialize login states cleanly inside session storage arrays
if "admin_authenticated" not in st.session_state:
    st.session_state["admin_authenticated"] = False

# Draw the control tools inside the sidebar box container panel
with st.sidebar:
    st.markdown("### 🔐 Admin Access Console")
    
    if st.session_state["admin_authenticated"]:
        st.success("✓ Session Active")
        # 🔴 LOGOUT ACTION BUTTON
        if st.button("❌ Logout from Admin Session", use_container_width=True):
            st.session_state["admin_authenticated"] = False
            st.rerun() # Refresh app container to lock the system instantly
    else:
        st.warning("🔒 Session Locked")
        # Alternative input window directly inside the sidebar layout box
        sidebar_password = st.text_input("Enter Passcode:", type="password", key="sidebar_pass_input")
        if st.button("🔑 Login", use_container_width=True):
            if sidebar_password == correct_password:
                st.session_state["admin_authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect Passcode")

# Global access validation parameter check
access_granted = st.session_state["admin_authenticated"]

# =========================================================================
# 🗄️ 2. MAIN SURFACE INTERFACE LAYOUT (DYNAMIC DISPLAY HOOK)
# =========================================================================
st.title("⚙️ Bulk Webhook Configuration & Account Metrics")
st.write("Analyze repository spikes and deploy configurations dynamically across your entire profile.")

if not access_granted:
    # Main window display fallback screen if user is logged out
    st.markdown("---")
    st.info("### 🔑 Developer Portal Locked")
    st.write("Please use the input form fields inside the left sidebar panel to authenticate and unlock your analytical data monitors.")
    
    # Optional fallback input block in the center screen if sidebar is closed
    center_password = st.text_input("Or enter password here to unlock:", type="password", key="center_pass_input")
    if center_password:
        if center_password == correct_password:
            st.session_state["admin_authenticated"] = True
            st.rerun()
        else:
            st.error("🚫 Access Denied. Please input the correct admin security password.")

# =========================================================================
# 📊 3. CORE UTILITIES (ONLY RUNS AFTER ACCESS IS GRANTED)
# =========================================================================
if access_granted:
    if "github_setup" in st.secrets and "token" in st.secrets["github_setup"]:
        github_token = st.secrets["github_setup"]["token"]
        target_receiver_url = st.secrets["github_setup"]["github_webhook_endpoint"]
    else:
        github_token = None
        st.error("⚠️ Configuration Error: Missing github parameters inside Streamlit Cloud Secrets.")

    if github_token:
        try:
            g = Github(github_token)
            authenticated_user = g.get_user()
            
            with st.spinner("Analyzing repository historical data timelines..."):
                repositories = authenticated_user.get_repos(type="owner")
                repo_data = []
                
                for repo in repositories:
                    repo_data.append({
                        "Name": repo.name,
                        "Created_At": repo.created_at,
                        "Year_Month": repo.created_at.strftime("%Y-%m")
                    })
                
                df = pd.DataFrame(repo_data)
                total_repos = len(df)
                
            st.subheader("📊 Repository Creation Timeline Metrics")
            st.metric(label="Total Tracked Repositories Owned", value=total_repos)
            
            if not df.empty:
                timeline_counts = df.groupby("Year_Month").size().reset_index(name="Repositories Created")
                timeline_counts = timeline_counts.sort_values("Year_Month")
                
                st.markdown("### 📈 Creation Spikes Chart")
                st.line_chart(data=timeline_counts, x="Year_Month", y="Repositories Created", color="#ff4b4b")
                
                with st.expander("👁️ View Raw Project Date Registry"):
                    st.dataframe(df.sort_values(by="Created_At", ascending=False), use_container_width=True)
            
            st.markdown("---")
            st.subheader("🚀 Infrastructure Sync Controller")
            st.write(f"🔗 Target Sync Endpoint: `{target_receiver_url}`")
            
            if st.button("Deploy Webhooks globally across all current repos"):
                if not target_receiver_url:
                    st.error("Please ensure your target webhook receiver endpoint URL is set up in your secrets dashboard.")
                else:
                    counter_success = 0
                    counter_skipped = 0
                    status_box = st.empty()
                    
                    with st.spinner("Injecting hooks cloud-to-cloud..."):
                        for repo in repositories:
                            try:
                                config = {"url": target_receiver_url, "content_type": "json"}
                                repo.create_hook("web", config, ["push", "repository"], active=True)
                                counter_success += 1
                                status_box.text(f"✅ Webhook configured -> {repo.full_name}")
                            except Exception as e:
                                if "already exists" in str(e).lower():
                                    counter_skipped += 1
                                else:
                                    st.warning(f"❌ Failed for {repo.name}: {str(e)}")
                                    
                    st.balloons()
                    st.success(f"Sync Finished! Configured: {counter_success} | Skipped/Existing: {counter_skipped}")
                    
        except Exception as auth_error:
            st.error(f"GitHub Auth Failure: Ensure your token credentials are active. Details: {str(auth_error)}")


# =============================================================================
# 🎯 4. ABSOLUTE LAST LINE OF FILE (GUARANTEED FOOTER IN BOTH STATES)
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
