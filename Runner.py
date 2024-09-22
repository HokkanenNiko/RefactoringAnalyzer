import subprocess
import time
import RefactoringRunner

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
    RefactoringRunner.main(repository)
    end = time.time()
    print(f'ran: {repository} elapsed: {end - start}')
    repositories_analysed += 1
    if(repositories_analysed >= number_of_repositories_to_analyse):
        break

print("runner finished")