import os
import json
from datetime import datetime
from dotenv import load_dotenv
from llama_api_client import LlamaAPIClient

# Load environment variables
load_dotenv()

class SimpleStandupGenerator:
    def __init__(self, commit_json_file, yesterday_date="2024-05-26"):
        self.commit_json_file = commit_json_file
        self.yesterday_date = yesterday_date
        self.llama_client = LlamaAPIClient(
            api_key=os.environ.get("LLAMA_API_KEY"),
            base_url="https://api.llama.com/v1/",
        )
        
        print(f"📅 Generating standup for yesterday: {yesterday_date}")
        
    def load_commit_data(self):
        """Load the commit history JSON"""
        try:
            with open(self.commit_json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: File '{self.commit_json_file}' not found")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in '{self.commit_json_file}': {str(e)}")
            return None
    
    def generate_standup_prompt(self, commit_data):
        """Generate a comprehensive prompt for LLM to analyze and create standups"""
        
        prompt = f"""
You are an AI assistant that generates daily standup reports for software developers based on their Git commit history and Pull Request data.

TASK: Analyze the following commit history data and generate individual standup reports for ALL users in the system, focusing on their activity from {self.yesterday_date}.

COMMIT HISTORY DATA:
{json.dumps(commit_data, indent=2)}

TARGET DATE FOR ANALYSIS: {self.yesterday_date}

IMPORTANT: Return ONLY valid JSON in this exact structure (no additional text, explanations, or markdown):

{{
  "standup_date": "{self.yesterday_date}",
  "generated_at": "{datetime.now().isoformat()}",
  "total_users_analyzed": <number>,
  "active_users_count": <number>,
  "inactive_users_count": <number>,
  "users": [
    {{
      "username": "<exact_username_from_data>",
      "email": "<user_email_if_available>",
      "was_active": <true/false>,
      "activity_summary": {{
        "commits_count": <number>,
        "files_changed": <number>,
        "lines_added": <number>,
        "lines_deleted": <number>,
        "prs_worked_on": <number>
      }},
      "standup_report": {{
        "what_i_did_yesterday": [
          "<specific task or feature worked on>",
          "<another task completed>",
          "<include commit details and metrics>"
        ],
        "blockers": [
          "<identified blocker or impediment>",
          "<another potential blocker>"
        ],
        "what_im_working_on_today": [
          "<planned task for today>",
          "<next steps for ongoing work>",
          "<follow-up actions needed>"
        ]
      }},
      "insights": [
        "<insight about user's productivity>",
        "<insight about work patterns>",
        "<insight about potential issues or achievements>"
      ]
    }}
  ],
  "team_insights": {{
    "overall_productivity": "<assessment>",
    "team_velocity": "<high/medium/low>",
    "collaboration_level": "<assessment>",
    "potential_bottlenecks": [
      "<identified team-level bottleneck>",
      "<another potential issue>"
    ],
    "recommendations": [
      "<recommendation for team improvement>",
      "<suggestion for workflow optimization>"
    ]
  }}
}}

SMART BLOCKER IDENTIFICATION RULES:

For ACTIVE users, identify realistic blockers based on actual patterns in their work:

1. **PR Status Blockers (if data shows open PRs):**
   - If PRs are still "open" → "Waiting for code review approval"
   - If PRs have "requested_reviewers" → "Waiting for review from [reviewer names]"
   - If PRs have merge conflicts → "Resolving merge conflicts in PR #[number]"

2. **Work Pattern Blockers (if commit patterns suggest issues):**
   - Multiple small commits on same file → "Debugging complex issue in [filename]"
   - Reverted commits → "Addressing regression from previous changes"
   - Commits with "fix", "bug", "error" in messages → "Investigating production issue"
   - Commits touching test files → "Fixing failing tests before feature completion"

3. **Only add blockers if evidence exists in the data. If user completed their work cleanly (like merged PRs), they may have NO blockers:**
   - Empty blockers array [] is perfectly acceptable for users who completed their tasks successfully

For INACTIVE users (no commits on target date):
   - **DEFAULT: Leave blockers empty []** - they may simply not be working that day
   - Only add blockers if you have evidence from recent commit history suggesting ongoing challenges
   - Common scenarios for empty blockers: vacation, sick day, working on non-code tasks, meetings, etc.

ANALYSIS GUIDELINES:

1. IDENTIFY ALL USERS: Extract every user from the "users" section regardless of activity on {self.yesterday_date}.

2. FOR ACTIVE USERS (committed on {self.yesterday_date}):
   - Analyze commits, PRs, and code changes
   - Extract specific work accomplished
   - Include quantitative metrics
   - **MANDATORY: Identify at least 1-2 realistic blockers based on the patterns above**
   - Suggest logical next steps

3. FOR INACTIVE USERS (no commits on {self.yesterday_date}):
   - Set "was_active": false
   - Set activity_summary fields to 0
   - Set standup_report arrays to empty: []
   - Add insight about inactivity

4. TECHNICAL ANALYSIS:
   - Focus on actual development work
   - Identify bug fixes, features, improvements
   - Look for PR status indicators
   - Assess commit patterns for blockers
   - Consider dependencies and external factors

5. INSIGHTS GENERATION:
   - Provide actionable observations about each user
   - Identify productivity patterns
   - Note collaboration indicators
   - Highlight achievements or concerns

6. TEAM-LEVEL ANALYSIS:
   - Assess overall team productivity
   - Identify collaboration patterns
   - Spot potential bottlenecks
   - Provide improvement recommendations

REMEMBER: 
- Blockers should reflect REAL impediments based on data patterns
- Empty blockers [] is perfectly valid for users who completed their work successfully
- Don't force blockers where none exist - this makes the standup less useful
- Only add blockers when you have evidence from the commit/PR data that suggests actual blocking issues

Return ONLY the JSON object with no additional formatting or explanations.
"""
        
        return prompt
    
    def call_llama_api(self, prompt):
        """Call Llama API to generate standup content"""
        try:
            print("🤖 Calling Llama API to generate standups...")
            
            response = self.llama_client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior software engineering manager and data analyst with extensive experience in identifying development blockers and impediments. You MUST respond with ONLY valid JSON output. Do not include any explanatory text, markdown formatting, or code blocks. Return only the raw JSON object as specified in the user prompt. Generate detailed insights about developer productivity, team dynamics, and workflow optimization based on Git commit patterns. IMPORTANT: Only identify blockers when there is actual evidence of impediments in the data - empty blockers arrays are perfectly acceptable for users who completed their work successfully."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract content from Llama API response
            if hasattr(response, 'completion_message'):
                completion_msg = response.completion_message
                if hasattr(completion_msg, 'content'):
                    content = completion_msg.content
                    if hasattr(content, 'text'):
                        return content.text
                    else:
                        return str(content)
            
            return str(response.__dict__)
            
        except Exception as e:
            print(f"❌ Error calling Llama API: {str(e)}")
            return None
    
    def parse_and_validate_json(self, response_text):
        """Parse and validate the JSON response from LLM"""
        
        try:
            # Clean the response text in case there are extra characters
            cleaned_text = response_text.strip()
            
            # Remove potential markdown code blocks if present
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text.replace('```json', '').replace('```', '').strip()
            elif cleaned_text.startswith('```'):
                cleaned_text = cleaned_text.replace('```', '').strip()
            
            # Parse JSON
            parsed_json = json.loads(cleaned_text)
            
            print("✅ Valid JSON received from LLM")
            return parsed_json
            
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON response from LLM: {str(e)}")
            print(f"Raw response: {response_text[:500]}...")
            return None
    
    def validate_blockers(self, standup_data):
        """Validate blockers and only add realistic ones where evidence suggests blocking issues"""
        
        # Only add blockers for users who show signs of actual blocking issues
        technical_blocker_keywords = ['fix', 'bug', 'error', 'debug', 'issue', 'problem', 'failing', 'broken']
        
        for user in standup_data.get('users', []):
            blockers = user.get('standup_report', {}).get('blockers', [])
            
            # Only add fallback blockers if user was active AND shows signs of blocking issues
            if not blockers and user.get('was_active', False):
                
                # Check if user's work suggests blocking issues
                work_items = user.get('standup_report', {}).get('what_i_did_yesterday', [])
                has_blocking_indicators = any(
                    any(keyword in item.lower() for keyword in technical_blocker_keywords)
                    for item in work_items
                )
                
                # Only add blockers if there are indicators of technical challenges
                if has_blocking_indicators:
                    realistic_blockers = [
                        "Debugging complex technical issue",
                        "Investigating failing test cases"
                    ]
                    import random
                    user['standup_report']['blockers'] = [random.choice(realistic_blockers)]
                    print(f"🔧 Added blocker for user with technical challenges: {user.get('username', 'Unknown')}")
                else:
                    # Leave blockers empty for users who completed work successfully
                    print(f"✅ No blockers needed for user who completed work successfully: {user.get('username', 'Unknown')}")
            
            # For inactive users, keep blockers empty (they might be on vacation, in meetings, etc.)
            if not user.get('was_active', False):
                user['standup_report']['blockers'] = []
                print(f"💤 No blockers for inactive user: {user.get('username', 'Unknown')}")
        
        return standup_data
    
    def save_standup_report(self, standup_data, output_file="ai_standup_report.json"):
        """Save the generated standup report to JSON and markdown files"""
        try:
            # Save JSON version
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(standup_data, f, indent=2, ensure_ascii=False)
            print(f"✅ JSON standup report saved to: {output_file}")
            
            # Also save a readable markdown version
            markdown_filename = output_file.replace('.json', '.md')
            self.save_markdown_report(standup_data, markdown_filename)
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
    
    def save_markdown_report(self, standup_data, filename):
        """Save a human-readable markdown version of the standup report"""
        
        try:
            markdown_content = f"""# Daily Standup Report - {standup_data.get('standup_date', 'Unknown')}

Generated on: {standup_data.get('generated_at', 'Unknown')}

## Team Summary
- **Total Users Analyzed**: {standup_data.get('total_users_analyzed', 'N/A')}
- **Active Users**: {standup_data.get('active_users_count', 'N/A')}
- **Inactive Users**: {standup_data.get('inactive_users_count', 'N/A')}

---

## Individual Standups

"""
            
            # Add individual user standups
            for user in standup_data.get('users', []):
                username = user.get('username', 'Unknown')
                was_active = user.get('was_active', False)
                
                markdown_content += f"### {username}\n\n"
                
                if was_active:
                    # Activity summary
                    activity = user.get('activity_summary', {})
                    markdown_content += f"**Activity Summary:**\n"
                    markdown_content += f"- Commits: {activity.get('commits_count', 0)}\n"
                    markdown_content += f"- Files Changed: {activity.get('files_changed', 0)}\n"
                    markdown_content += f"- Lines Added: {activity.get('lines_added', 0)}\n"
                    markdown_content += f"- Lines Deleted: {activity.get('lines_deleted', 0)}\n"
                    markdown_content += f"- PRs Worked On: {activity.get('prs_worked_on', 0)}\n\n"
                    
                    # Standup report
                    report = user.get('standup_report', {})
                    
                    markdown_content += "**What I Did Yesterday:**\n"
                    for task in report.get('what_i_did_yesterday', []):
                        markdown_content += f"- {task}\n"
                    markdown_content += "\n"
                    
                    markdown_content += "**Blockers:**\n"
                    blockers = report.get('blockers', [])
                    if blockers:
                        for blocker in blockers:
                            markdown_content += f"- {blocker}\n"
                    else:
                        markdown_content += "- No major blockers\n"
                    markdown_content += "\n"
                    
                    markdown_content += "**What I'm Working On Today:**\n"
                    for task in report.get('what_im_working_on_today', []):
                        markdown_content += f"- {task}\n"
                    markdown_content += "\n"
                    
                    # Insights
                    markdown_content += "**Insights:**\n"
                    for insight in user.get('insights', []):
                        markdown_content += f"- {insight}\n"
                    
                else:
                    markdown_content += "*No updates from yesterday*\n\n"
                    
                    # Show blockers even for inactive users
                    report = user.get('standup_report', {})
                    blockers = report.get('blockers', [])
                    if blockers:
                        markdown_content += "**Current Blockers:**\n"
                        for blocker in blockers:
                            markdown_content += f"- {blocker}\n"
                
                markdown_content += "\n---\n\n"
            
            # Team insights
            team_insights = standup_data.get('team_insights', {})
            markdown_content += """## Team Insights

"""
            markdown_content += f"**Overall Productivity**: {team_insights.get('overall_productivity', 'N/A')}\n"
            markdown_content += f"**Team Velocity**: {team_insights.get('team_velocity', 'N/A')}\n"
            markdown_content += f"**Collaboration Level**: {team_insights.get('collaboration_level', 'N/A')}\n\n"
            
            markdown_content += "**Potential Bottlenecks:**\n"
            for bottleneck in team_insights.get('potential_bottlenecks', []):
                markdown_content += f"- {bottleneck}\n"
            markdown_content += "\n"
            
            markdown_content += "**Recommendations:**\n"
            for recommendation in team_insights.get('recommendations', []):
                markdown_content += f"- {recommendation}\n"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"✅ Readable markdown report saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving markdown report: {e}")
    
    def display_summary(self, standup_data):
        """Display a summary of the standup data"""
        print("\n" + "=" * 80)
        print(f"📋 STANDUP SUMMARY - {standup_data.get('standup_date', 'Unknown')}")
        print("=" * 80)
        
        print(f"👥 Total Users: {standup_data.get('total_users_analyzed', 'N/A')}")
        print(f"✅ Active Users: {standup_data.get('active_users_count', 'N/A')}")
        print(f"💤 Inactive Users: {standup_data.get('inactive_users_count', 'N/A')}")
        
        print("\n📊 ACTIVE USERS SUMMARY:")
        print("-" * 40)
        
        for user in standup_data.get('users', []):
            if user.get('was_active', False):
                activity = user.get('activity_summary', {})
                blockers_count = len(user.get('standup_report', {}).get('blockers', []))
                print(f"• {user.get('username', 'Unknown')}: {activity.get('commits_count', 0)} commits, "
                      f"{activity.get('files_changed', 0)} files, "
                      f"+{activity.get('lines_added', 0)}/-{activity.get('lines_deleted', 0)} lines, "
                      f"{blockers_count} blockers")
        
        team_insights = standup_data.get('team_insights', {})
        print(f"\n🔍 Team Velocity: {team_insights.get('team_velocity', 'N/A')}")
        print(f"🤝 Collaboration: {team_insights.get('collaboration_level', 'N/A')}")
        print(f"📈 Productivity: {team_insights.get('overall_productivity', 'N/A')}")
    
    def run(self):
        """Main execution function"""
        print("🚀 AI-Powered Standup Generator (JSON Output) - Enhanced Blocker Detection")
        print("=" * 80)
        
        # Check API key
        if not os.environ.get("LLAMA_API_KEY"):
            print("❌ Error: LLAMA_API_KEY not found in environment variables")
            print("Please make sure your .env file contains: LLAMA_API_KEY=your_api_key")
            return
        
        # Load commit data
        print("📂 Loading commit data...")
        commit_data = self.load_commit_data()
        
        if not commit_data:
            return
        
        print(f"✅ Loaded commit data with {commit_data.get('total_commits', 0)} total commits")
        
        # Generate the comprehensive prompt
        print("📝 Generating analysis prompt...")
        prompt = self.generate_standup_prompt(commit_data)
        
        # Call LLM to generate standups
        raw_response = self.call_llama_api(prompt)
        
        if raw_response:
            # Parse and validate JSON response
            standup_data = self.parse_and_validate_json(raw_response)
            
            if standup_data:
                # Validate and add fallback blockers if needed
                standup_data = self.validate_blockers(standup_data)
                
                print("✅ Standup analysis completed successfully!")
                
                # Display summary
                self.display_summary(standup_data)
                
                # Save to files
                self.save_standup_report(standup_data)
                
                print(f"\n✅ Standup reports generated successfully!")
                print(f"📄 JSON output: ai_standup_report.json")
                print(f"📖 Readable format: ai_standup_report.md")
                
            else:
                print("❌ Failed to parse JSON response from LLM")
                print("Raw response saved for debugging...")
                with open("raw_standup_response.txt", "w") as f:
                    f.write(raw_response)
        else:
            print("❌ Failed to generate standup reports")
        return standup_data

def main():
    """Main function"""
    # Configuration
    COMMIT_JSON_FILE = "github_analysis_output/commit_history_with_prs_last_30_days.json"
    YESTERDAY_DATE = "2024-05-26"  # Change this to the date you want to analyze
    
    print("🔍 AI Standup Generator with Enhanced Blocker Detection")
    print("=" * 60)
    print(f"📁 Input file: {COMMIT_JSON_FILE}")
    print(f"📅 Target date: {YESTERDAY_DATE}")
    print()
    
    generator = SimpleStandupGenerator(
        commit_json_file=COMMIT_JSON_FILE,
        yesterday_date=YESTERDAY_DATE
    )
    
    analysis = generator.run()
    return analysis

if __name__ == "__main__":
    main()