import os
import requests
import json

def get_user_type(username, token):
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("type")

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
    event = os.getenv("GITHUB_EVENT_NAME")
    with open(event, "r") as f:
        event_data = json.load(f)

    issue = event_data["issue"]
    issue_number = issue["number"]
    repo = os.getenv("GITHUB_REPOSITORY")
    owner, repo_name = repo.split("/")
    action = event_data["action"]
    assignee = issue["assignee"]["login"]

    token = os.getenv("GITHUB_TOKEN")
    user_type = get_user_type(assignee, token)

    if action == "assigned" and user_type not in ["Member"]:
        add_label(owner, repo_name, issue_number, token)
    elif action == "unassigned" and user_type not in ["Member"]:
        remove_label(owner, repo_name, issue_number, token)

if __name__ == "__main__":
    main()
