import json
import os
from llama_api_client import LlamaAPIClient

from dotenv import load_dotenv
load_dotenv()

def generate_llama_prompt_with_json(json_filename='specific_vscode_cosmosdb_issues_extracted.json'):
    """Generate a complete LLaMA prompt with embedded JSON data"""
    
    # Load the JSON data
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Convert back to JSON string for embedding
        json_str = json.dumps(json_data, indent=2)
        
        prompt = f"""You are an expert data analyst. Your task is to create a Sankey diagram from GitHub issues data.

# CRITICAL: Start your response with the exact JavaScript array format shown below

## Required Output Format (copy this structure exactly):

```javascript
const sankeyData = [
  ["From", "To", "Weight"],
  ["Bug", "AT-CTI", 6],
  ["Feature", "MongoDB Clusters", 9],
  ["Enhancement", "NoSQL", 4],
  ["AT-CTI", "P1", 7],
  ["MongoDB Clusters", "P0", 2],
  ["P1", "0.26.x", 5],
  ["P0", "0.27.x", 3],
  ["0.26.x", "tnaum-ms", 5],
  ["0.27.x", "bk201-", 4]
];
```

## Processing Rules:
1. **Type**: Use existing type field, or infer from labels (bug→Bug, feature→Feature, enhancement→Enhancement)
2. **Primary Label**: Pick ONE most important label per issue. Priority: AT-CTI > MongoDB Clusters > NoSQL > engineering > user feedback > external
3. **Priority**: Only use P0, P1, P2 (skip null/empty priorities)
4. **Milestone**: Group similar versions (0.26.x, 0.27.x, 0.28.x, Backlog, Shipped)
5. **User**: Use user.login field
6. **Thresholds**: Only include connections with 2+ issues (3+ for Milestone→User)

## Flow Structure: Type → Primary Label → Priority → Milestone → User

## GitHub Issues Data:
```json
{json_str}
```

IMPORTANT: Begin your response immediately with the JavaScript array. Then provide analysis below it.
"""
        
        return prompt
        
    except FileNotFoundError:
        return f"Error: File {json_filename} not found"
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON - {e}"

def call_llama_api(prompt):
    """Call LLaMA API with the generated prompt"""
    try:
        client = LlamaAPIClient(
            api_key=os.environ.get("LLAMA_API_KEY"),
            base_url="https://api.llama.com/v1/",
        )
        
        print("🔄 Calling LLaMA API...")
        response = client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        
        print(f"📊 Response type: {type(response)}")
        print(f"📊 Response attributes: {dir(response)}")
        
        # Try different ways to access the content
        if hasattr(response, 'choices') and response.choices:
            return response.choices[0].message.content
        elif hasattr(response, 'content'):
            return response.content
        elif hasattr(response, 'message'):
            return response.message
        elif hasattr(response, 'text'):
            return response.text
        else:
            # Print the raw response to debug
            print(f"🔍 Raw response: {response}")
            return str(response)
        
    except Exception as e:
        return f"Error calling LLaMA API: {e}"

def save_response_to_file(response, output_filename='llama_sankey_analysis.txt'):
    """Save the LLaMA response to a file"""
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(response)
    print(f"✅ Analysis saved to {output_filename}")

def extract_sankey_data(response):
    """Extract just the Sankey JavaScript array from the response"""
    try:
        # Find the JavaScript array in the response
        start_marker = "const sankeyData = ["
        end_marker = "];"
        
        start_idx = response.find(start_marker)
        if start_idx == -1:
            return "Sankey data not found in response"
        
        end_idx = response.find(end_marker, start_idx) + len(end_marker)
        if end_idx == -1:
            return "Sankey data end not found in response"
        
        sankey_js = response[start_idx:end_idx]
        return sankey_js
        
    except Exception as e:
        return f"Error extracting Sankey data: {e}"

def main():
    """Generate prompt, call LLaMA API, and save results"""
    print("🔄 Generating LLaMA prompt with JSON context...")
    
    # Generate prompt with embedded JSON
    prompt = generate_llama_prompt_with_json()
    
    if prompt.startswith("Error:"):
        print(f"❌ {prompt}")
        return
    
    print(f"📄 Generated prompt: {len(prompt):,} characters")
    
    # Save prompt for reference
    with open('generated_prompt.txt', 'w', encoding='utf-8') as f:
        f.write(prompt)
    print("✅ Prompt saved to 'generated_prompt.txt'")
    
    # Call LLaMA API
    response = call_llama_api(prompt)
    
    if response.startswith("Error"):
        print(f"❌ {response}")
        return
    
    print("✅ LLaMA API call successful!")
    
    # Save full response
    save_response_to_file(response)
    
    # Extract and save just the Sankey data
    sankey_data = extract_sankey_data(response)
    with open('sankey_data.js', 'w', encoding='utf-8') as f:
        f.write(sankey_data)
    print("✅ Sankey data extracted to 'sankey_data.js'")
    
    print(f"\n📊 Analysis Complete!")
    print(f"📁 Files created:")
    print(f"  - generated_prompt.txt (the prompt sent to LLaMA)")
    print(f"  - llama_sankey_analysis.txt (full LLaMA response)")
    print(f"  - sankey_data.js (extracted Sankey diagram)")
    
    print(f"\n🎯 Sankey Data Preview:")
    print(sankey_data[:500] + "..." if len(sankey_data) > 500 else sankey_data)

if __name__ == "__main__":
    main()