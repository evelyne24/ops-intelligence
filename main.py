# Location: /ops-intelligence/main.py (ROOT)
import click
import subprocess
import os
from dotenv import load_dotenv
import time

# CORRECT IMPORT: Notice we do NOT say 'src.ops_intelligence'
from ops_intelligence.crew import OpsIntelligenceCrew

load_dotenv()

@click.group()
def cli():
    """Agentic Ops Intelligence System"""
    pass

@cli.command()
def analyze():
    """Run the AI Agents to simulate and analyze data."""
    print("🚀 Kicking off CrewAI Agents...")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            OpsIntelligenceCrew().crew().kickoff()
            print("✅ Analysis Complete.")
            return # Exit successfully
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e).lower():
                wait_time = (attempt + 1) * 5 # Wait 5s, then 10s, then 15s
                print(f"⚠️ Model overloaded. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                # If it's a real code error, crash immediately
                raise e
    
    print("❌ Failed after multiple retries. Please try again later.")

@cli.command()
def dashboard():
    """Launch the Web Dashboard."""
    print("📊 Starting Streamlit Dashboard...")
    
    # We use 'sys.executable' or direct command to ensure we use the correct env
    # Note: Streamlit needs the path to the file.
    dashboard_path = os.path.join("src", "web", "dashboard.py")
    
    subprocess.run([
        "streamlit", "run", dashboard_path,
        "--server.port=8501", 
        "--server.address=0.0.0.0"
    ])

if __name__ == "__main__":
    cli()