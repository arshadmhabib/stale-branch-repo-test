from datetime import datetime, timedelta
from github import Github

# GitHub authentication
g = Github("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")

# Get the repository
repo = g.get_repo("arshadmhabib/stale-branch-repo-test")

# Define the threshold for stale branches (e.g., 30 days)
threshold_days = 30
threshold_date = datetime.now() - timedelta(days=threshold_days)

# Iterate through branches
for branch in repo.get_branches():
    # Check if branch is stale
    if branch.commit.commit.author.date < threshold_date:
        # Remind branch owner via GitHub notification
        owner = branch.commit.author.login
        reminder_msg = f"Hello @{owner}, please delete your stale branch '{branch.name}' in repository {repo.full_name}."
        repo.create_issue(title="Reminder: Delete Stale Branch", body=reminder_msg, assignees=[owner])
        # Optionally, delete stale branches after a certain period of time
        # repo.get_git_ref(f"heads/{branch.name}").delete()
