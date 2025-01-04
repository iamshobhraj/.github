import os
import requests
import json

def get_user_type(owner, repo, username, token):
    url = f'https://api.github.com/repos/{owner}/{repo}/collaborators/{username}'
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.status_code

def add_label(owner, repo, issue_number, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels"
    headers = {"Authorization": f"token {token}"}
    data = {"labels": ["community-contribution-in-progress"]}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

def remove_label(owner, repo, issue_number, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels/community-contribution-in-progress"
    headers = {"Authorization": f"token {token}"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()

def main():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    with open(event_path, "r") as f:
        event_data = json.load(f)

    issue = event_data["issue"]
    issue_number = issue["number"]
    repo = os.getenv("GITHUB_REPOSITORY")
    owner, repo_name = repo.split("/")
    action = event_data["action"]

    if action == "unassigned":
        assignee = event_data.get("changes", {}).get("assignee", {}).get("from", {}).get("login")
    else:
        assignee = issue.get("assignee", {}).get("login")

    token = os.getenv("token")
    user_type = get_user_type(owner, repo_name, assignee, token)

    if action == "assigned" and user_type == 404:
        add_label(owner, repo_name, issue_number, token)
    elif action == "unassigned" and user_type == 404:
        remove_label(owner, repo_name, issue_number, token)

if __name__ == "__main__":
    main()
