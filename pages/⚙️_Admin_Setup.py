import streamlit as st
from github import Github
import pandas as pd

st.set_page_config(page_title="Ecosystem Analytics", page_icon="⚙️", layout="wide")

st.title("⚙️ Bulk Webhook Configuration & Account Metrics")
st.write("Analyze repository spikes and deploy configurations dynamically across your entire profile.")

# 🔒 Input keys safely inside the running browser interface
github_token = st.text_input("Enter GitHub Personal Access Token (PAT):", type="password")
target_receiver_url = st.text_input("Enter Webhook Target Receiver Endpoint URL:", 
                                    placeholder="https://your-receiver-server.com")

# Only run analytics if a token is entered
if github_token:
    try:
        # Initialize PyGithub connection
        g = Github(github_token)
        authenticated_user = g.get_user()
        
        # 1. FETCH REPOSITORIES & METRICS IN REAL-TIME
        with st.spinner("Analyzing repository historical data timelines..."):
            repositories = authenticated_user.get_repos(type="owner")
            
            repo_data = []
            
            # Loops through all available repos dynamically (handles auto scaling/shrinking)
            for repo in repositories:
                repo_data.append({
                    "Name": repo.name,
                    "Created_At": repo.created_at,
                    "Year_Month": repo.created_at.strftime("%Y-%m") # Grouping into Month buckets
                })
            
            # Format raw array data into a table structure
            df = pd.DataFrame(repo_data)
            total_repos = len(df)
            
        # 2. RENDER INTERACTIVE ANALYTICS GRAPH
        st.subheader("📊 Repository Creation Timeline Metrics")
        st.metric(label="Total Tracked Repositories Owned", value=total_repos)
        
        if not df.empty:
            # Group repositories by year/month to count how many were built during specific windows
            timeline_counts = df.groupby("Year_Month").size().reset_index(name="Repositories Created")
            timeline_counts = timeline_counts.sort_values("Year_Month")
            
            st.markdown("### 📈 Creation Spikes Chart")
            st.info("The spikes in this graph show periods where you created clusters of repositories at once.")
            
            # Draw line chart automatically reflecting exact count data points
            st.line_chart(data=timeline_counts, x="Year_Month", y="Repositories Created", color="#ff4b4b")
            
            # View Raw Datatable breakdown inside an expandable view drawer
            with st.expander("👁️ View Raw Project Date Registry"):
                st.dataframe(df.sort_values(by="Created_At", ascending=False), use_container_width=True)
        
        # 3. BULK DEPLOYMENT SYSTEM ACTION
        st.markdown("---")
        st.subheader("🚀 Infrastructure Sync Controller")
        
        if st.button("Deploy Webhooks globally across all current repos"):
            if not target_receiver_url:
                st.error("Please enter a target webhook receiver endpoint URL first.")
            else:
                counter_success = 0
                counter_skipped = 0
                status_box = st.empty()
                
                with st.spinner("Injecting hooks cloud-to-cloud..."):
                    for repo in repositories:
                        try:
                            config = {"url": target_receiver_url, "content_type": "json"}
                            # Subscribe repository actions cleanly
                            repo.create_hook("web", config, ["push", "repository"], active=True)
                            counter_success += 1
                            status_box.text(f"✅ Webhook configured -> {repo.full_name}")
                        except Exception as e:
                            # Catch standard 422 errors indicating that the hook is already alive
                            if "already exists" in str(e).lower():
                                counter_skipped += 1
                            else:
                                st.warning(f"❌ Failed for {repo.name}: {str(e)}")
                                
                st.balloons()
                st.success(f"Sync Finished! Configured: {counter_success} | Skipped/Existing: {counter_skipped}")
                
    except Exception as auth_error:
        st.error(f"GitHub Auth Failure: Ensure token characters are valid. Details: {str(auth_error)}")
else:
    st.warning("🔑 Please input your GitHub Personal Access Token at the top of the page to generate your analytics graph.")
