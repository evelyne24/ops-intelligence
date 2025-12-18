import streamlit as st
import pandas as pd
import json
import os

# Point to the shared Docker volume path
DATA_PATH = "/app/data/dashboard_data.json"

def main():
    st.set_page_config(layout="wide", page_title="Ops Intelligence")
    st.title("🤖 Agentic Engineering Dashboard")

    if not os.path.exists(DATA_PATH):
        st.warning("⏳ Waiting for agents to generate data... Refresh shortly.")
        return

    with open(DATA_PATH, "r") as f:
        # Simple error handling for malformed JSON from LLM
        try:
            content = f.read()
            # Clean potential markdown wrapping
            if "```" in content:
                content = content.split("```")[1]
                if content.startswith("json"): content = content[4:]
            data = json.loads(content)
        except:
            st.error("Error parsing data. Agents might be writing invalid JSON.")
            return

    stats = data.get("summary", {})
    
    col1, col2 = st.columns(2)
    col1.metric("Ghost Work", f"{stats.get('ghost_work_pct', 0)}%")
    col2.metric("Tickets Processed", stats.get('total_tickets', 0))

if __name__ == "__main__":
    main()