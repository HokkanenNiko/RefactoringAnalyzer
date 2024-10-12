import os
import shutil
import time
import argparse
import DeveloperEffort
import RefactoringRunner
from LoggerManager import get_logger
from GetBugIssueData import main as issue_data

def main(user, token):
    user = user
    token = token

    # Loggers
    refactoring_runner_logger = get_logger("RefactoringRunner")

    number_of_repositories_to_analyse = 1

    repositoriesInfoFilePath = 'UniqueRepositoriesOutput/uniqueRepositories.txt'
    with open(repositoriesInfoFilePath, "r") as f:
        repos_string = f.read()

    repos_list = repos_string.splitlines()

    repositories_analysed = 0

    for repository in repos_list:
        refactoring_runner_logger.info(repository)
        start = time.time()

        try:
            issue_data(user, token, repository)
            # Run RefactoringRunner and get paths
            cloned_repo_path, refminer_output_path = RefactoringRunner.main(repository, refactoring_runner_logger)

            end = time.time()
            refactoring_runner_logger.info(f'ran: {repository} elapsed: {end - start:.2f}')
            refactoring_runner_logger.info("RefactoringRunner finished")

            repositories_analysed += 1
            print(f'{repositories_analysed} / {len(repos_list)}')

            # If both the repo and refactoring output are available, run DeveloperEffort analysis
            if cloned_repo_path and refminer_output_path:
                refactoring_runner_logger.info("Proceeding to DeveloperEffort analysis...")

                repo_name = repository.split('/')[-1]
                output_csv_path = os.path.join('DeveloperEffortOutputs', f'developer_effort_{repo_name}.csv')

                # Run DeveloperEffort
                DeveloperEffort.collect_refactoring_developer_effort(cloned_repo_path, refminer_output_path, output_csv_path)

                # Remove the cloned repository
                refactoring_runner_logger.info(f"Deleting the cloned repository at {cloned_repo_path}...")
                shutil.rmtree(cloned_repo_path, ignore_errors=True)
                refactoring_runner_logger.info(f"Repository at {cloned_repo_path} deleted.")
            else:
                refactoring_runner_logger.error("Failed to clone the repository or generate RefactoringMiner output.")

        except Exception as e:
            refactoring_runner_logger.error(f"An error occurred while processing {repository}: {e}", exc_info=True)

        if repositories_analysed >= number_of_repositories_to_analyse:
            break

    refactoring_runner_logger.info(f"Runner finished. Total repositories analyzed: {repositories_analysed}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch GitHub repository information.")
    parser.add_argument("--user", required=True, help="GitHub username")
    parser.add_argument("--token", required=True, help="GitHub access token")
    args = parser.parse_args()

    main(args.user, args.token)