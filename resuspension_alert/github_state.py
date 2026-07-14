import os
from github import Github

repo_name = os.environ["GITHUB_REPOSITORY"]
issue_title = "Grey Flag Alert Active"

g = Github(os.environ["GITHUB_TOKEN"])
repo = g.get_repo(repo_name)

def get_open_alert_issue():
    """Return the open alert issue, or None if one doesn't exist."""
    for issue in repo.get_issues(state="open"):
        if issue.title == ISSUE_TITLE:
            return issue
    return None

def alert_exists():
    return get_open_alert_issue() is not None

def create_alert_issue(body):
    repo.create_issue(
        title=ISSUE_TITLE,
        body=body
    )

def close_alert_issue():
    issue = get_open_alert_issue()

    if issue is not None:
        issue.edit(state="closed")
