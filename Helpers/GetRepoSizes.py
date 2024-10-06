import requests
import re
import json
import os
import argparse

class RepositoryInformation:
    github_owner = ''
    github_repository = ''
    github_url = ''

    def __init__(self, github_owner, github_repository):
        self.github_owner = github_owner
        self.github_repository = github_repository
        self.github_url = f'https://api.github.com/repos/{github_owner}/{github_repository}'

def ensureValidHttpResult(status):
    return status < 400

def runHttpQuery(endpoint, user, token, printResult = False, terminateOnInvalidResponse = True):
    r = requests.get(endpoint, auth=(user, token))
    if(ensureValidHttpResult(r.status_code) == False):
        print(f'failed to fetch information from endpoint: {endpoint}. Result: {r.text}')
        if(terminateOnInvalidResponse):
            exit -1
        else:
            return None
    if(printResult):
        print(f'result: {r.content}')
    return r

def GetRepositoryOwner(repositoryUrl):
    # Extract the owner of the repository from the given URL

    # Use regex to find the owner (second part after the domain)
    match = re.search(r"github\.com/([^/]+)/", repositoryUrl)

    # Extract owner if found
    owner = match.group(1) if match else None
    return owner

def GetRepository(repositoryUrl):
    # Extract the repository name of the repository from the given URL

    # Use regex to find the owner (second part after the domain)
    match = re.search(r"github\.com/[^/]+/([^/]+)", repositoryUrl)

    # Extract owner if found
    repoName = match.group(1) if match else None
    return repoName

### KEYS ###
language_key = 'language'
collaborators_key = 'collaborators_url'
created_at_key = 'created_at'
commits_key = 'commits_url'
open_issues_key = 'open_issues'
issues_key = 'issues_url'
size_key = 'size'

def main(user, token):
    dictionary =  []
    user = user
    token = token
    repositoriesInfoFilePath = f'{os.path.dirname(__file__)}' + '/../UniqueRepositoriesOutput/uniqueRepositories.txt'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    with open(repositoriesInfoFilePath, "r") as f:
        repos_string = f.read()

    repos_list = repos_string.splitlines()
    counter = 0
    max_counter = 10000
    total_size = 0

    for repo in repos_list:
        if(counter >= max_counter):
            continue
        owner = GetRepositoryOwner(repo)
        if(owner == None):
            print(f'could not find owner for repository:{repo}. Terminating run..')
        repository = GetRepository(repo)
        if(repository == None):
            print(f'could not find repository name for repository address:{repo}. Terminating run..')
        repositoryItem = RepositoryInformation(owner, repository)
        r = runHttpQuery(repositoryItem.github_url, user=user, token=token, terminateOnInvalidResponse=False)
        counter += 1
        print(f'{counter}/{len(repos_list)}')
        
        if(r is None):
            dictionary.append({"RepositoryOwner": owner, "RepositoryName": repository, f'{size_key}': -1, "Result": "Fail"})
            continue

        size = r.json()[size_key]

        repoDictionary = {
            "RepositoryOwner": owner,
            "RepositoryName": repository,
            size_key: size
        }
        dictionary.append(repoDictionary)
        total_size += size


    sortedList = sorted(dictionary, key=lambda d: d[size_key])
    sortedList.insert(0, {'TotalSize': total_size})


    # Serializing json
    json_object = json.dumps(sortedList, indent=4)
    # Writing to sample.json
    outputFilePath = f'{os.path.dirname(__file__)}' + '/../RepoSizesOutput/RepoSizesOutput.json'
    with open(outputFilePath, 'w') as file:
        file.write(json_object)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch GitHub repository information.")
    parser.add_argument("--user", required=True, help="GitHub username")
    parser.add_argument("--token", required=True, help="GitHub access token")
    args = parser.parse_args()

    main(args.user, args.token)