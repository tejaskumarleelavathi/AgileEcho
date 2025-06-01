import json
import os
from llama_api_client import LlamaAPIClient
from datetime import datetime


from dotenv import load_dotenv


# === Load API Keys from .env ===
load_dotenv()




# Initialize Llama client
client = LlamaAPIClient(
    api_key=os.environ.get("LLAMA_API_KEY"),
    base_url="https://api.llama.com/v1/",
)

def create_extraction_prompt(issues_data):
    """Create a structured prompt for Llama to extract specific fields"""
    
    prompt = f"""You are a GitHub Issues Data Extraction Expert. I will provide you with GitHub issues data in JSON format, and you need to extract specific fields for each issue.

TASK: Extract the following fields for each issue:
1. Issue ID (number)
2. Type (from the "type" field)
3. Labels (extract only the "name" values from the labels array)
4. Milestone (from milestone.title)
5. Priority (from the "priority" field)
6. User Information (from the "user" object: login, id, type)

INPUT DATA:
{json.dumps(issues_data, indent=2)}

OUTPUT FORMAT: Return a JSON array where each object contains:
{{
    "issue_id": <number>,
    "type": <type_value_or_null>,
    "labels": [<list_of_label_names>],
    "milestone": <milestone_title_or_null>,
    "priority": <priority_value_or_null>,
    "user": {{
        "login": <user_login>,
        "id": <user_id>,
        "type": <user_type>
    }}
}}

IMPORTANT RULES:
- Extract data for ALL issues provided
- If a field is null/missing, use null in the output
- Labels should be an array of strings (label names only)
- Keep the exact values as they appear in the source data
- Return only valid JSON, no explanations

Extract the data:"""

    return prompt

def extract_issues_with_llama(issues_data, batch_size=5):
    """Extract issue fields using Llama 4 Scout"""
    
    print(f"🤖 Starting Llama 4 Scout extraction for {len(issues_data)} issues...")
    
    all_extracted = []
    
    # Process issues in batches to avoid token limits
    for i in range(0, len(issues_data), batch_size):
        batch = issues_data[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(issues_data) + batch_size - 1) // batch_size
        
        print(f"📋 Processing batch {batch_num}/{total_batches} ({len(batch)} issues)...")
        
        # Create prompt for this batch
        prompt = create_extraction_prompt(batch)
        
        try:
            # Call Llama API
            response = client.chat.completions.create(
                model="Llama-4-Scout-17B-16E-Instruct-FP8",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistent extraction
                max_tokens=4000   # Enough for extraction results
            )
            
            # Extract response content
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].message.content
            else:
                # Handle different response formats
                content = str(response)
            
            # Parse the JSON response
            try:
                extracted_batch = json.loads(content.strip())
                
                if isinstance(extracted_batch, list):
                    all_extracted.extend(extracted_batch)
                    print(f"✅ Successfully extracted {len(extracted_batch)} issues from batch {batch_num}")
                else:
                    print(f"⚠️ Unexpected response format in batch {batch_num}")
                    print(f"Response: {content[:200]}...")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response for batch {batch_num}: {e}")
                print(f"Raw response: {content[:300]}...")
                
                # Try to extract fields manually as fallback
                fallback_data = extract_fallback(batch)
                all_extracted.extend(fallback_data)
                print(f"🔄 Used fallback extraction for batch {batch_num}")
                
        except Exception as e:
            print(f"❌ Error calling Llama API for batch {batch_num}: {e}")
            
            # Use fallback extraction
            fallback_data = extract_fallback(batch)
            all_extracted.extend(fallback_data)
            print(f"🔄 Used fallback extraction for batch {batch_num}")
    
    return all_extracted

def extract_fallback(issues_batch):
    """Fallback extraction method if Llama fails"""
    
    extracted = []
    
    for issue in issues_batch:
        # Extract labels names
        labels = []
        for label in issue.get('labels', []):
            if isinstance(label, dict) and 'name' in label:
                labels.append(label['name'])
        
        # Extract user info
        user_info = issue.get('user', {})
        user = {
            "login": user_info.get('login'),
            "id": user_info.get('id'),
            "type": user_info.get('type')
        }
        
        # Extract milestone
        milestone = None
        if issue.get('milestone') and isinstance(issue['milestone'], dict):
            milestone = issue['milestone'].get('title')
        
        extracted_issue = {
            "issue_id": issue.get('number'),
            "type": issue.get('type'),
            "labels": labels,
            "milestone": milestone,
            "priority": issue.get('priority'),
            "user": user
        }
        
        extracted.append(extracted_issue)
    
    return extracted

def save_extracted_data(extracted_data, output_file='extracted_issues.json'):
    """Save extracted data to JSON file"""
    
    output = {
        "metadata": {
            "total_issues": len(extracted_data),
            "extracted_at": datetime.now().isoformat(),
            "extraction_method": "Llama 4 Scout + Fallback",
            "fields_extracted": ["issue_id", "type", "labels", "milestone", "priority", "user"]
        },
        "extracted_issues": extracted_data
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved extracted data to: {output_file}")

def analyze_extracted_data(extracted_data):
    """Analyze the extracted data and print summary"""
    
    print(f"\n📊 EXTRACTION ANALYSIS:")
    print("=" * 50)
    
    # Count by type
    type_counts = {}
    priority_counts = {}
    milestone_counts = {}
    user_counts = {}
    
    for item in extracted_data:
        # Count types
        issue_type = item.get('type') or 'No Type'
        type_counts[issue_type] = type_counts.get(issue_type, 0) + 1
        
        # Count priorities
        priority = item.get('priority') or 'No Priority'
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Count milestones
        milestone = item.get('milestone') or 'No Milestone'
        milestone_counts[milestone] = milestone_counts.get(milestone, 0) + 1
        
        # Count users
        user_login = item.get('user', {}).get('login') or 'No User'
        user_counts[user_login] = user_counts.get(user_login, 0) + 1
    
    print(f"📋 TYPES:")
    for type_name, count in sorted(type_counts.items()):
        print(f"  {type_name}: {count}")
    
    print(f"\n⚡ PRIORITIES:")
    for priority, count in sorted(priority_counts.items()):
        print(f"  {priority}: {count}")
    
    print(f"\n📅 MILESTONES:")
    for milestone, count in sorted(milestone_counts.items()):
        print(f"  {milestone}: {count}")
    
    print(f"\n👥 TOP USERS:")
    sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)
    for user, count in sorted_users[:5]:
        print(f"  {user}: {count} issues")
    
    # Show sample labels
    all_labels = set()
    for item in extracted_data:
        all_labels.update(item.get('labels', []))
    
    print(f"\n🏷️ UNIQUE LABELS ({len(all_labels)} total):")
    for label in sorted(list(all_labels))[:10]:
        print(f"  {label}")
    if len(all_labels) > 10:
        print(f"  ... and {len(all_labels) - 10} more")

def main():
    """Main execution function"""
    
    # Check for API key
    if not os.environ.get("LLAMA_API_KEY"):
        print("❌ Please set LLAMA_API_KEY environment variable")
        return
    
    # Load GitHub issues data
    input_file = input("Enter GitHub issues JSON file path: ").strip()
    if not input_file:
        input_file = "specific_vscode_cosmosdb_issues.json"  # Default file
    
    try:
        print(f"📂 Loading data from: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            github_data = json.load(f)
        
        issues = github_data.get('issues', [])
        print(f"✅ Loaded {len(issues)} issues")
        
        if not issues:
            print("❌ No issues found in the data")
            return
        
        # Extract fields using Llama
        extracted_data = extract_issues_with_llama(issues)
        
        if extracted_data:
            # Save extracted data
            output_file = input_file.replace('.json', '_extracted.json')
            save_extracted_data(extracted_data, output_file)
            
            # Analyze results
            analyze_extracted_data(extracted_data)
            
            print(f"\n🎉 Extraction complete!")
            print(f"📄 Input: {len(issues)} issues")
            print(f"📄 Output: {len(extracted_data)} extracted records")
            
        else:
            print("❌ No data was extracted")
            
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON file: {input_file}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()