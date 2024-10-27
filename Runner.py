import os
import shutil
import time
import argparse
import DeveloperEffort
import RefactoringRunner
from LoggerManager import get_logger
from GetBugIssueData import main as issue_data
from ProduceUniqueRepos import main as get_unique_repos
from GetGitDiff import get_commit_diff

def get_unique_repos_list():
    repositoriesInfoFilePath = get_unique_repos() # step a)

    with open(repositoriesInfoFilePath, "r") as f:
        repos_string = f.read()

    repos_list = repos_string.splitlines()
    return repos_list

def run_refactoring_miner(repository, refactoring_runner_logger):
    start = time.time()
    cloned_repo_path, refminer_output_path = RefactoringRunner.main(repository, refactoring_runner_logger)            # step b) and c)

    end = time.time()
    refactoring_runner_logger.info(f'ran: {repository} elapsed: {end - start:.2f}')
    refactoring_runner_logger.info("RefactoringRunner finished")
    return cloned_repo_path, refminer_output_path

def main(user, token, single_repository):
    user = user
    token = token

    number_of_repositories_to_analyse = 1

    # Loggers
    refactoring_runner_logger = get_logger("RefactoringRunner")

    repos_list = get_unique_repos_list()                                                                                      # step a)

    repositories_analysed = 0

    for repository in repos_list:
        if(single_repository is not None and repository != single_repository):
            continue

        refactoring_runner_logger.info(repository)

        try:
            cloned_repo_path, refminer_output_path = run_refactoring_miner(repository, refactoring_runner_logger)            # step b) and c)

            repositories_analysed += 1

            # If both the repo and refactoring output are available, run DeveloperEffort analysis
            if cloned_repo_path and refminer_output_path:
                refactoring_runner_logger.info("Proceeding to DeveloperEffort analysis...")

                repo_name = repository.split('/')[-1]
                output_csv_path = os.path.join('DeveloperEffortOutputs', f'developer_effort_{repo_name}.csv')

                get_commit_diff(cloned_repo_path, f'CommitDifferencesOutput/{repo_name}.json')                                # step d)                                                                   # step d)
                DeveloperEffort.collect_refactoring_developer_effort(cloned_repo_path, refminer_output_path, output_csv_path) # step e)
                issue_data(user, token, repository)                                                                           # step f)

                # Remove the cloned repository
                refactoring_runner_logger.info(f"Deleting the cloned repository at {cloned_repo_path}...")
                shutil.rmtree(cloned_repo_path, ignore_errors=True)
                refactoring_runner_logger.info(f"Repository at {cloned_repo_path} deleted.")
            else:
                refactoring_runner_logger.error("Failed to clone the repository or generate RefactoringMiner output.")
            print(f'{repositories_analysed} / {len(repos_list)}')

        except Exception as e:
            refactoring_runner_logger.error(f"An error occurred while processing {repository}: {e}", exc_info=True)

        if repositories_analysed >= number_of_repositories_to_analyse:
            break

    refactoring_runner_logger.info(f"Runner finished. Total repositories analyzed: {repositories_analysed}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch GitHub repository information.")
    parser.add_argument("--user", required=True, help="GitHub username")
    parser.add_argument("--token", required=True, help="GitHub access token")
    parser.add_argument("--repo_url", required=False, help="If this parameter is supplied, only that repository is analyzed.")
    args = parser.parse_args()

    main(args.user, args.token, args.repo_url)