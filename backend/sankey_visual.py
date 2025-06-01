def generate_sankey_analysis_prompt(json_data):
    """Generate a comprehensive prompt for Sankey generation and analysis"""
    
    prompt = f"""You are an expert data analyst specializing in GitHub project analysis and Sankey diagram creation. Your task is to:

1. Generate a complete Sankey diagram from the GitHub issues data
2. Provide detailed analysis with key insights

# TASK 1: GENERATE SANKEY DATA

Create a Sankey diagram following this EXACT flow structure:
**Type/Labels → Primary Categories → Priority → Milestone → Assignee**

## Required Output Format:

```javascript
const sankeyData = [
  ["From", "To", "Weight"],
  
  // Stage 1: Type/Labels → Primary Categories
  ["bug", "AT-CTI", 5],
  ["feature", "MongoDB Clusters", 12],
  ["enhancement", "NoSQL", 8],
  ["Other", "user feedback", 6],
  
  // Stage 2: Primary Categories → Priority
  ["AT-CTI", "P1", 10],
  ["MongoDB Clusters", "P2", 15],
  ["NoSQL", "No Priority", 20],
  
  // Stage 3: Priority → Milestone
  ["P1", "0.26.1", 8],
  ["P2", "0.27.0", 12],
  ["No Priority", "Backlog", 25],
  
  // Stage 4: Milestone → Assignee
  ["0.26.1", "tnaum-ms", 6],
  ["0.27.0", "sevoku", 8],
  ["Backlog", "bk201-", 10]
];
```

## Processing Rules:
1. **Extract Types**: Use issue types (bug, feature, enhancement) or label-based inference
2. **Categorize Labels**: Group into primary categories: AT-CTI, MongoDB Clusters, NoSQL, user feedback, engineering, external, etc.
3. **Normalize Priority**: Use P0, P1, P2, "No Priority" (group nulls/empty as "No Priority")
4. **Group Milestones**: Combine similar versions (0.26.x, 0.27.x), keep shipped versions separate
5. **Assignees**: Use exact usernames from assignee data
6. **Minimum Threshold**: Include connections with 2+ issues

# TASK 2: PROVIDE ANALYSIS

After generating the Sankey data, provide this analysis structure:

## 📊 KEY INSIGHT 1: [Title]
**Finding**: [One sentence summary]
**Details**: [2-3 sentences explaining the insight with specific numbers]

## 📊 KEY INSIGHT 2: [Title]  
**Finding**: [One sentence summary]
**Details**: [2-3 sentences explaining the insight with specific numbers]

## 📊 KEY INSIGHT 3: [Title]
**Finding**: [One sentence summary] 
**Details**: [2-3 sentences explaining the insight with specific numbers]

## 🎯 BIG PICTURE INSIGHT: [Title]
**Overall Assessment**: [Comprehensive 4-5 sentence analysis that ties together all the findings, explains the team's work patterns, identifies the main bottlenecks or focus areas, and provides actionable recommendations for project management]

# GitHub Issues Data:
```json
{json_data}
```

CRITICAL INSTRUCTIONS:
1. Start immediately with: const sankeyData = [
2. Follow the exact flow structure: Type → Category → Priority → Milestone → Assignee
3. Count actual issues for accurate weights
4. After the JavaScript array, provide the 4-part analysis
5. Focus on actionable insights for project management

Begin now:"""

    return prompt

def generate_comprehensive_sankey_prompt():
    """Complete prompt for generating Sankey data like the example"""
    
    prompt = """You are an expert GitHub project analyst. Create a comprehensive Sankey diagram and analysis from GitHub issues data.

# OBJECTIVE: Generate Sankey data in this EXACT format and provide strategic insights

## Required Output Structure:

```javascript
const sankeyData = [
  ["From", "To", "Weight"],
  // Multi-stage flow showing project workflow
  ["Other", "AT-CTI", 21],
  ["bug", "NoSQL", 4],
  ["feature", "MongoDB Clusters", 5],
  // ... continuing through all workflow stages
  ["0.26.1", "tnaum-ms", 5],
  ["Backlog", "bk201-", 7]
];
```

## Flow Structure Rules:
1. **Stage 1**: Issue Types/Labels → Primary Categories
   - Types: bug, feature, enhancement, Other
   - Categories: AT-CTI, MongoDB Clusters, NoSQL, user feedback, engineering, external

2. **Stage 2**: Primary Categories → Priority Levels  
   - Priorities: P0, P1, P2, No Priority
   - Count actual issues flowing from each category

3. **Stage 3**: Priority Levels → Milestones
   - Milestones: 0.26.1, 0.27.0, 0.28.0, Backlog, shipped versions
   - Group similar milestones appropriately

4. **Stage 4**: Milestones → Team Members
   - Assignees: tnaum-ms, sevoku, bk201-, v-ruizh
   - Show actual workload distribution

## Analysis Requirements:

After the Sankey data, provide:

### 📊 KEY INSIGHT 1: Workload Distribution
**Finding**: [Analysis of how work is distributed across team members]
**Details**: [Specific numbers and patterns in assignments]

### 📊 KEY INSIGHT 2: Priority Management  
**Finding**: [Analysis of priority distribution and milestone planning]
**Details**: [Insights about priority levels and milestone allocation]

### 📊 KEY INSIGHT 3: Issue Type Patterns
**Finding**: [Analysis of bug vs feature vs enhancement distribution]  
**Details**: [Patterns in issue types and their flow through the system]

### 🎯 BIG PICTURE INSIGHT: Project Health & Strategic Recommendations
**Overall Assessment**: [Comprehensive analysis covering team productivity, project focus areas, potential bottlenecks, milestone planning effectiveness, and 2-3 actionable recommendations for improving project management and delivery]

## Data Processing Guidelines:
- Include ALL significant flows (2+ issues minimum)
- Use exact weight counts from data
- Maintain flow conservation (inputs = outputs for each node)
- Group similar items logically (versions, priorities, labels)
- Preserve important distinctions (don't over-aggregate)

Generate the complete Sankey data array followed by the 4-part analysis. Start with: const sankeyData = ["""

    return prompt

# Example usage function
def create_sankey_analysis_request(json_filename='github_issues.json'):
    """Create a complete request for Sankey generation and analysis"""
    
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Convert to string for embedding in prompt
        json_str = json.dumps(json_data, indent=2)
        
        # Generate the comprehensive prompt
        prompt = generate_sankey_analysis_prompt(json_str)
        
        return prompt
        
    except FileNotFoundError:
        return f"Error: File {json_filename} not found"
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON - {e}"

def call_llama_for_sankey_analysis(prompt):
    """Call LLM with the Sankey analysis prompt"""
    
    # This would be your LLM API call
    system_message = """You are a senior data analyst and project management expert specializing in GitHub workflow analysis. You excel at:

1. Creating accurate Sankey diagrams that show true project workflows
2. Identifying key patterns in development team productivity  
3. Providing actionable insights for project management
4. Analyzing workload distribution and bottlenecks
5. Making strategic recommendations based on data patterns

You MUST provide both the complete Sankey JavaScript array AND the detailed 4-part analysis as requested. Be specific with numbers and actionable with recommendations."""

    return {
        "system": system_message,
        "user": prompt
    }

# Complete example that matches your desired output
def example_sankey_analysis():
    """Example of the complete output format you want"""
    
    example_output = """const sankeyData = [
  ["From", "To", "Weight"],
  ["Other", "AT-CTI", 21],
  ["Other", "MongoDB Clusters", 48],
  ["bug", "NoSQL", 4],
  ["feature", "MongoDB Clusters", 5],
  ["AT-CTI", "P1", 5],
  ["MongoDB Clusters", "P2", 11],
  ["P1", "0.26.1", 5],
  ["P2", "0.27.0", 12],
  ["0.26.1", "tnaum-ms", 5],
  ["0.27.0", "sevoku", 8]
];

📊 KEY INSIGHT 1: Workload Concentration
**Finding**: Heavy workload concentration on specific team members with uneven distribution
**Details**: tnaum-ms handles 35+ issues across multiple milestones, while other team members have 15-25 issues each. This suggests potential bottlenecks and the need for better load balancing across the team.

📊 KEY INSIGHT 2: Priority Gap Challenge  
**Finding**: Significant portion of work lacks priority classification
**Details**: Over 60% of issues are marked as "No Priority", with many flowing to Backlog. Only 25% have clear P0/P1/P2 designations, indicating a need for better priority triaging and milestone planning.

📊 KEY INSIGHT 3: Feature vs Maintenance Balance
**Finding**: Project shows healthy balance between new features and maintenance work
**Details**: Feature requests (40+ issues) slightly outweigh bug fixes (15+ issues), with enhancement work forming a smaller but consistent portion. The AT-CTI and MongoDB Clusters categories dominate the workflow.

🎯 BIG PICTURE INSIGHT: Strategic Development Focus with Process Improvement Needs
**Overall Assessment**: The team is actively developing core database functionality with strong focus on MongoDB Clusters and AT-CTI features, but faces process challenges in priority management and workload distribution. The high volume of "No Priority" items suggests need for better intake and triaging processes. While shipped milestones show delivery capability, the large Backlog indicates scope management challenges. Recommendations: implement regular priority review sessions, establish clearer assignment criteria to distribute workload more evenly, and create a structured process for moving items from "No Priority" to defined priority levels."""

    return example_output

# Main function to demonstrate usage
def main():
    """Demonstrate how to use the prompt generator"""
    
    print("🎯 Sankey Analysis Prompt Generator")
    print("=" * 50)
    
    # Method 1: Generate prompt with actual data file
    prompt_with_data = create_sankey_analysis_request('your_github_issues.json')
    
    # Method 2: Use the comprehensive standalone prompt  
    standalone_prompt = generate_comprehensive_sankey_prompt()
    
    # Method 3: Show example of expected output
    example = example_sankey_analysis()
    
    print("✅ Generated prompts for:")
    print("1. Data-specific analysis (if you have JSON file)")
    print("2. Standalone comprehensive prompt")  
    print("3. Example output format")
    
    print(f"\n📝 Standalone Prompt Length: {len(standalone_prompt):,} characters")
    print(f"🎯 Example Output Length: {len(example):,} characters")

if __name__ == "__main__":
    main()