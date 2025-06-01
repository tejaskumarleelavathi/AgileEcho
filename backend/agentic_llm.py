import os
import json
import requests
from dotenv import load_dotenv

# === Load API Keys ===
load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")

class LlamaAPIClient:
    """Simple Llama API client"""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.llama.com/v1/chat/completions"
    
    def create_completion(self, messages: list, model: str = "Llama-4-Maverick-17B-128E-Instruct-FP8") -> str:
        """Create a completion with Llama API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # Handle Llama API response structure
                if 'completion_message' in result:
                    content = result['completion_message']['content']
                    if isinstance(content, dict) and 'text' in content:
                        return content['text']
                    return str(content)
                
                # Fallback for OpenAI-like structure
                elif 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                
                return str(result)
                
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Llama API: {e}")
            return None

# Initialize Llama client
llama = LlamaAPIClient(api_key=LLAMA_API_KEY)

# === Load GitHub issues ===
print("📂 Loading GitHub issues data...")
try:
    with open("specific_vscode_cosmosdb_issues.json") as f:
        github_data = json.load(f)
    issues = github_data.get("issues", [])
    print(f"✅ Loaded {len(issues)} issues")
except FileNotFoundError:
    print("❌ Issues file not found. Please check the filename.")
    exit(1)

# === Agentic Function Generator ===
def generate_analysis_code(task_description: str) -> str:
    """Ask LLM to generate Python code for a specific analysis task"""
    
    prompt = f"""
You are a Python code generator. Generate ONLY executable Python code for this task:

Task: {task_description}

Requirements:
- You have access to a variable called 'issues' (list of GitHub issue dictionaries)
- Each issue has: number, title, state, labels, milestone, etc.
- Store your result in a variable called 'result'
- Write clean, direct Python code (no functions, no imports)
- No explanations, just code

Example issue structure:
{{
    "number": 123,
    "title": "Bug fix",
    "state": "open",
    "labels": [{{"name": "bug"}}, {{"name": "priority: high"}}],
    "milestone": {{"title": "v1.0"}} or None
}}

Generate Python code:
"""

    print(f"🤖 Generating code for: {task_description}")
    
    response = llama.create_completion([{"role": "user", "content": prompt}])
    
    if response:
        # Extract code from response
        code = extract_code_from_response(response)
        print(f"✅ Generated code: {code[:100]}...")
        return code
    else:
        print(f"❌ Failed to generate code for: {task_description}")
        return None

def extract_code_from_response(response: str) -> str:
    """Extract Python code from LLM response"""
    import re
    
    # Look for code blocks
    code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    
    code_blocks = re.findall(r'```\n(.*?)\n```', response, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    
    # If no code blocks, assume whole response is code
    lines = response.strip().split('\n')
    # Remove any explanation lines
    code_lines = [line for line in lines if not line.strip().startswith('#') or 'result' in line]
    return '\n'.join(code_lines)

def execute_generated_code(code: str, issues: list):
    """Execute the generated Python code safely"""
    try:
        print(f"🔧 Executing generated code...")
        
        # Safe execution environment
        safe_globals = {
            'issues': issues,
            'len': len, 'sum': sum, 'any': any, 'all': all,
            'max': max, 'min': min, 'sorted': sorted,
            'enumerate': enumerate, 'range': range,
            'dict': dict, 'list': list, 'set': set,
            'str': str, 'int': int, 'float': float
        }
        
        local_vars = {}
        exec(code, safe_globals, local_vars)
        
        if 'result' in local_vars:
            result = local_vars['result']
            print(f"✅ Execution successful: {type(result)}")
            return result
        else:
            print(f"❌ No 'result' variable found")
            return None
            
    except Exception as e:
        print(f"❌ Code execution failed: {e}")
        return None

# === Define Analysis Tasks ===
analysis_tasks = [
    {
        "name": "open_issues",
        "description": "Count the total number of open issues (state == 'open')"
    },
    {
        "name": "closed_issues", 
        "description": "Count the total number of closed issues (state == 'closed')"
    },
    {
        "name": "blockers",
        "description": "Find issues with blockers by checking if labels contain 'blocked', 'blocker', 'external', 'dependency' or title contains 'block'. Return list of dicts with 'id' and 'title'"
    },
    {
        "name": "milestones",
        "description": "Group issues by milestone, counting open vs closed for each. Use 'Backlog' for issues without milestone. Return dict with milestone names as keys and {'open': count, 'closed': count} as values"
    },
    {
        "name": "critical_issues",
        "description": "Find critical issues by checking if priority or name in label of issues has 'p0', or 'p1', or 'P1', or 'P1'. Return list of dicts with 'id', 'title', 'milestone'"
    },
    {
        "name": "size_by_milestone",
        "description": "Categorize issues by size labels (look for 'size: s', 'size: m', 'size: l', 'S', 'M', 'L', 'XS', 'XL', 'xl', 'xs', 'xxl', 'XXL in labels) and group by milestone. Return dict with milestone as key and size counts as values"
    }
]

# === Agentic Orchestrator ===
def orchestrate_analysis():
    """Main orchestrator that delegates tasks to code-generating agents"""
    
    print("🚀 Starting Agentic GitHub Analysis...")
    print("Each task will be handled by a code-generating agent\n")
    
    final_results = {
        "totals": {},
        "blockers": [],
        "milestones": {},
        "critical_issues": [],
        "size_by_milestone": {},
        "metadata": {
            "total_issues": len(issues),
            "analysis_timestamp": f"{__import__('datetime').datetime.now().isoformat()}",
            "agentic_analysis": True
        }
    }
    
    # Execute each task with an agentic code generator
    for task in analysis_tasks:
        print(f"📋 Task: {task['description']}")
        
        # Generate code for this task with retry logic
        code = generate_analysis_code(task['description'])
        
        if code:
            # Execute the generated code
            result = execute_generated_code(code, issues)
            
            if result is not None:
                # Map results to the expected schema
                if task['name'] == 'open_issues':
                    final_results['totals']['open_issues'] = result
                elif task['name'] == 'closed_issues':
                    final_results['totals']['closed_issues'] = result
                elif task['name'] == 'blockers':
                    final_results['blockers'] = result
                elif task['name'] == 'milestones':
                    final_results['milestones'] = result
                elif task['name'] == 'critical_issues':
                    final_results['critical_issues'] = result
                elif task['name'] == 'size_by_milestone':
                    final_results['size_by_milestone'] = result
                
                print(f"✅ Task completed: {task['name']}")
            else:
                print(f"❌ Task failed: {task['name']}")
        else:
            print(f"❌ Code generation failed for: {task['name']}")
        
        print()  # Add spacing
    
    return final_results

# === Execute Agentic Analysis ===
if __name__ == "__main__":
    if not LLAMA_API_KEY:
        print("❌ Please set LLAMA_API_KEY environment variable")
        exit(1)
    
    # Run the agentic analysis
    results = orchestrate_analysis()
    
    # Save results
    output_file = "agentic_analysis_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("=" * 60)
    print("🎉 AGENTIC ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"📊 Open Issues: {results['totals'].get('open_issues', 'N/A')}")
    print(f"📊 Closed Issues: {results['totals'].get('closed_issues', 'N/A')}")
    print(f"🚧 Blocked Issues: {len(results.get('blockers', []))}")
    print(f"📅 Milestones: {len(results.get('milestones', {}))}")
    print(f"❗ Critical Issues: {len(results.get('critical_issues', []))}")
    print(f"📏 Size Categories: {len(results.get('size_by_milestone', {}))}")
    print(f"\n📄 Results saved to: {output_file}")
    print("\n🤖 Each metric was calculated by LLM-generated code!")