import subprocess
import time
import RefactoringRunner
import DeveloperEffort
import shutil
import os

number_of_repositories_to_analyse = 1

repositoriesInfoFilePath = 'UniqueRepositoriesOutput/uniqueRepositories.txt'
f = open(repositoriesInfoFilePath, "r")
repos_string = f.read()
f.close()

repos_list = repos_string.splitlines()

repositories_analysed = 0
for repository in repos_list:
    print(repository)
    start = time.time()
    
    # Run RefactoringRunner and get paths
    cloned_repo_path, refminer_output_path = RefactoringRunner.main(repository)
    
    end = time.time()
    print(f'ran: {repository} elapsed: {end - start}')
    repositories_analysed += 1

    # If both the repo and refactoring output are available, run DeveloperEffort analysis
    if cloned_repo_path and refminer_output_path:
        print("Proceeding to DeveloperEffort analysis...")

        repo_name = repository.split('/')[-1]

        output_csv_path = os.path.join('DeveloperEffortOutputs', f'developer_effort_{repo_name}.csv')

        # Run DeveloperEffort
        DeveloperEffort.collect_refactoring_developer_effort(cloned_repo_path, refminer_output_path, output_csv_path)

        # Remove the cloned repository
        print(f"Deleting the cloned repository at {cloned_repo_path}...")
        shutil.rmtree(cloned_repo_path, ignore_errors=True)
        print(f"Repository at {cloned_repo_path} deleted.")
    else:
        print("Error: Failed to clone the repository or generate RefactoringMiner output.")

    if repositories_analysed >= number_of_repositories_to_analyse:
        break

print("runner finished")