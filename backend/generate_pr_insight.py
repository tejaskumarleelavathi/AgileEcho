import os
import json
from datetime import datetime
from dotenv import load_dotenv
from llama_api_client import LlamaAPIClient

# Load environment variables
load_dotenv()

class PRInsightsGenerator:
    def __init__(self, pr_json_file):
        self.pr_json_file = pr_json_file
        self.llama_client = LlamaAPIClient(
            api_key=os.environ.get("LLAMA_API_KEY"),
            base_url="https://api.llama.com/v1/",
        )
        
    def load_pr_data(self):
        """Load the PR data JSON"""
        try:
            with open(self.pr_json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: File '{self.pr_json_file}' not found")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in '{self.pr_json_file}': {str(e)}")
            return None
    
    def generate_insights_prompt(self, pr_data):
        """Generate a comprehensive prompt for LLM to analyze long-running PRs"""
        
        # Convert PR data to JSON string to avoid f-string conflicts
        pr_data_json = json.dumps(pr_data, indent=2)
        
        prompt = """
You are an AI assistant that analyzes Pull Request data to identify long-running open PRs and provide actionable insights for project management and development workflow optimization.

TASK: Analyze the following PR data to identify Pull Requests that have been open for a very long time and generate insights about potential issues, bottlenecks, and recommendations.

PR DATA:
""" + pr_data_json + """

INSTRUCTIONS:

1. IDENTIFY LONG-RUNNING OPEN PRS:
   - Look through all pull requests in the data
   - Focus on PRs with state "open" (not closed or merged)
   - Consider PRs that have been open for MORE THAN 8 DAYS as long-running and potentially problematic
   - Calculate how long each open PR has been running based on created_at vs current date
   - Only include PRs that exceed the 8-day threshold in your analysis
   - Prioritize the most concerning ones (longest running, most complex, or showing signs of being stuck)

2. ANALYZE PATTERNS AND ISSUES:
   - For each open PR, calculate the exact number of days it has been open (from created_at to current date)
   - Look at timeline events to understand what's happening with each long-running PR
   - Check for signs of:
     * Lack of review activity
     * Multiple requested changes without resolution
     * Complex PRs that might need breaking down
     * Blocked PRs waiting for external dependencies
     * PRs with conflicting feedback
     * Stale PRs that might have been abandoned
     * PRs missing critical information or approvals

3. GENERATE INSIGHTS:
   - Identify root causes for delays (review bottlenecks, technical complexity, resource constraints, etc.)
   - Suggest actionable solutions for each identified issue, considering how long each PR has been open
   - Provide recommendations for preventing similar delays in the future
   - Consider team workflow improvements, process changes, or technical solutions
   - Prioritize recommendations based on PR age and impact

4. OUTPUT FORMAT:
   Provide your analysis in EXACTLY this JSON format:

   {
     "longest_open_pr_days": X,
     "average_pr_resolution_days": Y,
     "days_threshold": 8,
     "long_running_prs": [
       {
         "pr_number": 2696,
         "days_open": 15,
         "title": "PR title here"
       },
       {
         "pr_number": 2645,
         "days_open": 23,
         "title": "PR title here"
       }
     ],
     "insight": "Your detailed analysis and recommendations here. Include which PRs are most concerning and why, common patterns or bottlenecks identified, specific recommendations for resolving current issues based on how long they've been open, suggestions for improving the overall PR workflow, and any process improvements or team coordination recommendations."
   }

   IMPORTANT: 
   - longest_open_pr_days should be the highest number of days any OPEN PR has been running
   - average_pr_resolution_days should be calculated from ALL PRs (open and closed) - average time from creation to closure/merge
   - Only include PRs in long_running_prs array that have been open for MORE THAN 8 DAYS
   - If no PRs exceed 8 days, use empty array [] for long_running_prs and mention this in the insight
   - Return ONLY valid JSON, no additional text or formatting

5. ANALYSIS GUIDELINES:
   - Focus on actionable insights, not just describing problems
   - Consider both technical and process-related issues
   - Look at the broader patterns across multiple PRs
   - Provide specific, implementable recommendations
   - Consider the impact on team productivity and project timeline
   - Include both immediate fixes and long-term improvements

6. IMPORTANT CONSIDERATIONS:
   - Only include PRs that are actually "open" (state: "open")
   - ONLY analyze PRs that have been open for MORE THAN 8 DAYS - ignore anything 8 days or less
   - Focus on PRs that represent real blockers or workflow issues
   - Consider the complexity and scope of each PR when assessing if the duration is reasonable
   - Look at recent activity to distinguish between actively worked PRs vs abandoned ones
   - If no PRs exceed the 8-day threshold, respond with empty long_running_prs array and mention this in the insight

Please analyze the data and provide insights on long-running PRs now:
"""
        
        return prompt
    
    def call_llama_api(self, prompt):
        """Call Llama API to generate PR insights"""
        try:
            print("🤖 Calling Llama API to analyze long-running PRs...")
            
            response = self.llama_client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software project manager and development workflow analyst. You excel at identifying bottlenecks in development processes, analyzing Pull Request patterns, and providing actionable insights to improve team productivity and code delivery. You MUST respond with valid JSON only, no additional text or markdown formatting."
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
    
    def save_insights_report(self, insights_content, output_file="pr_insights_report.json"):
        """Save the generated insights report to a JSON file"""
        try:
            # Clean up the response - remove markdown code blocks if present
            cleaned_content = insights_content.strip()
            
            # Remove ```json and ``` markers if present
            if cleaned_content.startswith('```json'):
                cleaned_content = cleaned_content[7:]  # Remove ```json
            if cleaned_content.startswith('```'):
                cleaned_content = cleaned_content[3:]   # Remove ```
            if cleaned_content.endswith('```'):
                cleaned_content = cleaned_content[:-3]  # Remove trailing ```
            
            cleaned_content = cleaned_content.strip()
            
            # Try to parse the cleaned content as JSON
            try:
                insights_json = json.loads(cleaned_content)
                
                # Extract only the fields you want
                filtered_report = {
                    "generated_on": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "repository": self.pr_data.get('repository', 'Unknown') if hasattr(self, 'pr_data') else 'Unknown',
                    "longest_open_pr_days": insights_json.get('longest_open_pr_days'),
                    "average_pr_resolution_days": insights_json.get('average_pr_resolution_days'),
                    "days_threshold": insights_json.get('days_threshold', 8),
                    "long_running_prs": insights_json.get('long_running_prs', []),
                    "insight": insights_json.get('insight', 'No insights provided')
                }
                
            except json.JSONDecodeError:
                # If still not valid JSON, wrap it in error structure
                filtered_report = {
                    "generated_on": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "repository": self.pr_data.get('repository', 'Unknown') if hasattr(self, 'pr_data') else 'Unknown',
                    "longest_open_pr_days": None,
                    "average_pr_resolution_days": None,
                    "days_threshold": 8,
                    "long_running_prs": [],
                    "insight": "Error: LLM did not return valid JSON format",
                    "error_details": cleaned_content
                }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(filtered_report, f, indent=2, ensure_ascii=False)
            print(f"✅ Insights report saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
    
    def display_insights(self, insights_content):
        """Display insights in a formatted way"""
        try:
            # Clean up the response - remove markdown code blocks if present
            cleaned_content = insights_content.strip()
            
            # Remove ```json and ``` markers if present
            if cleaned_content.startswith('```json'):
                cleaned_content = cleaned_content[7:]
            if cleaned_content.startswith('```'):
                cleaned_content = cleaned_content[3:]
            if cleaned_content.endswith('```'):
                cleaned_content = cleaned_content[:-3]
            
            cleaned_content = cleaned_content.strip()
            
            insights_json = json.loads(cleaned_content)
            
            print(f"\n📊 LONG-RUNNING PR ANALYSIS RESULTS:")
            print(f"🔸 Longest open PR: {insights_json.get('longest_open_pr_days', 'N/A')} days")
            print(f"🔸 Average PR resolution: {insights_json.get('average_pr_resolution_days', 'N/A')} days") 
            print(f"🔸 Threshold: {insights_json.get('days_threshold', 8)} days")
            
            long_running = insights_json.get('long_running_prs', [])
            if long_running:
                print(f"\n🚨 Long-running PRs ({len(long_running)} found):")
                for pr in long_running:
                    print(f"  • PR #{pr.get('pr_number')} - {pr.get('days_open')} days: {pr.get('title', 'No title')}")
            else:
                print(f"\n✅ No long-running PRs found (all open PRs are ≤ 8 days)")
            
            print(f"\n💡 INSIGHTS:")
            print(f"{insights_json.get('insight', 'No insights provided')}")
            
        except json.JSONDecodeError:
            print("⚠️ LLM response was not valid JSON after cleaning. Raw response:")
            print(insights_content)
    
    def run(self):
        """Main execution function"""
        print("🚀 PR Insights Generator - Long-Running PR Analysis")
        print("=" * 60)
        
        # Check API key
        if not os.environ.get("LLAMA_API_KEY"):
            print("❌ Error: LLAMA_API_KEY not found in environment variables")
            print("Please make sure your .env file contains: LLAMA_API_KEY=your_api_key")
            return
        
        # Load PR data
        print("📂 Loading PR data...")
        pr_data = self.load_pr_data()
        
        if not pr_data:
            return
        
        self.pr_data = pr_data  # Store for later use
        
        total_prs = pr_data.get('total_prs', 0)
        open_prs = len([pr for pr in pr_data.get('pull_requests', []) if pr.get('state') == 'open'])
        
        print(f"✅ Loaded PR data with {total_prs} total PRs ({open_prs} open)")
        
        # Generate the comprehensive prompt
        print("📝 Generating analysis prompt...")
        prompt = self.generate_insights_prompt(pr_data)
        
        # Call LLM to generate insights
        insights_content = self.call_llama_api(prompt)
        
        if insights_content:
            print("\n" + "=" * 80)
            print("📊 LONG-RUNNING PR INSIGHTS")
            print("=" * 80)
            
            # Display formatted insights
            self.display_insights(insights_content)
            
            print("=" * 80)
            
            # Save to file
            self.save_insights_report(insights_content)
            
            print(f"\n✅ PR insights generated successfully!")
        else:
            print("❌ Failed to generate PR insights")
        return insights_content

def main():
    """Main function"""
    # Configuration
    PR_JSON_FILE = "github_analysis_output/pull_requests_last_30_days.json"  # Change this to your PR JSON file
    
    print("🔍 Long-Running PR Insights Generator")
    print("=" * 40)
    print(f"📁 Input file: {PR_JSON_FILE}")
    print()
    
    generator = PRInsightsGenerator(pr_json_file=PR_JSON_FILE)
    analysis = generator.run()
    return analysis
if __name__ == "__main__":
    main()