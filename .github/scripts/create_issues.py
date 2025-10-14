import os
import requests

# Directory containing markdown files to be converted into GitHub Issues
issues_directory = "Issues"

# Repository and authentication token from environment variables
repository = os.environ["REPO"]
token = os.environ["GITHUB_TOKEN"]
headers = {"Authorization": f"token {token}"}

# Iterate through all markdown files in the specified directory
for filename in os.listdir(issues_directory):
    if filename.endswith(".md"):
        with open(os.path.join(issues_directory, filename), "r", encoding="utf-8") as file:
            lines = file.readlines()
            title = lines[0].strip() if lines else filename
            body = "".join(lines[1:]).strip()

        # Prepare the payload for the GitHub API
        issue_data = {
            "title": title,
            "body": body
        }

        # Send POST request to create the issue
        response = requests.post(
            f"https://api.github.com/repos/{repository}/issues",
            headers=headers,
            json=issue_data
        )

        # Output result to the workflow log
        if response.status_code == 201:
            print(f"Issue '{title}' created successfully.")
        else:
            print(f"Failed to create issue '{title}': {response.status_code} - {response.text}")
