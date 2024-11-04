import requests
import json
import os
import argparse
from datetime import datetime

JIRA_BASE_URL = "https://issues.apache.org/jira/rest/api/2/"
SEARCH_URL = f"{JIRA_BASE_URL}search"
PROJECT_URL = f"{JIRA_BASE_URL}project"

def ensure_valid_http_result(status):
    return status < 400

def run_http_query(endpoint, token, print_result=False, terminate_on_invalid_response=True):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = requests.get(endpoint, headers=headers)
    if not ensure_valid_http_result(r.status_code):
        print(f'Failed to fetch information from endpoint: {endpoint}. Result: {r.text}')
        if terminate_on_invalid_response:
            raise Exception(f"Invalid response: {r.status_code} from endpoint: {endpoint}")
        else:
            return None
    if print_result:
        print(f'Result: {r.content}')
        print(f'Header: {r.headers}')
    return r

def update_results_index_file(result):
    output_file_path = f'{os.path.dirname(__file__)}/BugIssueDataOutputs/run_results.txt'
    with open(output_file_path, 'a') as file:
        file.write(result + "\n")

def get_projects(token):
    """Fetch JIRA projects and retain only single-word keys."""
    projects = []
    r = run_http_query(PROJECT_URL, token)
    
    if r:
        for project in r.json():
            project_key = project.get("key", "").lower()
            if project_key.isalpha() and len(project_key.split()) == 1:
                projects.append(project_key)
    return projects

def get_items(endpoint, token):
    """Retrieve all bug issues from JIRA with pagination support."""
    issues = []
    r = run_http_query(endpoint, token)

    items = r.json().get('issues', [])
    issues.extend(items)

    total = r.json().get('total', 0)
    start_at = r.json().get('startAt', 0)
    max_results = r.json().get('maxResults', 50)

    while start_at + max_results < total:
        start_at += max_results
        paginated_endpoint = f"{endpoint}&startAt={start_at}"
        r = run_http_query(paginated_endpoint, token)
        items = r.json().get('issues', [])
        issues.extend(items)

    return issues

def get_issue_info(project_key, token):
    """Get JIRA bug issues for a specified project."""
    search_endpoint = f"{SEARCH_URL}?jql=project={project_key} AND issuetype=Bug&maxResults=50"
    issues = get_items(search_endpoint, token)
    return issues

def get_base_repo_name(repository):
    """Extract base repository name from the URL and sanitize it by removing hyphens."""
    return repository.split('/')[-1].lower().replace('-', '')  

def main(token, repository):
    try:
        projects = get_projects(token)

        base_repo_name = get_base_repo_name(repository)  

        if base_repo_name in projects:  
            print(f"Fetching bug-fixing issues for JIRA project: {base_repo_name}")
            issues = get_issue_info(base_repo_name, token)

            json_object = json.dumps(issues, indent=4)
            output_file_path = f'{os.path.dirname(__file__)}/BugIssueDataOutputs/jira_{base_repo_name}.json'
            with open(output_file_path, 'w') as file:
                file.write(json_object)

            run_results = f'"project":{base_repo_name}, "result":True, "issues_count": "{len(issues)}", "timestamp":{datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")}"'
            update_results_index_file(run_results)
            print(f"Successfully fetched issues for {base_repo_name}.")
        else:
            print(f"No matching JIRA project found for repository: {base_repo_name}")

    except Exception as e:
        run_results = f'"project":None, "result":Fail, "exception": "{str(e)}", "timestamp":{datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")}"'
        update_results_index_file(run_results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch bug-fixing issues from JIRA.")
    parser.add_argument("--token", required=True, help="JIRA API token")
    parser.add_argument("--repository", required=True, help="Repository URL to match")
    args = parser.parse_args()

    main(args.token, args.repository)
