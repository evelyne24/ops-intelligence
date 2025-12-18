import click
import subprocess
import os
from datetime import datetime
from ops_intelligence.crew import OpsIntelligenceCrew
from ops_intelligence.aws import S3Client

@click.group()
def cli():
    pass

@cli.command()
def analyze():
    """Run Agent -> Timestamp -> Upload to S3"""
    print("🚀 Kicking off CrewAI Agents...")
    
    # 1. Run Crew
    result = OpsIntelligenceCrew().crew().kickoff()
    result_str = str(result)
    
    # 2. Generate Timestamped Filename
    # Format: run_YYYY-MM-DD_HH-MM-SS.json
    filename = f"run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    
    # 3. Upload to LocalStack S3
    print(f"☁️  Uploading {filename} to S3...")
    s3 = S3Client()
    s3.upload_string(result_str, filename)
    
    print("✅ Analysis Complete & Persisted.")

@cli.command()
def dashboard():
    """Launch Streamlit with config fixes"""
    path = os.path.join("src", "web", "dashboard.py")
    subprocess.run([
        "python", "-m", "streamlit", "run", path,
        "--server.port=8501", 
        "--server.address=0.0.0.0",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false"
    ])

if __name__ == "__main__":
    cli()