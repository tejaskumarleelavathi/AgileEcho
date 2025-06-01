import requests
import json
import os
from datetime import datetime

# Configuration
from dotenv import load_dotenv

load_dotenv()

# Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") 
ORG = 'microsoft'
REPO = 'vscode-cosmosdb'

def extract_type_from_issue(issue):
    """Extract type information from issue labels and other sources"""
    
    # Check labels for type information
    type_info = None
    
    for label in issue.get('labels', []):
        label_name = label.get('name', '').lower()
        
        # Look for common type patterns
        if label_name.startswith('type:'):
            type_info = label_name.replace('type:', '').strip()
        elif label_name.startswith('kind:'):
            type_info = label_name.replace('kind:', '').strip()
        elif label_name in ['bug', 'feature', 'enhancement', 'documentation', 'question', 'help wanted']:
            type_info = label_name
        elif 'bug' in label_name:
            type_info = 'bug'
        elif 'feature' in label_name or 'enhancement' in label_name:
            type_info = 'feature'
        elif 'doc' in label_name:
            type_info = 'documentation'
    
    return type_info

def get_issue_type_simple(issue_number):
    """Get just the type for a single issue"""
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Type-Extractor'
    }
    
    # Get individual issue
    issue_url = f'https://api.github.com/repos/{ORG}/{REPO}/issues/{issue_number}'
    
    try:
        response = requests.get(issue_url, headers=headers)
        
        if response.status_code != 200:
            return None
            
        issue = response.json()
        
        # Skip pull requests
        if 'pull_request' in issue:
            return None
        
        issue_type = extract_type_from_issue(issue)
        
        return {
            'number': issue_number,
            'title': issue.get('title', ''),
            'type': issue_type,
            'labels': [label.get('name') for label in issue.get('labels', [])]
        }
        
    except Exception as e:
        print(f"Error fetching issue #{issue_number}: {str(e)}")
        return None

def extract_types_for_issues():
    """Extract types for your specific list of issues"""
    
    # Your list of issue numbers
    target_issue_numbers = [
        2460, 2456, 2445, 2443, 2463, 2484, 2694, 2697, 2550, 2593,
        2422, 2416, 2497, 2503, 2446, 2513, 2542, 2549, 2437, 2454,
        2619, 2483, 2556, 2469, 2488, 2567, 2582, 2620, 2624, 2639,
        2649, 2675, 2682, 2689, 2487, 2482, 2586, 2621, 2592, 2690,
        2691, 2432, 2480, 2507, 2500, 2499, 2498, 2504, 2505, 2496,
        2495, 2494, 2493, 2479, 2461, 2509, 2486, 2485, 2489, 2490,
        2491, 2508, 2473, 2510, 2521, 2528, 2531, 2532, 2459, 2452,
        2583, 2564, 2596, 2423, 2523, 2458, 2418, 2417, 2451, 2439,
        2468, 2478, 2524, 2526, 2440, 2457, 2449, 2514, 2516, 2517,
        2540, 2474, 2515, 2475, 2565, 2502, 2472, 2527, 2551, 2552,
        2553, 2563, 2575, 2597, 2632, 2628, 2636
    ]
    
    results = []
    
    print(f"Extracting types for {len(target_issue_numbers)} issues...")
    
    for i, issue_number in enumerate(target_issue_numbers, 1):
        print(f"Processing issue #{issue_number} ({i}/{len(target_issue_numbers)})...")
        
        issue_data = get_issue_type_simple(issue_number)
        
        if issue_data:
            results.append(issue_data)
            print(f"  ✅ #{issue_number}: Type = {issue_data['type'] or 'None'}")
        else:
            print(f"  ❌ Failed to get #{issue_number}")
    
    return results

def main():
    """Main function - just extract types"""
    
    print("Starting simple type extraction...")
    
    try:
        issues_with_types = extract_types_for_issues()
        
        # Save to simple JSON
        output = {
            'extracted_at': datetime.now().isoformat(),
            'total_issues': len(issues_with_types),
            'issues': issues_with_types
        }
        
        filename = 'issue_types_only.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ SUCCESS! Extracted types for {len(issues_with_types)} issues")
        print(f"📁 Saved to: {filename}")
        
        # Print summary
        type_counts = {}
        for issue in issues_with_types:
            issue_type = issue['type'] or 'Unknown'
            type_counts[issue_type] = type_counts.get(issue_type, 0) + 1
        
        print(f"\n📊 Type Summary:")
        for type_name, count in sorted(type_counts.items()):
            print(f"  {type_name}: {count}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()