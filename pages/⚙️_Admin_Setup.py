import streamlit as st
from github import Github
import pandas as pd

st.set_page_config(page_title="Ecosystem Analytics", page_icon="⚙️", layout="wide")

st.title("⚙️ Bulk Webhook Configuration & Account Metrics")
st.write("Analyze repository spikes and deploy configurations dynamically across your entire profile.")

# =========================================================================
# 🔒 1. ACCESS CONTROL GATEWAY
# =========================================================================
correct_password = st.secrets["admin_security"]["admin_password"]
user_input_password = st.text_input("🔑 Enter Admin Access Password to Unlock:", type="password")

access_granted = False

if user_input_password == correct_password:
    access_granted = True
    st.success("🔒 Access Granted. Loading infrastructure control panel...")
elif user_input_password != "":
    st.error("🚫 Access Denied. Please input the correct admin security password.")
else:
    st.warning("🔑 Please input the password to unlock the developer dashboard management panel.")


# =========================================================================
# 📊 2. CORE UTILITIES (ONLY RUNS IF ACCESS IS GRANTED)
# =========================================================================
if access_granted:
    if "github_setup" in st.secrets and "token" in st.secrets["github_setup"]:
        github_token = st.secrets["github_setup"]["token"]
        target_receiver_url = st.secrets["github_setup"]["github_webhook_endpoint"]
    else:
        github_token = None
        st.error("⚠️ Configuration Error: Could not find '[github_setup]' variables inside your Streamlit Cloud Secrets dashboard.")

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
                st.info("The spikes in this graph show periods where you created clusters of repositories at once.")
                
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
