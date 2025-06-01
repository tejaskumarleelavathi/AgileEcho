import os
import json
import requests
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

# Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Replace with your token
REPO_OWNER = "microsoft"
REPO_NAME = "vscode-cosmosdb"  # Change this to your target repo
OUTPUT_DIR = "github_analysis_output"

class ShippedMilestoneAnalyzer:
    def __init__(self, token, owner, repo, days_back=90):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.days_back = days_back
        
        # Calculate cutoff date - X days ago from now
        now = datetime.now(timezone.utc)
        self.cutoff_date = now - timedelta(days=days_back)
        
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Repo-Analyzer'
        }
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'
        
        # Create output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        print(f"📅 Current time: {now}")
        print(f"📅 Looking for shipped milestones from last {days_back} days")
        print(f"📅 Date range: {self.cutoff_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}")
        
        # Cache for data to avoid repeated API calls
        self.pr_cache = {}
        self.shipped_milestones = []
    
    def make_request(self, url, params=None):
        """Make GitHub API request with rate limiting"""
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            # Handle rate limiting
            if response.status_code == 403 and 'rate limit' in response.text.lower():
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                if reset_time:
                    wait_time = reset_time - int(time.time()) + 10
                    print(f"⏳ Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"❌ Error response: {response.status_code}")
                return None
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return None
    
    def get_all_paginated_data(self, endpoint, params=None, max_pages=None):
        """Get all data from paginated GitHub API endpoint"""
        all_data = []
        url = f"{self.base_url}/{endpoint}"
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
                
            current_params = {'page': page, 'per_page': 100}
            if params:
                current_params.update(params)
            
            print(f"📄 Fetching {endpoint} page {page}...")
            data = self.make_request(url, current_params)
            
            if not data or len(data) == 0:
                break
                
            all_data.extend(data)
            page += 1
            
            # Small delay to be nice to GitHub API
            time.sleep(0.1)
        
        return all_data
    
    def get_shipped_milestones(self):
        """Get all milestones that are shipped/closed"""
        print("🎯 Fetching all milestones...")
        
        # Get both open and closed milestones
        all_milestones = []
        
        # Get closed milestones (shipped)
        closed_milestones = self.get_all_paginated_data('milestones', {'state': 'closed'})
        if closed_milestones:
            all_milestones.extend(closed_milestones)
        
        # Get open milestones (check if any are marked as shipped)
        open_milestones = self.get_all_paginated_data('milestones', {'state': 'open'})
        if open_milestones:
            all_milestones.extend(open_milestones)
        
        # Filter for shipped milestones
        shipped_milestones = []
        for milestone in all_milestones:
            title = milestone.get('title', '').lower()
            state = milestone.get('state', '')
            
            # Check if milestone is shipped based on title or state
            is_shipped = (
                'shipped' in title or
                'release' in title or
                state == 'closed' or
                title.startswith('v') or  # Version tags like v1.0.0
                any(keyword in title for keyword in ['0.', '1.', '2.', '3.']) # Version numbers
            )
            
            if is_shipped:
                shipped_milestones.append({
                    'number': milestone.get('number'),
                    'title': milestone.get('title'),
                    'state': milestone.get('state'),
                    'description': milestone.get('description', ''),
                    'created_at': milestone.get('created_at'),
                    'updated_at': milestone.get('updated_at'),
                    'closed_at': milestone.get('closed_at'),
                    'due_on': milestone.get('due_on'),
                    'url': milestone.get('html_url')
                })
        
        print(f"📊 Found {len(shipped_milestones)} shipped milestones")
        for milestone in shipped_milestones:
            print(f"  - {milestone['title']} ({milestone['state']})")
        
        self.shipped_milestones = shipped_milestones
        return shipped_milestones
    
    def get_prs_for_shipped_milestones(self):
        """Get all PRs associated with shipped milestones"""
        print("🔍 Fetching PRs for shipped milestones...")
        
        milestone_prs = {}
        
        for milestone in self.shipped_milestones:
            milestone_number = milestone['number']
            milestone_title = milestone['title']
            
            print(f"📋 Getting PRs for milestone: {milestone_title}")
            
            # Search for PRs associated with this milestone
            search_url = f"https://api.github.com/search/issues"
            params = {
                'q': f'repo:{self.owner}/{self.repo} type:pr milestone:"{milestone_title}"',
                'per_page': 100,
                'sort': 'created',
                'order': 'desc'
            }
            
            search_response = self.make_request(search_url, params)
            
            if search_response and search_response.get('items'):
                prs = []
                for item in search_response['items']:
                    # Get detailed PR info
                    pr_number = item.get('number')
                    pr_url = f"{self.base_url}/pulls/{pr_number}"
                    pr_detail = self.make_request(pr_url)
                    
                    if pr_detail:
                        prs.append({
                            'number': pr_detail.get('number'),
                            'title': pr_detail.get('title'),
                            'state': pr_detail.get('state'),
                            'merged': pr_detail.get('merged', False),
                            'created_at': pr_detail.get('created_at'),
                            'merged_at': pr_detail.get('merged_at'),
                            'closed_at': pr_detail.get('closed_at'),
                            'author': pr_detail.get('user', {}).get('login', ''),
                            'url': pr_detail.get('html_url')
                        })
                
                milestone_prs[milestone_title] = {
                    'milestone_info': milestone,
                    'prs': prs,
                    'pr_count': len(prs)
                }
                
                print(f"  ✅ Found {len(prs)} PRs for {milestone_title}")
            else:
                print(f"  ⚠️ No PRs found for {milestone_title}")
        
        return milestone_prs
    
    def get_commits_for_prs(self, milestone_prs):
        """Get all commits for PRs in shipped milestones"""
        print("🔗 Fetching commits for milestone PRs...")
        
        milestone_commits = {}
        
        for milestone_title, milestone_data in milestone_prs.items():
            print(f"📝 Processing commits for milestone: {milestone_title}")
            
            all_commits = []
            users_commits = defaultdict(lambda: defaultdict(list))
            
            for pr in milestone_data['prs']:
                pr_number = pr['number']
                print(f"  Getting commits for PR #{pr_number}: {pr['title'][:50]}...")
                
                # Get commits for this PR
                commits_url = f"{self.base_url}/pulls/{pr_number}/commits"
                pr_commits = self.make_request(commits_url)
                
                if pr_commits:
                    for commit in pr_commits:
                        try:
                            # Extract commit info
                            commit_info = commit.get('commit', {})
                            author_info = commit_info.get('author', {})
                            
                            # Get author details
                            author_name = author_info.get('name', 'Unknown')
                            author_email = author_info.get('email', 'unknown@example.com')
                            commit_date = author_info.get('date', '')
                            commit_sha = commit.get('sha', '')
                            
                            # Parse date
                            if commit_date:
                                try:
                                    parsed_date = datetime.fromisoformat(commit_date.replace('Z', '+00:00'))
                                    date_key = parsed_date.strftime('%Y-%m-%d')
                                except:
                                    date_key = commit_date.split('T')[0] if 'T' in commit_date else commit_date
                            else:
                                date_key = 'unknown-date'
                            
                            # Create commit record
                            commit_record = {
                                'sha': commit_sha,
                                'message': commit_info.get('message', ''),
                                'date': commit_date,
                                'time': parsed_date.strftime('%H:%M:%S') if commit_date else 'unknown',
                                'author_name': author_name,
                                'author_email': author_email,
                                'url': commit.get('html_url', ''),
                                'pr_number': pr_number,
                                'pr_title': pr['title'],
                                'pr_url': pr['url'],
                                'milestone': milestone_title
                            }
                            
                            all_commits.append(commit_record)
                            
                            # Store by user and date
                            user_key = f"{author_name} <{author_email}>"
                            users_commits[user_key][date_key].append(commit_record)
                            
                        except Exception as e:
                            print(f"    ⚠️ Error processing commit {commit.get('sha', 'unknown')}: {e}")
                            continue
            
            # Convert defaultdict to regular dict
            users_commits_dict = {
                user: dict(dates) for user, dates in users_commits.items()
            }
            
            # Calculate user statistics for this milestone
            user_stats = {}
            for user, dates in users_commits_dict.items():
                total_commits = sum(len(commits) for commits in dates.values())
                prs_contributed = len(set(commit['pr_number'] for date_commits in dates.values() for commit in date_commits))
                
                user_stats[user] = {
                    'total_commits': total_commits,
                    'prs_contributed': prs_contributed,
                    'active_days': len(dates),
                    'first_commit': min(dates.keys()) if dates else None,
                    'last_commit': max(dates.keys()) if dates else None
                }
            
            milestone_commits[milestone_title] = {
                'milestone_info': milestone_data['milestone_info'],
                'total_commits': len(all_commits),
                'total_prs': len(milestone_data['prs']),
                'users': users_commits_dict,
                'user_stats': user_stats,
                'all_commits': all_commits
            }
            
            print(f"  ✅ Found {len(all_commits)} commits from {len(users_commits_dict)} users")
        
        return milestone_commits
    
    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        filepath = os.path.join(OUTPUT_DIR, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved to: {filepath}")
        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")
    
    def run_analysis(self):
        """Run complete shipped milestone analysis"""
        print(f"🚀 Starting Shipped Milestone Analysis for {self.owner}/{self.repo}")
        print("=" * 70)
        
        # Step 1: Get shipped milestones
        shipped_milestones = self.get_shipped_milestones()
        
        if not shipped_milestones:
            print("❌ No shipped milestones found")
            return
        
        # Step 2: Get PRs for shipped milestones
        milestone_prs = self.get_prs_for_shipped_milestones()
        
        if not milestone_prs:
            print("❌ No PRs found for shipped milestones")
            return
        
        # Step 3: Get commits for those PRs
        milestone_commits = self.get_commits_for_prs(milestone_prs)
        
        # Step 4: Create comprehensive output
        output_data = {
            'repository': f"{self.owner}/{self.repo}",
            'extracted_at': datetime.now().isoformat(),
            'analysis_type': 'shipped_milestones_only',
            'timeframe': {
                'days_back': self.days_back,
                'from_date': self.cutoff_date.isoformat(),
                'to_date': datetime.now(timezone.utc).isoformat()
            },
            'summary': {
                'total_shipped_milestones': len(shipped_milestones),
                'total_prs_in_shipped_milestones': sum(data['total_prs'] for data in milestone_commits.values()),
                'total_commits_in_shipped_milestones': sum(data['total_commits'] for data in milestone_commits.values()),
                'milestones_analyzed': list(milestone_commits.keys())
            },
            'shipped_milestones': milestone_commits
        }
        
        # Step 5: Save results
        filename = f"shipped_milestones_commit_history.json"
        self.save_to_json(output_data, filename)
        
        # Step 6: Print summary
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"=" * 50)
        print(f"🎯 Shipped milestones found: {len(shipped_milestones)}")
        print(f"📋 Total PRs analyzed: {output_data['summary']['total_prs_in_shipped_milestones']}")
        print(f"📝 Total commits found: {output_data['summary']['total_commits_in_shipped_milestones']}")
        
        print(f"\n🏷️ Shipped milestones analyzed:")
        for milestone_title, data in milestone_commits.items():
            print(f"  - {milestone_title}: {data['total_commits']} commits, {data['total_prs']} PRs")
        
        print(f"\n✅ Analysis complete! Data saved to: {OUTPUT_DIR}/{filename}")

def main():
    """Main function"""
    print("🔍 Shipped Milestone Commit History Analyzer")
    print("=" * 50)
    
    # Configuration
    DAYS_BACK = 90  # Look back further to catch more shipped milestones
    
    analyzer = ShippedMilestoneAnalyzer(
        token=GITHUB_TOKEN,
        owner=REPO_OWNER,
        repo=REPO_NAME,
        days_back=DAYS_BACK
    )
    
    analyzer.run_analysis()

if __name__ == "__main__":
    main()