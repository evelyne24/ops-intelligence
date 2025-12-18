import streamlit as st
import pandas as pd
import json
import plotly.express as px
from ops_intelligence.aws import S3Client

def main():
    st.set_page_config(layout="wide", page_title="Ops Intelligence")
    s3 = S3Client()

    # --- 1. Fetch History from S3 ---
    with st.spinner("Connecting to Cloud Storage..."):
        files = s3.list_files()

    if not files:
        st.warning("⚠️ No data found in S3 Bucket. Please run 'python main.py analyze' first.")
        return

    # --- 2. Sidebar Selector ---
    st.sidebar.title("🗂️ Run History")
    
    # Create a mapping of "Filename" -> "S3 Key"
    # Files are already sorted newest-first by our S3Client
    options = [f['Key'] for f in files]
    
    selected_key = st.sidebar.selectbox(
        "Select Analysis Run:",
        options=options,
        index=0  # Default to 0 (The Newest)
    )

    # --- 3. Download & Parse ---
    try:
        raw_content = s3.download_as_json(selected_key)
        
        # Clean Markdown wrappers if present
        if "```" in raw_content:
            raw_content = raw_content.split("```")[1]
            if raw_content.startswith("json"): raw_content = raw_content[4:]
            
        data = json.loads(raw_content)
        st.sidebar.success(f"Loaded: {selected_key}")
        
    except Exception as e:
        st.error(f"Failed to load file: {e}")
        return

    # --- 4. Render Dashboard ---
    stats = data.get("summary", {})
    st.title(f"📊 Dashboard: {selected_key}")
    
    # KPI Row
    k1, k2, k3 = st.columns(3)
    k1.metric("Ghost Work", f"{stats.get('ghost_work_pct', 0)}%")
    k2.metric("High Churn Tickets", stats.get('high_churn_count', 0))
    k3.metric("Total Throughput", stats.get('total_tickets', 0))
    
    st.divider()
    
    # Charts
    c1, c2 = st.columns(2)
    tickets = pd.DataFrame(data.get("raw_tickets", []))
    
    with c1:
        if not tickets.empty:
            st.subheader("Ticket Churn")
            fig = px.bar(tickets['churn_events'].value_counts().reset_index(), 
                         x="churn_events", y="count")
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Raw Data")
        st.dataframe(tickets.head(10))

if __name__ == "__main__":
    main()