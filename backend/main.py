from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/contributors"
COMMITS_API = "https://api.github.com/repos/{owner}/{repo}/commits?author={username}"
COMMITS_API_URL = "https://api.github.com/repos/{owner}/{repo}/commits"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    # "Authorization": "token YOUR_GITHUB_TOKEN"  # Optional
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Contributor(BaseModel):
    username: str
    avatar_url: str
    last_contribution_date: str

@app.get("/top-contributors", response_model=list[Contributor])
def get_top_contributors(owner: str = "microsoft", repo: str = "vscode-cosmosdb", top_n: int = 4):
    contrib_url = GITHUB_API.format(owner=owner, repo=repo)
    response = requests.get(contrib_url, headers=HEADERS)
    if response.status_code != 200:
        return []

    contributors = response.json()[:top_n]
    result = []

    for c in contributors:
        username = c["login"]
        avatar = c["avatar_url"]

        commits_url = COMMITS_API.format(owner=owner, repo=repo, username=username)
        commits_resp = requests.get(commits_url, headers=HEADERS)
        if commits_resp.status_code == 200 and commits_resp.json():
            last_date = commits_resp.json()[0]['commit']['committer']['date']
        else:
            last_date = "N/A"

        result.append(Contributor(
            username=username,
            avatar_url=avatar,
            last_contribution_date=last_date
        ))
    return result

@app.get("/latest-contributors", response_model=list[Contributor])
def fetch_latest_contributors(owner: str = "microsoft", repo: str = "vscode-cosmosdb", top_n: int = 5):
    result = []
    seen_users = set()

    commits_api_url = COMMITS_API_URL.format(owner=owner, repo=repo)
    response = requests.get(commits_api_url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code}")

    commits = response.json()

    for commit in commits:
        author = commit.get("author")
        if not author:
            continue

        username = author["login"]
        if username in seen_users:
            continue

        avatar = author["avatar_url"]
        last_date = commit["commit"]["committer"]["date"]

        result.append(Contributor(
            username=username,
            avatar_url=avatar,
            last_contribution_date=last_date
        ))
        seen_users.add(username)

        if len(result) == top_n:
            break

    return result

@app.get("/standup/{username}")
def get_standup(username: str):
    # Example standup for tnaum-ms
    if username == "tnaum-ms":
        return {
            "yesterday": {
                "summary": "Worked on merging two major PRs to improve BaseCachedBranchDataProvider and launchShell command for Windows.",
                "details": [
                    {
                        "pr_number": 2696,
                        "description": "Re-inserts the node on refresh in BaseCachedBranchDataProvider"
                    },
                    {
                        "pr_number": 2698,
                        "description": "Enhances launchShell command to support different shell environments on Windows"
                    }
                ],
                "commits": 2,
                "additions": 0,
                "deletions": 0,
                "files_changed": 0
            },
            "blockers": [],
            "today": {
                "focus": [
                    "Review and address feedback on recently merged PRs",
                    "Explore follow-up tasks or improvements for BaseCachedBranchDataProvider and launchShell command",
                    "Prioritize open issues or PRs assigned"
                ]
            },
            "user": "Tomasz Naumowicz"
        }
    # For other users, return not submitted
    return JSONResponse(content={"message": "Standup not submitted"}, status_code=404)

@app.get("/retrospectives")
def get_retrospectives():
    return {
        "generated_on": "2025-06-01 10:30:00",
        "milestone": "shipped: 0.25.0",
        "repository": "microsoft/vscode-cosmosdb",
        "retrospective": "## 🎯 MILESTONE OVERVIEW\n- Milestone name: shipped: 0.25.0\n- Timeline: 2025-02-17 to 2025-02-28\n- Scope and key deliverables: API Upgrade - Migrating Tree View to V2, \"Readme\": update for better user engagement\n- Overall team performance summary: The team successfully delivered the milestone with key features and improvements, showing good collaboration and productivity.\n\n## ✅ WHAT WENT WELL (Positives/Wins)\n- Tomasz Naumowicz and Dmitrii Shilov made significant contributions to the API Upgrade for Tree View V2.\n- Efficient development patterns were observed with quick PR turnarounds.\n- The team demonstrated good collaboration in integrating the new Tree API V2.\n- The \"Readme\" update improved user engagement and clarity.\n\n## 🚧 WHAT DIDN'T GO WELL (Pain Points/Challenges)\n- Some PRs took longer than expected to review and merge.\n- There were instances of rework indicated by multiple commits in some PRs.\n- Uneven workload distribution was observed among team members.\n\n## 🔍 WHAT WE LEARNED (Insights/Discoveries)\n- The team gained insights into the new Tree API V2 and its integration challenges.\n- Process learnings included the importance of timely PR reviews.\n- Patterns in commit/PR data showed a need for better workload distribution.\n- Skills development was evident in team members handling new API integrations.\n\n## 🎯 ACTION ITEMS (Improvements for Next Sprint)\n- Improve PR review process to reduce turnaround time.\n- Enhance workload distribution among team members.\n- Continue knowledge sharing on the new Tree API V2.\n- Focus on reducing technical debt introduced during the milestone.\n\n## 📊 TEAM PERFORMANCE METRICS\n- Commit frequency: Regular commits were observed throughout the milestone.\n- PR review and merge time: Some PRs took longer than expected.\n- Code contribution distribution: Tomasz Naumowicz and Dmitrii Shilov were top contributors.\n- Active development days: Team members were active throughout the milestone period.\n\n## 🏆 INDIVIDUAL CONTRIBUTIONS & RECOGNITION\n- Tomasz Naumowicz: Led the API Upgrade for Tree View V2 effort.\n- Dmitrii Shilov: Made significant contributions to the Tree View V2 migration.\n- Emerging leaders: Dmitrii Shilov showed leadership in handling complex tasks.\n\n## 📈 MILESTONE SUCCESS CRITERIA\n- Delivery timeline: The milestone was delivered on time.\n- Quality of deliverables: High-quality deliverables were achieved.\n- Team velocity: The team showed good productivity.\n- Technical debt: Some technical debt was introduced but is being addressed.\n- Stakeholder satisfaction: Stakeholders were satisfied with the milestone delivery."
    }

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "")
    # For now, always return a sample answer
    return {"answer": f"This is a sample answer to your question: '{question}'. (Replace this with real logic later)"}

