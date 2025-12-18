import random
import json
from datetime import datetime, timedelta
from faker import Faker
from crewai.tools import BaseTool

class EngineeringSimulatorTool(BaseTool):
    name: str = "Simulated Data Generator"
    description: str = "Generates 90 days of simulated Jira/GitHub data for a struggling team."

    def _run(self) -> str:
        fake = Faker()
        num_engineers = 8
        days = 90
        engineers = [fake.first_name() for _ in range(num_engineers)]
        start_date = datetime.now() - timedelta(days=days)
        
        jira_tickets = []
        github_prs = []
        ticket_counter = 100
        current_date = start_date

        while current_date <= datetime.now():
            if current_date.weekday() < 5 and random.random() > 0.3:
                num_tickets = random.randint(1, 4)
                for _ in range(num_tickets):
                    ticket_counter += 1
                    t_key = f"PROJ-{ticket_counter}"
                    assignee = random.choice(engineers)
                    
                    # Scenario: Unclear Requirements (Churn)
                    is_churny = random.random() < 0.4
                    churn_count = random.randint(2, 5) if is_churny else 0
                    coding_days = random.randint(5, 12) if is_churny else random.randint(1, 3)
                    
                    # Scenario: Poor Hygiene (Long Reviews)
                    pr_date = current_date + timedelta(days=coding_days)
                    is_long_review = random.random() < 0.5
                    review_days = random.randint(3, 7) if is_long_review else random.randint(0, 2)
                    resolve_date = pr_date + timedelta(days=review_days)
                    
                    status = "Done" if resolve_date <= datetime.now() else "In Progress"

                    jira_tickets.append({
                        "key": t_key,
                        "status": status,
                        "assignee": assignee,
                        "created_at": current_date.isoformat(),
                        "resolved_at": resolve_date.isoformat() if status == "Done" else None,
                        "churn_events": churn_count
                    })

                    # Scenario: Ghost Work (Missing Linkage)
                    if pr_date <= datetime.now():
                        is_ghost = random.random() < 0.3
                        title = f"feat: {fake.sentence(nb_words=4)[:-1]}"
                        final_title = title if is_ghost else f"feat: {t_key} {title}"
                        
                        github_prs.append({
                            "title": final_title,
                            "created_at": pr_date.isoformat(),
                            "merged_at": resolve_date.isoformat() if status == "Done" else None,
                            "comments": random.randint(10, 30) if is_long_review else random.randint(0, 5)
                        })
            
            current_date += timedelta(days=1)
            
        return json.dumps({"jira_tickets": jira_tickets, "github_prs": github_prs})