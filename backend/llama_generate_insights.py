import os
import json
from dotenv import load_dotenv
from llama_api_client import LlamaAPIClient

# Load environment variables
load_dotenv()

def load_json_file(filename):
    """Load and return JSON data from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{filename}': {str(e)}")
        return None

def generate_analysis_prompt(json1_data, json2_data):
    """Generate a focused prompt with raw JSON data"""
    
    # Limit the JSON size by taking only first 50 issues from each if they're too large
    json1_sample = json1_data
    json2_sample = json2_data
    
    if 'issues' in json1_data and len(json1_data['issues']) > 50:
        json1_sample = {**json1_data, 'issues': json1_data['issues'][:50]}
        
    if 'issues' in json2_data and len(json2_data['issues']) > 50:
        json2_sample = {**json2_data, 'issues': json2_data['issues'][:50]}
    
    prompt = f"""
Analyze these GitHub issues from microsoft/vscode-cosmosdb project and provide ONLY valid JSON output:

DATASET 1 (Project Summary):
{json.dumps(json1_sample, indent=1)}

DATASET 2 (Specific Issues):
{json.dumps(json2_sample, indent=1)}

IMPORTANT: Return ONLY valid JSON in this exact structure (no additional text, explanations, or markdown):

{{
  "open_vs_closed": {{
    "total_issues": <number>,
    "open_issues": <number>,
    "closed_issues": <number>,
    "resolution_rate_percentage": <number>,
    "health_status": "<good/fair/poor>",
    "insights": [
      "<insight about open vs closed ratio>",
      "<insight about resolution trends>",
      "<insight about workload management>"
    ]
  }},
  "critical_issues_status": {{
    "total_critical": <number>,
    "critical_open": <number>,
    "critical_closed": <number>,
    "critical_issue_titles": ["<issue_number1> : <title1>", " <issue_number1> :<title2>"],
    "insights": [
      "<insight about critical issue handling>",
      "<insight about priority management>",
      "<insight about critical issue patterns>"
    ]
  }},
  "current_sprint_status": {{
    "milestone": "0.26.1",
    "total_milestone_issues": <number>,
    "milestone_open": <number>,
    "milestone_closed": <number>,
    "completion_percentage": <number>,
    "insights": [
      "<insight about sprint progress>",
      "<insight about milestone completion likelihood>",
      "<insight about sprint velocity>"
    ]
  }},
  "external_blockers_impact": {{
    "total_blocked_issues": <number>,
    "blocked_issue_titles": [<number>: "<title1>",<number>: "<title2>"],
    "impact_level": "<high/medium/low>",
    "insights": [
      "<insight about blocker impact on delivery>",
      "<insight about dependency risks>",
      "<insight about external coordination needs>"
    ],
    "days_blocked": <number>
    "priority":"P0/P1/P2/P3"
  }},
  "external_blocker_breakdown": [
    {{
      "risk_level": "<high/medium/low>",
      "blocker_type": "<dependency_name>",
      "affected_issues_count": <number>,
      "blocker_issue_titles": [<number>: "<title1>",<number>: "<title2>"],
      "mitigation_strategy": "<strategy_description>",
      "insights": [
        "<insight about this specific blocker>",
        "<insight about mitigation effectiveness>"
      ]
      
    }}
  ],
  "summary": {{
    "overall_health": "<assessment>",
    "key_concerns": ["<concern1>", "<concern2>"],
    "recommended_actions": ["<action1>", "<action2>"],
    "strategic_insights": [
      "<high-level insight about project trajectory>",
      "<insight about resource allocation>",
      "<insight about process improvements>",
      "<insight about stakeholder communication needs>"
    ]
  }}
}}
"""
    
    return prompt

def call_llama_api(prompt):
    """Call Llama API with the generated prompt"""
    
    try:
        # Initialize Llama API client
        client = LlamaAPIClient(
            api_key=os.environ.get("LLAMA_API_KEY"),
            base_url="https://api.llama.com/v1/",
        )
        
        print("🤖 Calling Llama API for analysis...")
        
        response = client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a senior software project analyst with deep expertise in GitHub project management and issue tracking. You MUST respond with ONLY valid JSON output. Do not include any explanatory text, markdown formatting, or code blocks. Return only the raw JSON object as specified in the user prompt. For each section, provide actionable insights based on data patterns, trends, and potential risks or opportunities. Your insights should be specific, data-driven, and immediately useful for project managers and development teams."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        
        # Extract content from the specific Llama API response format
        if hasattr(response, 'completion_message'):
            completion_msg = response.completion_message
            if hasattr(completion_msg, 'content'):
                content = completion_msg.content
                if hasattr(content, 'text'):
                    return content.text
                else:
                    return str(content)
        
        # Fallback to string representation
        return str(response._dict_)
        
    except Exception as e:
        print(f"❌ Error calling Llama API: {str(e)}")
        return None

def parse_and_validate_json(response_text):
    """Parse and validate the JSON response from LLM"""
    
    try:
        # Clean the response text in case there are extra characters
        cleaned_text = response_text.strip()
        
        # Remove potential markdown code blocks if present
        if cleaned_text.startswith('⁠  json'):
            cleaned_text = cleaned_text.replace('  ⁠json', '').replace('⁠  ', '').strip()
        elif cleaned_text.startswith('  ⁠'):
            cleaned_text = cleaned_text.replace('```', '').strip()
        
        # Parse JSON
        parsed_json = json.loads(cleaned_text)
        
        print("✅ Valid JSON received from LLM")
        return parsed_json
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON response from LLM: {str(e)}")
        print(f"Raw response: {response_text[:500]}...")
        return None

def save_analysis_report(analysis_data, filename="llama_analysis_report.json"):
    """Save the analysis report to a JSON file"""
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Analysis report saved to: {filename}")
        
        # Also save a readable markdown version
        markdown_filename = filename.replace('.json', '.md')
        save_markdown_report(analysis_data, markdown_filename)
        
    except Exception as e:
        print(f"❌ Error saving report: {str(e)}")

def save_markdown_report(analysis_data, filename):
    """Save a human-readable markdown version of the analysis"""
    
    try:
        markdown_content = f"""# GitHub Issues Analysis Report

## Open vs Closed Issues
•⁠  ⁠*Total Issues*: {analysis_data.get('open_vs_closed', {}).get('total_issues', 'N/A')}
•⁠  ⁠*Open Issues*: {analysis_data.get('open_vs_closed', {}).get('open_issues', 'N/A')}
•⁠  ⁠*Closed Issues*: {analysis_data.get('open_vs_closed', {}).get('closed_issues', 'N/A')}
•⁠  ⁠*Resolution Rate*: {analysis_data.get('open_vs_closed', {}).get('resolution_rate_percentage', 'N/A')}%
•⁠  ⁠*Health Status*: {analysis_data.get('open_vs_closed', {}).get('health_status', 'N/A')}

### Insights:
{chr(10).join(['- ' + insight for insight in analysis_data.get('open_vs_closed', {}).get('insights', [])])}

## Critical Issues Status
•⁠  ⁠*Total Critical Issues*: {analysis_data.get('critical_issues_status', {}).get('total_critical', 'N/A')}
•⁠  ⁠*Critical Open*: {analysis_data.get('critical_issues_status', {}).get('critical_open', 'N/A')}
•⁠  ⁠*Critical Closed*: {analysis_data.get('critical_issues_status', {}).get('critical_closed', 'N/A')}

### Insights:
{chr(10).join(['- ' + insight for insight in analysis_data.get('critical_issues_status', {}).get('insights', [])])}

## Current Sprint (0.26.1) Status
•⁠  ⁠*Total Issues*: {analysis_data.get('current_sprint_status', {}).get('total_milestone_issues', 'N/A')}
•⁠  ⁠*Open*: {analysis_data.get('current_sprint_status', {}).get('milestone_open', 'N/A')}
•⁠  ⁠*Closed*: {analysis_data.get('current_sprint_status', {}).get('milestone_closed', 'N/A')}
•⁠  ⁠*Completion*: {analysis_data.get('current_sprint_status', {}).get('completion_percentage', 'N/A')}%

### Insights:
{chr(10).join(['- ' + insight for insight in analysis_data.get('current_sprint_status', {}).get('insights', [])])}

## External Blockers
•⁠  ⁠*Total Blocked Issues*: {analysis_data.get('external_blockers_impact', {}).get('total_blocked_issues', 'N/A')}
•⁠  ⁠*Impact Level*: {analysis_data.get('external_blockers_impact', {}).get('impact_level', 'N/A')}

### Insights:
{chr(10).join(['- ' + insight for insight in analysis_data.get('external_blockers_impact', {}).get('insights', [])])}

## External Blocker Breakdown
{chr(10).join([f"### {blocker.get('blocker_type', 'Unknown')} ({blocker.get('affected_issues_count', 0)} issues)" + chr(10) + 
              f"*Mitigation Strategy*: {blocker.get('mitigation_strategy', 'N/A')}" + chr(10) + 
              "*Insights*:" + chr(10) + 
              chr(10).join(['- ' + insight for insight in blocker.get('insights', [])]) + chr(10)
              for blocker in analysis_data.get('external_blocker_breakdown', [])])}

## Summary
*Overall Health*: {analysis_data.get('summary', {}).get('overall_health', 'N/A')}

### Key Concerns:
{chr(10).join(['- ' + concern for concern in analysis_data.get('summary', {}).get('key_concerns', [])])}

### Recommended Actions:
{chr(10).join(['- ' + action for action in analysis_data.get('summary', {}).get('recommended_actions', [])])}

### Strategic Insights:
{chr(10).join(['- ' + insight for insight in analysis_data.get('summary', {}).get('strategic_insights', [])])}
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"✅ Readable report saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error saving markdown report: {str(e)}")

def main():
    """Main function to orchestrate the analysis"""
    
    print("🚀 Starting GitHub Issues Analysis with Llama API (JSON Output)")
    print("=" * 70)
    
    # Check if API key is available
    if not os.environ.get("LLAMA_API_KEY"):
        print("❌ Error: LLAMA_API_KEY not found in environment variables")
        print("Please make sure your .env file contains: LLAMA_API_KEY=your_api_key")
        return
    
    # Load JSON files
    print("📂 Loading JSON files...")
    
    json1_data = load_json_file("agentic_analysis_results.json")
    if not json1_data:
        return
    
    json2_data = load_json_file("specific_vscode_cosmosdb_issues.json")
    if not json2_data:
        return
    
    print("✅ JSON files loaded successfully")
    
    # Generate analysis prompt
    print("📝 Generating analysis prompt...")
    prompt = generate_analysis_prompt(json1_data, json2_data)
    
    # Call Llama API
    raw_response = call_llama_api(prompt)
    
    if raw_response:
        # Parse and validate JSON response
        analysis_result = parse_and_validate_json(raw_response)
        
        if analysis_result:
            print("✅ Analysis completed successfully!")
            print("\n" + "=" * 70)
            print("📊 ANALYSIS RESULTS (JSON):")
            print("=" * 70)
            print(json.dumps(analysis_result, indent=2))
            
            # Save to files
            save_analysis_report(analysis_result)
            
            # Print key metrics
            print("\n" + "=" * 70)
            print("📈 KEY METRICS:")
            print("=" * 70)
            open_vs_closed = analysis_result.get('open_vs_closed', {})
            print(f"• Open vs Closed: {open_vs_closed.get('open_issues', 'N/A')} open / {open_vs_closed.get('closed_issues', 'N/A')} closed")
            print(f"• Resolution Rate: {open_vs_closed.get('resolution_rate_percentage', 'N/A')}%")
            print(f"• Health Status: {open_vs_closed.get('health_status', 'N/A')}")
            
        else:
            print("❌ Failed to parse JSON response from LLM")
            print("Raw response saved for debugging...")
            with open("raw_llm_response.txt", "w") as f:
                f.write(raw_response)
        
    else:
        print("❌ Failed to get analysis from Llama API")
     
    return analysis_result

if __name__ == "__main__":
    main()