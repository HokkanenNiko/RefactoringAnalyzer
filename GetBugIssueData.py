import requests
import re
import json
import os
import argparse
import time
from datetime import datetime

def ensure_valid_http_result(status):
    return status < 400

def run_http_query(endpoint, user, token, print_result = False, terminate_on_invalid_response = True):
    r = requests.get(endpoint, auth=(user, token))
    if(ensure_valid_http_result(r.status_code) == False):
        print(f'failed to fetch information from endpoint: {endpoint}. Result: {r.text}')
        if(terminate_on_invalid_response):
            raise Exception(f"invalid response:{r.status_code} from endpoint:{endpoint}")
        else:
            return None
    if(print_result):
        print(f'result: {r.content}')
        print(f'header: {r.headers}')
    return r

def get_repository_owner(repository_url):
    match = re.search(r"github\.com/([^/]+)/", repository_url)
    owner = match.group(1) if match else None
    return owner

def get_repository(repository_url):
    match = re.search(r"github\.com/[^/]+/([^/]+)", repository_url)
    repo_name = match.group(1) if match else None
    return repo_name

def ensure_api_limit_respect(remaining, used, reset):
    remaining_int = int(remaining)
    if(remaining_int < RATE_LIMIT_RESTRICT_THRESHOLD):
        time_until_reset = float(calculate_time_until_rate_reset(reset))
        sleep_time = 5
        if(time_until_reset != 0 and remaining_int != 0):
            sleep_time = (time_until_reset / remaining_int) + 0.1
        print(f'sleeping for: {sleep_time} remaining: {remaining}. used: {used}.')
        time.sleep(sleep_time)
        return

def calculate_time_until_rate_reset(reset):
    ts = float(reset)
    tsUtc = datetime.utcfromtimestamp(ts).timestamp() # UTC conversion
    now = float(datetime.utcnow().timestamp())
    reset_in = tsUtc - now
    print(f'reset in: {reset_in}')
    return reset_in

# function that filters bug issues
def bug_filter(issue):
    bug_id = "bug"
    labels = issue['labels']
    issue_type = ''
    if(len(labels) > 0):
        issue_type = issue['labels'][0]['name']
    return issue_type.lower() == bug_id

# appends info to the index.txt file
def update_results_index_file(result):
    output_file_path = f'{os.path.dirname(__file__)}' + f'./BugIssueDataOutputs/run_results.txt'
    with open(output_file_path, 'a') as file:
        file.write(result + "\n")

### Gets items with support for pagination ###
def get_items(endpoint, user, token, items_key=''):
    r = run_http_query(endpoint, user, token)

    rate_used = int(r.headers['X-RateLimit-Used'])
    rate_remaining = int(r.headers['X-RateLimit-Remaining'])
    rate_reset = r.headers['X-RateLimit-Reset']
    ensure_api_limit_respect(rate_remaining, rate_used, rate_reset)
    if(rate_remaining < 0):
        rate_remaining = 5000
        rate_used = 0

    items = list(r.json())
    content = r.links.get('next')
    if(content == None):
        return items
    url = content['url']
    while content != None:
        url = content['url']
        r = run_http_query(url, user, token)

        rate_used = int(r.headers['X-RateLimit-Used'])
        rate_remaining = int(r.headers['X-RateLimit-Remaining'])
        rate_reset = r.headers['X-RateLimit-Reset']
        ensure_api_limit_respect(rate_remaining, rate_used, rate_reset)
        if(rate_remaining < 0):
            rate_remaining = 5000
            rate_used = 0

        for issue in list(r.json()):
            items.append(issue)
        content = r.links.get('next')
    only_issues = list((x for x in items if "pull_request" not in x)) # this removes pull requests from the list, which Github API returns from the issues endpoint for some reason. 
    return only_issues

def get_issue_info(search_endpoint, user, token):
    issues = get_items(search_endpoint, user, token, items_key='items')
    return issues

MAX_SEARCH_RESULTS_PER_PAGE = 100
RATE_LIMIT_RESTRICT_THRESHOLD = 2000 # in essence this ensures that a minor delay is issued between every Github API call.

def main(user, token, repository_url):
    user = user
    token = token

    try:
        owner = get_repository_owner(repository_url)
        if(owner == None):
            print(f'could not find owner for repository:{repository_url}. Terminating run..')
        repository = get_repository(repository_url)
        if(repository == None):
            print(f'could not find repository name for repository address:{repository_url}. Terminating run..')

        uses_github_as_ITS = None
        r = run_http_query(f"https://api.github.com/repos/{owner}/{repository}", user, token)
        repo_uses_github_issue_tracking = r.json()["has_issues"]
        uses_github_as_ITS = repo_uses_github_issue_tracking
        if(not repo_uses_github_issue_tracking):
            run_results = f'"repository":{repository}, "result":True, "github_ITS": {uses_github_as_ITS}, "timestamp":{datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")}"'
            update_results_index_file(run_results)
            return
        search_url_issues = f"https://api.github.com/repos/{owner}/{repository}/issues?state=all&per_page=100" #f"https://api.github.com/search/issues?per_page={MAX_SEARCH_RESULTS_PER_PAGE}&q=is:issue%20repo:{owner}/{repository}"

        issues = get_issue_info(search_url_issues, user, token)

        # Filter is NOT used at the moment to get only bug related issues. The instructions seem unclear. Will need to resolve later.
        #issues_bug_list = list(filter(bug_filter, issues))

        # Output results
        json_object = json.dumps(issues, indent=4)
        output_file_path = f'{os.path.dirname(__file__)}' + f'./BugIssueDataOutputs/{repository}.json'
        with open(output_file_path, 'w') as file:
            file.write(json_object)
        run_results = f'"repository":{repository}, "result":True, "github_ITS": {uses_github_as_ITS}, "issues_count": "{len(issues)}", "timestamp":{datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")}"'
        update_results_index_file(run_results)
    except Exception as e:
        run_results = f'"repository":{repository}, "result":Fail, "github_ITS": {uses_github_as_ITS}, "exception": "{e}", "timestamp":{datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")}"'
        update_results_index_file(run_results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch GitHub repository information.")
    parser.add_argument("--user", required=True, help="GitHub username")
    parser.add_argument("--token", required=True, help="GitHub access token")
    parser.add_argument("--repository_url", required=True, help="URL of the Github repository")
    args = parser.parse_args()

    main(args.user, args.token, args.repository_url)