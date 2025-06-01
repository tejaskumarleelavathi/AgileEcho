import os
import json
from datetime import datetime
from dotenv import load_dotenv
from llama_api_client import LlamaAPIClient

# Load environment variables
load_dotenv()

class MilestoneRetrospectiveGenerator:
    def __init__(self, shipped_milestones_json_file):
        self.shipped_milestones_json_file = shipped_milestones_json_file
        self.llama_client = LlamaAPIClient(
            api_key=os.environ.get("LLAMA_API_KEY"),
            base_url="https://api.llama.com/v1/",
        )
        
    def load_milestone_data(self):
        """Load the shipped milestones commit history JSON"""
        try:
            with open(self.shipped_milestones_json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: File '{self.shipped_milestones_json_file}' not found")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in '{self.shipped_milestones_json_file}': {str(e)}")
            return None
    
    def get_latest_shipped_milestone(self, milestone_data):
        """Identify the most recent shipped milestone"""
        shipped_milestones = milestone_data.get('shipped_milestones', {})
        
        if not shipped_milestones:
            return None, None
        
        # Find the most recent milestone based on closed_at date
        latest_milestone = None
        latest_date = None
        
        for milestone_name, milestone_info in shipped_milestones.items():
            milestone_meta = milestone_info.get('milestone_info', {})
            closed_at = milestone_meta.get('closed_at')
            
            if closed_at:
                try:
                    closed_date = datetime.fromisoformat(closed_at.replace('Z', '+00:00'))
                    if latest_date is None or closed_date > latest_date:
                        latest_date = closed_date
                        latest_milestone = milestone_name
                except:
                    continue
        
        # If no closed_at dates, just take the first one
        if latest_milestone is None:
            latest_milestone = list(shipped_milestones.keys())[0]
        
        return latest_milestone, shipped_milestones.get(latest_milestone)
    
    def generate_retrospective_prompt(self, milestone_name, milestone_data, full_context):
        """Generate a comprehensive retrospective prompt for Llama API"""
        
        # Convert milestone data to JSON string to avoid f-string conflicts
        milestone_data_json = json.dumps(full_context, indent=2)
        
        prompt = """
You are an experienced Agile Coach and Scrum Master facilitating a sprint retrospective meeting. You have been provided with detailed commit history and development data for the recently shipped milestone.

Your task is to analyze this data and generate comprehensive retrospective insights that would typically be discussed in a team retrospective meeting.

MILESTONE DATA FOR ANALYSIS:
""" + milestone_data_json + """

RETROSPECTIVE FOCUS:
Please conduct a thorough retrospective analysis for the latest shipped milestone and provide insights in the following structured format used in professional retrospective meetings:

## 🎯 MILESTONE OVERVIEW
- Milestone name and completion details
- Timeline (start to completion)
- Scope and key deliverables achieved
- Overall team performance summary

## ✅ WHAT WENT WELL (Positives/Wins)
Analyze the data to identify:
- High-performing team members and their contributions
- Efficient development patterns (quick PR turnarounds, clean commits)
- Successful collaboration indicators
- Features/PRs that were delivered smoothly
- Good practices that should be continued
- Technical achievements and innovations
- Process improvements that worked

## 🚧 WHAT DIDN'T GO WELL (Pain Points/Challenges)
Identify areas of concern:
- Development bottlenecks or delays
- PRs that took unusually long
- Commits patterns indicating struggles or rework
- Uneven workload distribution
- Technical debt introduced
- Communication or coordination issues
- Process breakdowns or inefficiencies

## 🔍 WHAT WE LEARNED (Insights/Discoveries)
Extract key learnings:
- Technical insights gained during development
- Process learnings and team dynamics observations
- Patterns in commit/PR data that reveal team behavior
- Skills development and knowledge sharing evidence
- Unexpected challenges and how they were overcome
- Best practices that emerged during the milestone

## 🎯 ACTION ITEMS (Improvements for Next Sprint)
Based on your analysis, suggest specific, actionable improvements:
- Process improvements (development workflow, review process, etc.)
- Technical improvements (code quality, architecture, tools)
- Team collaboration enhancements
- Individual development goals
- Tools or infrastructure changes needed
- Communication and coordination improvements

## 📊 TEAM PERFORMANCE METRICS
Provide data-driven insights:
- Commit frequency and patterns analysis
- PR review and merge time analysis
- Code contribution distribution
- Active development days per team member
- Productivity patterns and trends
- Quality indicators (commit message quality, PR sizes, etc.)

## 🏆 INDIVIDUAL CONTRIBUTIONS & RECOGNITION
Highlight individual team member contributions:
- Top contributors and their key achievements
- Emerging leaders and mentors
- Skill development evidence
- Collaboration and support activities
- Areas where team members excelled

## 📈 MILESTONE SUCCESS CRITERIA
Evaluate against typical success metrics:
- Delivery timeline adherence
- Quality of deliverables
- Team velocity and productivity
- Technical debt management
- Stakeholder satisfaction indicators
- Process adherence and improvements

OUTPUT FORMAT:
You MUST respond with ONLY a valid JSON object in this exact format:

{
  "generated_on": "2025-06-01 10:30:00",
  "milestone": "milestone_name_here",
  "repository": "microsoft/vscode-cosmosdb",
  "retrospective": "Your complete retrospective analysis here with all the sections above. Include all the markdown formatting, emojis, and structure as requested. This should be the complete retrospective content that would be used in a team meeting."
}

IMPORTANT: 
- Fill in ALL the JSON fields yourself based on the data provided
- The retrospective field should contain the complete analysis with all 8 sections
- Include the milestone name from the data
- Add the current date/time
- Return ONLY valid JSON with no additional text, markdown formatting, or code blocks
- Do not add any extra fields or modify the structure

Please generate the retrospective insights now:
"""
        
        return prompt
    
    def call_llama_api(self, prompt):
        """Call Llama API to generate retrospective insights"""
        try:
            print("🤖 Calling Llama API to generate retrospective insights...")
            
            response = self.llama_client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Agile Coach and Scrum Master with extensive experience facilitating retrospective meetings. You excel at analyzing development data to provide actionable insights for team improvement. You understand software development workflows, team dynamics, and continuous improvement practices. You MUST respond with valid JSON only, no additional text or markdown formatting."
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
    
    def save_retrospective_report(self, retrospective_content, milestone_name, output_file=None):
        """Save the LLM-generated JSON directly"""
        if output_file is None:
            safe_milestone_name = milestone_name.replace(' ', '_').replace(':', '').replace('.', '_')
            output_file = f"retrospective_{safe_milestone_name}.json"
        
        try:
            # Clean up the response - remove markdown code blocks if present
            cleaned_content = retrospective_content.strip()
            
            # Remove ```json and ``` markers if present
            if cleaned_content.startswith('```json'):
                cleaned_content = cleaned_content[7:]
            if cleaned_content.startswith('```'):
                cleaned_content = cleaned_content[3:]
            if cleaned_content.endswith('```'):
                cleaned_content = cleaned_content[:-3]
            
            cleaned_content = cleaned_content.strip()
            
            # Try to parse as JSON to validate, then save as-is
            try:
                json.loads(cleaned_content)  # Just validate, don't modify
                
                # Save the LLM's JSON directly
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                print(f"✅ Retrospective report saved to: {output_file}")
                
            except json.JSONDecodeError:
                # If not valid JSON, create error structure
                error_report = {
                    "error": "LLM did not return valid JSON format",
                    "raw_response": cleaned_content
                }
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(error_report, f, indent=2)
                print(f"⚠️ Error in JSON format. Raw response saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
    
    def display_retrospective(self, retrospective_content):
        """Display retrospective content"""
        try:
            # Clean up the response
            cleaned_content = retrospective_content.strip()
            
            if cleaned_content.startswith('```json'):
                cleaned_content = cleaned_content[7:]
            if cleaned_content.startswith('```'):
                cleaned_content = cleaned_content[3:]
            if cleaned_content.endswith('```'):
                cleaned_content = cleaned_content[:-3]
            
            cleaned_content = cleaned_content.strip()
            
            retrospective_json = json.loads(cleaned_content)
            
            print("📋 RETROSPECTIVE CONTENT:")
            print(retrospective_json.get('retrospective', 'No retrospective content provided'))
            
        except json.JSONDecodeError:
            print("⚠️ LLM response was not valid JSON. Raw response:")
            print(retrospective_content)
    
    def run(self):
        """Main execution function"""
        print("🚀 Milestone Retrospective Insights Generator")
        print("=" * 60)
        
        # Check API key
        if not os.environ.get("LLAMA_API_KEY"):
            print("❌ Error: LLAMA_API_KEY not found in environment variables")
            print("Please make sure your .env file contains: LLAMA_API_KEY=your_api_key")
            return
        
        # Load milestone data
        print("📂 Loading shipped milestone data...")
        milestone_data = self.load_milestone_data()
        
        if not milestone_data:
            return
        
        total_milestones = len(milestone_data.get('shipped_milestones', {}))
        print(f"✅ Loaded data for {total_milestones} shipped milestones")
        
        # Get the latest shipped milestone
        print("🎯 Identifying latest shipped milestone...")
        latest_milestone_name, latest_milestone_data = self.get_latest_shipped_milestone(milestone_data)
        
        if not latest_milestone_name:
            print("❌ No shipped milestones found in the data")
            return
        
        print(f"📋 Latest shipped milestone: {latest_milestone_name}")
        print(f"📊 Milestone stats:")
        print(f"   - Total commits: {latest_milestone_data.get('total_commits', 0)}")
        print(f"   - Total PRs: {latest_milestone_data.get('total_prs', 0)}")
        print(f"   - Contributors: {len(latest_milestone_data.get('users', {}))}")
        
        # Generate the comprehensive retrospective prompt
        print("📝 Generating retrospective analysis prompt...")
        prompt = self.generate_retrospective_prompt(latest_milestone_name, latest_milestone_data, milestone_data)
        
        # Call LLM to generate retrospective insights
        retrospective_content = self.call_llama_api(prompt)
        
        if retrospective_content:
            print("\n" + "=" * 80)
            print(f"📋 RETROSPECTIVE INSIGHTS - {latest_milestone_name}")
            print("=" * 80)
            
            # Display formatted retrospective
            self.display_retrospective(retrospective_content)
            
            print("=" * 80)
            
            # Save to file
            self.save_retrospective_report(retrospective_content, latest_milestone_name)
            
            print(f"\n✅ Retrospective insights generated successfully!")
            print(f"🎯 Focus milestone: {latest_milestone_name}")
            print(f"📈 Ready for team retrospective meeting!")
        else:
            print("❌ Failed to generate retrospective insights")

def main():
    """Main function"""
    # Configuration
    SHIPPED_MILESTONES_JSON = "github_analysis_output/shipped_milestones_commit_history.json"
    
    print("🔍 AI-Powered Milestone Retrospective Generator")
    print("=" * 50)
    print(f"📁 Input file: {SHIPPED_MILESTONES_JSON}")
    print()
    
    generator = MilestoneRetrospectiveGenerator(
        shipped_milestones_json_file=SHIPPED_MILESTONES_JSON
    )
    
    generator.run()

if __name__ == "__main__":
    main()