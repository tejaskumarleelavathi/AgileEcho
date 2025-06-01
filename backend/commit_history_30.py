import os
import json
import requests
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import time
from dotenv import load_dotenv

load_dotenv()

# Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # Replace with your token
REPO_OWNER = "microsoft"
REPO_NAME = "vscode-cosmosdb"  # Change this to your target repo
OUTPUT_DIR = "github_analysis_output"

class GitHubRepoAnalyzer:
    def __init__(self, token, owner, repo, days_back=30):
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
        print(f"📅 Looking for data from {self.cutoff_date} onwards ({days_back} days ago)")
        print(f"📅 Date range: {self.cutoff_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}")
        
        # Cache for PR data to avoid repeated API calls
        self.pr_cache = {}
    
    def is_within_timeframe(self, date_string):
        """Check if a date is within the specified timeframe"""
        if not date_string:
            return False
        try:
            # Handle different date formats
            if date_string.endswith('Z'):
                date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            elif '+' in date_string or date_string.endswith('UTC'):
                date_obj = datetime.fromisoformat(date_string.replace('UTC', ''))
            else:
                date_obj = datetime.fromisoformat(date_string)
            
            # Ensure timezone awareness
            if date_obj.tzinfo is None:
                date_obj = date_obj.replace(tzinfo=timezone.utc)
            
            is_within = date_obj >= self.cutoff_date
            return is_within
        except Exception as e:
            print(f"⚠️ Date parsing error for '{date_string}': {e}")
            return False
    
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
    
    def find_commit_pr(self, commit_sha):
        """Find the PR associated with a commit"""
        if commit_sha in self.pr_cache:
            return self.pr_cache[commit_sha]
        
        try:
            # Search for PRs that include this commit
            search_url = f"https://api.github.com/search/issues"
            params = {
                'q': f'repo:{self.owner}/{self.repo} type:pr {commit_sha}',
                'per_page': 5
            }
            
            response = self.make_request(search_url, params)
            if response and response.get('items'):
                # Get the first PR that matches
                pr_item = response['items'][0]
                pr_number = pr_item.get('number')
                
                # Get detailed PR info
                pr_url = f"{self.base_url}/pulls/{pr_number}"
                pr_detail = self.make_request(pr_url)
                
                if pr_detail:
                    pr_info = {
                        'number': pr_detail.get('number'),
                        'title': pr_detail.get('title', ''),
                        'state': pr_detail.get('state', ''),
                        'merged': pr_detail.get('merged', False),
                        'url': pr_detail.get('html_url', ''),
                        'created_at': pr_detail.get('created_at', ''),
                        'merged_at': pr_detail.get('merged_at', ''),
                        'closed_at': pr_detail.get('closed_at', '')
                    }
                    
                    # Cache the result
                    self.pr_cache[commit_sha] = pr_info
                    return pr_info
            
            # No PR found
            self.pr_cache[commit_sha] = None
            return None
            
        except Exception as e:
            print(f"⚠️ Error finding PR for commit {commit_sha}: {e}")
            self.pr_cache[commit_sha] = None
            return None
    
    def extract_commit_history(self):
        """Extract commit history from last month organized by user and date"""
        print(f"🔍 Extracting commit history from last {self.days_back} days...")
        
        # Get all commits without date filtering first
        all_commits = self.get_all_paginated_data('commits')
        
        if not all_commits:
            print("❌ No commits found")
            return {}
        
        print(f"📊 Total commits fetched: {len(all_commits)}")
        
        # Filter commits within timeframe
        filtered_commits = []
        for commit in all_commits:
            commit_date = commit.get('commit', {}).get('author', {}).get('date', '')
            if commit_date and self.is_within_timeframe(commit_date):
                filtered_commits.append(commit)
        
        print(f"📊 Found {len(filtered_commits)} commits in the last {self.days_back} days")
        
        if not filtered_commits:
            print(f"❌ No commits found in the last {self.days_back} days")
            return {}
        
        # Organize commits by user and date
        commit_data = {
            'repository': f"{self.owner}/{self.repo}",
            'extracted_at': datetime.now().isoformat(),
            'timeframe': {
                'days_back': self.days_back,
                'from_date': self.cutoff_date.isoformat(),
                'to_date': datetime.now(timezone.utc).isoformat()
            },
            'total_commits': len(filtered_commits),
            'total_commits_in_repo': len(all_commits),
            'users': defaultdict(lambda: defaultdict(list))
        }
        
        print("🔗 Finding PR associations for commits...")
        for i, commit in enumerate(filtered_commits, 1):
            print(f"Processing commit {i}/{len(filtered_commits)}: {commit.get('sha', '')[:8]}...")
            
            try:
                # Extract commit info
                commit_info = commit.get('commit', {})
                author_info = commit_info.get('author', {})
                committer_info = commit_info.get('committer', {})
                
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
                
                # Find associated PR
                associated_pr = self.find_commit_pr(commit_sha)
                
                # Create commit record with PR info
                commit_record = {
                    'sha': commit_sha,
                    'message': commit_info.get('message', ''),
                    'date': commit_date,
                    'time': parsed_date.strftime('%H:%M:%S') if commit_date else 'unknown',
                    'author_name': author_name,
                    'author_email': author_email,
                    'committer_name': committer_info.get('name', ''),
                    'committer_email': committer_info.get('email', ''),
                    'url': commit.get('html_url', ''),
                    'additions': commit.get('stats', {}).get('additions', 0),
                    'deletions': commit.get('stats', {}).get('deletions', 0),
                    'total_changes': commit.get('stats', {}).get('total', 0),
                    'files_changed': len(commit.get('files', [])),
                    'associated_pr': associated_pr  # This is the new PR information
                }
                
                # Store by user and date
                user_key = f"{author_name} <{author_email}>"
                commit_data['users'][user_key][date_key].append(commit_record)
                
            except Exception as e:
                print(f"⚠️ Error processing commit {commit.get('sha', 'unknown')}: {e}")
                continue
        
        # Convert defaultdict to regular dict for JSON serialization
        commit_data['users'] = {
            user: dict(dates) for user, dates in commit_data['users'].items()
        }
        
        # Add user statistics
        commit_data['user_stats'] = {}
        for user, dates in commit_data['users'].items():
            total_commits = sum(len(commits) for commits in dates.values())
            total_additions = sum(
                commit['additions'] for date_commits in dates.values() 
                for commit in date_commits
            )
            total_deletions = sum(
                commit['deletions'] for date_commits in dates.values() 
                for commit in date_commits
            )
            
            # PR statistics for user
            commits_with_pr = sum(
                1 for date_commits in dates.values() 
                for commit in date_commits 
                if commit.get('associated_pr')
            )
            
            commit_data['user_stats'][user] = {
                'total_commits': total_commits,
                'total_additions': total_additions,
                'total_deletions': total_deletions,
                'commits_with_pr': commits_with_pr,
                'commits_without_pr': total_commits - commits_with_pr,
                'pr_percentage': round((commits_with_pr / total_commits) * 100, 1) if total_commits > 0 else 0,
                'active_days': len(dates),
                'first_commit': min(dates.keys()) if dates else None,
                'last_commit': max(dates.keys()) if dates else None
            }
        
        return commit_data
    
    def extract_pr_data(self):
        """Extract PR data from last month with timelines and milestones"""
        print(f"🔍 Extracting Pull Request data from last {self.days_back} days...")
        
        all_prs = []
        
        # Get closed PRs updated since cutoff date
        closed_prs = self.get_all_paginated_data('pulls', {
            'state': 'closed',
            'sort': 'updated',
            'direction': 'desc'
        })
        
        # Filter closed PRs to only include those updated in our timeframe
        if closed_prs:
            for pr in closed_prs:
                if (self.is_within_timeframe(pr.get('updated_at')) or 
                    self.is_within_timeframe(pr.get('created_at')) or
                    self.is_within_timeframe(pr.get('closed_at')) or
                    self.is_within_timeframe(pr.get('merged_at'))):
                    all_prs.append(pr)
        
        # Get open PRs (filter by creation/update date)
        open_prs = self.get_all_paginated_data('pulls', {
            'state': 'open',
            'sort': 'updated',
            'direction': 'desc'
        })
        
        if open_prs:
            for pr in open_prs:
                if (self.is_within_timeframe(pr.get('updated_at')) or 
                    self.is_within_timeframe(pr.get('created_at'))):
                    all_prs.append(pr)
        
        if not all_prs:
            print("❌ No PRs found in the specified timeframe")
            return {}
        
        print(f"📊 Found {len(all_prs)} PRs active in the last {self.days_back} days")
        
        pr_data = {
            'repository': f"{self.owner}/{self.repo}",
            'extracted_at': datetime.now().isoformat(),
            'timeframe': {
                'days_back': self.days_back,
                'from_date': self.cutoff_date.isoformat(),
                'to_date': datetime.now(timezone.utc).isoformat()
            },
            'total_prs': len(all_prs),
            'pull_requests': []
        }
        
        for i, pr in enumerate(all_prs, 1):
            print(f"📋 Processing PR #{pr.get('number')} ({i}/{len(all_prs)})...")
            
            try:
                # Get detailed PR timeline
                timeline_data = self.get_pr_timeline(pr['number'])
                
                # Extract basic PR info
                created_at = pr.get('created_at', '')
                updated_at = pr.get('updated_at', '')
                closed_at = pr.get('closed_at', '')
                merged_at = pr.get('merged_at', '')
                
                # Calculate duration
                duration_info = self.calculate_pr_duration(created_at, closed_at, merged_at)
                
                pr_record = {
                    'number': pr.get('number'),
                    'title': pr.get('title', ''),
                    'state': pr.get('state', ''),
                    'merged': pr.get('merged', False),
                    'author': {
                        'login': pr.get('user', {}).get('login', ''),
                        'name': pr.get('user', {}).get('name', ''),
                        'email': pr.get('user', {}).get('email', '')
                    },
                    'timeline': {
                        'created_at': created_at,
                        'updated_at': updated_at,
                        'closed_at': closed_at,
                        'merged_at': merged_at,
                        'duration_hours': duration_info['duration_hours'],
                        'duration_days': duration_info['duration_days'],
                        'status': duration_info['status']
                    },
                    'milestone': {
                        'title': pr.get('milestone', {}).get('title', '') if pr.get('milestone') else '',
                        'description': pr.get('milestone', {}).get('description', '') if pr.get('milestone') else '',
                        'state': pr.get('milestone', {}).get('state', '') if pr.get('milestone') else '',
                        'due_on': pr.get('milestone', {}).get('due_on', '') if pr.get('milestone') else '',
                        'url': pr.get('milestone', {}).get('html_url', '') if pr.get('milestone') else ''
                    },
                    'details': {
                        'body': pr.get('body', ''),
                        'url': pr.get('html_url', ''),
                        'labels': [label.get('name', '') for label in pr.get('labels', [])],
                        'assignees': [assignee.get('login', '') for assignee in pr.get('assignees', [])],
                        'reviewers': [reviewer.get('login', '') for reviewer in pr.get('requested_reviewers', [])],
                        'commits': pr.get('commits', 0),
                        'additions': pr.get('additions', 0),
                        'deletions': pr.get('deletions', 0),
                        'changed_files': pr.get('changed_files', 0)
                    },
                    'timeline_events': timeline_data
                }
                
                pr_data['pull_requests'].append(pr_record)
                
            except Exception as e:
                print(f"⚠️ Error processing PR #{pr.get('number', 'unknown')}: {e}")
                continue
        
        # Add summary statistics
        pr_data['statistics'] = self.calculate_pr_statistics(pr_data['pull_requests'])
        
        return pr_data
    
    def get_pr_timeline(self, pr_number):
        """Get detailed timeline for a specific PR"""
        timeline_url = f"{self.base_url}/issues/{pr_number}/timeline"
        timeline_events = self.make_request(timeline_url)
        
        if not timeline_events:
            return []
        
        parsed_events = []
        for event in timeline_events:
            event_data = {
                'event': event.get('event', ''),
                'created_at': event.get('created_at', ''),
                'actor': event.get('actor', {}).get('login', '') if event.get('actor') else '',
            }
            
            # Add specific event details
            if event.get('event') == 'reviewed':
                event_data['review_state'] = event.get('state', '')
            elif event.get('event') == 'labeled':
                event_data['label'] = event.get('label', {}).get('name', '')
            elif event.get('event') == 'assigned':
                event_data['assignee'] = event.get('assignee', {}).get('login', '')
            
            parsed_events.append(event_data)
        
        return parsed_events
    
    def calculate_pr_duration(self, created_at, closed_at, merged_at):
        """Calculate PR duration and status"""
        try:
            if not created_at:
                return {'duration_hours': 0, 'duration_days': 0, 'status': 'unknown'}
            
            start_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            
            if merged_at:
                end_time = datetime.fromisoformat(merged_at.replace('Z', '+00:00'))
                status = 'merged'
            elif closed_at:
                end_time = datetime.fromisoformat(closed_at.replace('Z', '+00:00'))
                status = 'closed'
            else:
                end_time = datetime.now(timezone.utc)
                status = 'open'
            
            duration = end_time - start_time
            duration_hours = duration.total_seconds() / 3600
            duration_days = duration.days + (duration.seconds / 86400)
            
            return {
                'duration_hours': round(duration_hours, 2),
                'duration_days': round(duration_days, 2),
                'status': status
            }
            
        except Exception as e:
            print(f"⚠️ Error calculating duration: {e}")
            return {'duration_hours': 0, 'duration_days': 0, 'status': 'error'}
    
    def calculate_pr_statistics(self, prs):
        """Calculate summary statistics for PRs"""
        if not prs:
            return {}
        
        merged_prs = [pr for pr in prs if pr['timeline']['status'] == 'merged']
        closed_prs = [pr for pr in prs if pr['timeline']['status'] == 'closed']
        open_prs = [pr for pr in prs if pr['timeline']['status'] == 'open']
        
        # Calculate average durations
        merged_durations = [pr['timeline']['duration_hours'] for pr in merged_prs if pr['timeline']['duration_hours'] > 0]
        avg_merge_time = sum(merged_durations) / len(merged_durations) if merged_durations else 0
        
        # Milestone statistics
        milestone_stats = defaultdict(int)
        for pr in prs:
            milestone = pr['milestone']['title']
            if milestone:
                milestone_stats[milestone] += 1
        
        # Author statistics
        author_stats = defaultdict(int)
        for pr in prs:
            author = pr['author']['login']
            if author:
                author_stats[author] += 1
        
        return {
            'total_prs': len(prs),
            'merged_prs': len(merged_prs),
            'closed_prs': len(closed_prs),
            'open_prs': len(open_prs),
            'merge_rate': round((len(merged_prs) / len(prs)) * 100, 1) if prs else 0,
            'average_merge_time_hours': round(avg_merge_time, 2),
            'average_merge_time_days': round(avg_merge_time / 24, 2),
            'milestone_distribution': dict(milestone_stats),
            'top_contributors': dict(sorted(author_stats.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        filepath = os.path.join(OUTPUT_DIR, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved to: {filepath}")
        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")
    
    def run_full_analysis(self):
        """Run complete repository analysis for the last month"""
        print(f"🚀 Starting {self.days_back}-day analysis of {self.owner}/{self.repo}")
        print("=" * 60)
        
        # Extract commit history
        print(f"\n📝 EXTRACTING COMMIT HISTORY (Last {self.days_back} days)...")
        commit_data = self.extract_commit_history()
        if commit_data:
            filename = f"commit_history_with_prs_last_{self.days_back}_days.json"
            self.save_to_json(commit_data, filename)
            print(f"📊 Found {commit_data['total_commits']} commits from {len(commit_data['users'])} users")
        
        # Extract PR data
        print(f"\n📋 EXTRACTING PULL REQUEST DATA (Last {self.days_back} days)...")
        pr_data = self.extract_pr_data()
        if pr_data:
            filename = f"pull_requests_last_{self.days_back}_days.json"
            self.save_to_json(pr_data, filename)
            print(f"📊 Found {pr_data['total_prs']} pull requests")
        
        print(f"\n✅ {self.days_back}-day analysis complete!")
        print(f"📁 Output files saved in: {OUTPUT_DIR}/")

def main():
    """Main function"""
    print("🔍 GitHub Repository Analyzer - Last 30 Days with PR Links")
    print("=" * 60)
    
    # Configuration - you can modify these values
    DAYS_BACK = 30  # Change this to get different timeframes (7, 14, 30, 60, etc.)
    
    analyzer = GitHubRepoAnalyzer(
        token=GITHUB_TOKEN,
        owner=REPO_OWNER,
        repo=REPO_NAME,
        days_back=DAYS_BACK
    )
    
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()