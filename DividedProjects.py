import os

# Function to divide the list of repos
def divide_repos(input_file, num_members):
    with open(input_file, 'r') as file:
        repos = file.readlines()
    
    repos = [repo.strip() for repo in repos if repo.strip()]
    
    size = len(repos) // num_members
    remainder = len(repos) % num_members  # For uneven division
    
    # Get the directory of the input file to save the 5 txt files there
    output_dir = os.path.dirname(input_file)
    
    # Create files for each member
    for i in range(num_members):
        start_index = i * size + min(i, remainder)
        end_index = start_index + size + (1 if i < remainder else 0)
        team_repos = repos[start_index:end_index]
        
        # Specify the path and file name
        output_file = os.path.join(output_dir, f'team_member_{i + 1}_repos.txt')
        with open(output_file, 'w') as out_file:
            for repo in team_repos:
                out_file.write(repo + '\n')
        print(f'{output_file} created with {len(team_repos)} repos.')
    
if __name__ == '__main__':

    input_file = 'UniqueRepositoriesOutput/uniqueRepositories.txt'
    
    num_members = 5
    
    if os.path.exists(input_file):
        divide_repos(input_file, num_members)
    else:
        print(f'Error: {input_file} does not exist!')
