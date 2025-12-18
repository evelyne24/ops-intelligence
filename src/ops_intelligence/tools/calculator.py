import json
import re
from crewai.tools import BaseTool

class MetricsCalculatorTool(BaseTool):
    name: str = "Metrics Calculator"
    description: str = "Calculates Cycle Time, Churn, and Ghost Work stats from raw JSON."

    def _run(self, json_data: str) -> str:
        try:
            # Handle potential double-encoding from LLMs
            if isinstance(json_data, str):
                 # Strip markdown code blocks if present
                clean_json = json_data.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)
            else:
                data = json_data
        except:
            return json.dumps({"error": "Invalid JSON input"})
            
        tickets = data.get('jira_tickets', [])
        prs = data.get('github_prs', [])
        ticket_pattern = re.compile(r"([A-Z]+-\d+)")
        
        # Linkage Logic
        ghosts = [pr['title'] for pr in prs if not ticket_pattern.search(pr['title'])]
        churners = [t for t in tickets if t['churn_events'] > 1]
        
        # Stats
        ghost_rate = (len(ghosts) / len(prs) * 100) if prs else 0
        
        result = {
            "summary": {
                "ghost_work_pct": round(ghost_rate, 1),
                "high_churn_count": len(churners),
                "total_tickets": len(tickets),
                "total_prs": len(prs)
            },
            "raw_tickets": tickets,
            "raw_prs": prs
        }
        return json.dumps(result)