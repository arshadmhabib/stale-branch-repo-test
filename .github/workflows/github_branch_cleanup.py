import os
import requests
from datetime import datetime, timedelta

# GitHub API endpoint
github_api_url = 'https://api.github.com'
# Email subject and body for reminder
reminder_subject = 'Reminder: Delete Stale Branches'
reminder_body = 'Hello, please remember to delete your stale branches on GitHub.'
# Time to wait before sending a reminder (in days)
reminder_interval_days = 7
# Time to wait before deleting the stale branches (in days)
delete_interval_days = 14

def send_reminder_email(branch_owner, branch_name):
    # Simulate sending an email (replace with actual email sending logic if available)
    print(f"Reminder email sent to {branch_owner} for stale branch: {branch_name}")

def get_stale_branches(repo_name, github_token):
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(f"{github_api_url}/repos/{os.environ['GITHUB_REPOSITORY']}/branches", headers=headers)
    branches = response.json()
    
    stale_branches = []
    for branch in branches:
        last_commit_date = datetime.strptime(branch['commit']['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
        if datetime.utcnow() - last_commit_date > timedelta(days=delete_interval_days):
            stale_branches.append(branch['name'])
    
    return stale_branches

def main():
    github_token = os.environ['GITHUB_TOKEN']
    repo_name = os.environ['GITHUB_REPOSITORY']
    stale_branches = get_stale_branches(repo_name, github_token)
    
    for branch_name in stale_branches:
        send_reminder_email(os.environ['GITHUB_ACTOR'], branch_name)
    
    # Wait for the reminder interval before deleting stale branches
    print(f"Waiting for {reminder_interval_days} days before deleting stale branches.")
    os.system(f"sleep {reminder_interval_days * 24 * 3600}")
    
    # Delete stale branches
    for branch_name in stale_branches:
        delete_branch(repo_name, branch_name, github_token)

def delete_branch(repo_name, branch_name, github_token):
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.delete(f"{github_api_url}/repos/{os.environ['GITHUB_REPOSITORY']}/git/refs/heads/{branch_name}", headers=headers)
    if response.status_code == 204:
        print(f"Stale branch {branch_name} deleted successfully.")
    else:
        print(f"Failed to delete stale branch {branch_name}. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
