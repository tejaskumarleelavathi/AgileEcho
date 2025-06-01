import json
import os
from llama_api_client import LlamaAPIClient
from dotenv import load_dotenv

load_dotenv()

class SankeyInsightsAnalyzer:
    def __init__(self):
        self.llama_client = LlamaAPIClient(
            api_key=os.environ.get("LLAMA_API_KEY"),
            base_url="https://api.llama.com/v1/",
        )
    
    def generate_insights_prompt(self, sankey_data):
        """Generate prompt to analyze Sankey data and produce insights"""
        
        prompt = f"""You are an expert data analyst. Analyze the following Sankey diagram data from a GitHub project and provide insights.

# SANKEY DATA CONTEXT:
This Sankey diagram shows the flow of GitHub issues through a development workflow:
- **Flow Structure**: Issue Types → Categories → Priority → Milestone → Team Members
- **Data**: Each connection shows how many issues flow from one stage to the next

# SANKEY DATA TO ANALYZE:
```javascript
{sankey_data}
```

# TASK: Generate EXACTLY 4 insights in JSON format

Provide your analysis in this EXACT JSON structure:

{{
  "insight_1": {{
    "title": "Brief title (5 words max)",
    "finding": "One concise sentence summarizing the key finding"
  }},
  "insight_2": {{
    "title": "Brief title (5 words max)", 
    "finding": "One concise sentence summarizing the key finding"
  }},
  "insight_3": {{
    "title": "Brief title (5 words max)",
    "finding": "One concise sentence summarizing the key finding"
  }},
  "executive_summary": {{
    "title": "Project Overview Summary",
    "explanation": "3-4 sentences explaining what this Sankey diagram shows in simple terms for someone unfamiliar with Sankey diagrams. Describe the team's workflow, main focus areas, and overall project health without using technical jargon."
  }}
}}

# ANALYSIS GUIDELINES:

**For Insights 1-3**: Focus on these areas:
1. **Workload Distribution**: How work is distributed among team members
2. **Priority Management**: How well priorities are assigned and managed  
3. **Project Focus**: What types of work dominate (bugs vs features vs categories)

**For Executive Summary**: 
- Explain what a Sankey diagram shows (flow of work through stages)
- Describe the team's main work patterns in plain English
- Highlight the biggest challenges or successes
- Make it understandable for non-technical stakeholders

# CRITICAL REQUIREMENTS:
1. Return ONLY valid JSON (no additional text)
2. Keep insights concise but specific with numbers when relevant
3. Make the executive summary accessible to non-technical readers
4. Use actual data from the Sankey connections provided

Return only the JSON object:"""
        
        return prompt
    
    def call_llama_api(self, prompt):
        """Call Llama API to generate insights"""
        try:
            print("🤖 Analyzing Sankey data for insights...")
            
            response = self.llama_client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior data analyst and project management expert. You excel at interpreting workflow data and communicating insights clearly to both technical and non-technical audiences. You MUST respond with ONLY valid JSON output. Do not include any explanatory text, markdown formatting, or code blocks. Return only the raw JSON object as specified."
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
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Remove potential markdown code blocks if present
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text.replace('```json', '').replace('```', '').strip()
            elif cleaned_text.startswith('```'):
                cleaned_text = cleaned_text.replace('```', '').strip()
            
            # Parse JSON
            parsed_json = json.loads(cleaned_text)
            
            # Validate structure
            required_keys = ['insight_1', 'insight_2', 'insight_3', 'executive_summary']
            for key in required_keys:
                if key not in parsed_json:
                    raise ValueError(f"Missing required key: {key}")
            
            print("✅ Valid JSON insights received")
            return parsed_json
            
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON response: {str(e)}")
            print(f"Raw response: {response_text[:300]}...")
            return None
        except ValueError as e:
            print(f"❌ Error: Invalid structure: {str(e)}")
            return None
    
    def save_insights_to_json(self, insights_data, output_file="sankey_insights.json"):
        """Save the insights to a JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(insights_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Insights saved to: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving insights: {str(e)}")
            return False
    
    def display_insights(self, insights_data):
        """Display the insights in a readable format"""
        print("\n" + "=" * 60)
        print("📊 SANKEY DIAGRAM INSIGHTS")
        print("=" * 60)
        
        # Display the 3 key insights
        for i in range(1, 4):
            insight_key = f"insight_{i}"
            if insight_key in insights_data:
                insight = insights_data[insight_key]
                print(f"\n🔍 INSIGHT {i}: {insight.get('title', 'N/A')}")
                print(f"   {insight.get('finding', 'N/A')}")
        
        # Display executive summary
        if 'executive_summary' in insights_data:
            summary = insights_data['executive_summary']
            print(f"\n📋 {summary.get('title', 'EXECUTIVE SUMMARY')}")
            print(f"   {summary.get('explanation', 'N/A')}")
        
        print("\n" + "=" * 60)
    
    def analyze_sankey_data(self, sankey_data_file="sankey_data.js"):
        """Main method to analyze Sankey data and generate insights"""
        
        print("🚀 Sankey Data Insights Analyzer")
        print("=" * 50)
        
        # Check if API key is available
        if not os.environ.get("LLAMA_API_KEY"):
            print("❌ Error: LLAMA_API_KEY not found in environment variables")
            print("Please make sure your .env file contains: LLAMA_API_KEY=your_api_key")
            return None
        
        # Read the Sankey data from file
        try:
            with open(sankey_data_file, 'r', encoding='utf-8') as f:
                sankey_content = f.read()
            print(f"✅ Loaded Sankey data from: {sankey_data_file}")
            
            # Validate that the file contains Sankey data
            if "sankeyData" not in sankey_content or "[" not in sankey_content:
                raise ValueError("File does not contain valid Sankey data")
                
        except FileNotFoundError:
            print(f"❌ Error: File '{sankey_data_file}' not found")
            print("💡 Please ensure 'sankey_data.js' exists in the current directory")
            print("💡 The file should contain: const sankeyData = [...]")
            return None
        except ValueError as e:
            print(f"❌ Error: {e}")
            print("💡 Please ensure the file contains valid Sankey data in the format:")
            print("💡 const sankeyData = [[\"From\", \"To\", \"Weight\"], ...]")
            return None
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return None
        
        # Generate the analysis prompt
        print("📝 Generating analysis prompt...")
        prompt = self.generate_insights_prompt(sankey_content)
        
        # Call LLM for analysis
        raw_response = self.call_llama_api(prompt)
        
        if raw_response:
            # Parse and validate JSON response
            insights_data = self.parse_and_validate_json(raw_response)
            
            if insights_data:
                print("✅ Analysis completed successfully!")
                
                # Display insights
                self.display_insights(insights_data)
                
                # Save to JSON file
                if self.save_insights_to_json(insights_data):
                    print(f"\n✅ Complete! Insights saved to 'sankey_insights.json'")
                    return insights_data
                else:
                    return insights_data
            else:
                print("❌ Failed to parse insights from LLM response")
                # Save raw response for debugging
                with open("raw_insights_response.txt", "w", encoding='utf-8') as f:
                    f.write(raw_response)
                print("💾 Raw response saved to 'raw_insights_response.txt' for debugging")
                return None
        else:
            print("❌ Failed to get response from LLM")
            return None

def main():
    """Main function to run the Sankey insights analyzer"""
    
    print("📋 Instructions:")
    print("1. Make sure 'sankey_data.js' file exists in the current directory")
    print("2. The file should contain: const sankeyData = [...]")
    print("3. Set LLAMA_API_KEY in your .env file")
    print("")
    
    analyzer = SankeyInsightsAnalyzer()
    
    # Analyze data from sankey_data.js file
    result = analyzer.analyze_sankey_data("sankey_data.js")
    
    if result:
        print("\n🎉 Success! Sankey insights have been generated and saved.")
        print("📄 Output file: sankey_insights.json")
        print("💡 The insights are ready for use in reports or dashboards.")
        
        # Show file contents preview
        try:
            with open("sankey_insights.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"\n📊 Generated {len(data)} insights:")
            for key in data.keys():
                if 'insight' in key:
                    print(f"  ✓ {data[key].get('title', key)}")
                elif key == 'executive_summary':
                    print(f"  ✓ {data[key].get('title', 'Executive Summary')}")
        except:
            pass
            
    else:
        print("\n❌ Failed to generate insights. Check the error messages above.")
        print("\n💡 Troubleshooting:")
        print("  - Ensure 'sankey_data.js' exists and contains valid Sankey data")
        print("  - Check your LLAMA_API_KEY in the .env file")
        print("  - Verify internet connection for API calls")
    return result

if __name__ == "__main__":
    main()