import subprocess
import csv
import json
import os

def run_scc(repo_path):
    """
    Run SCC on the current checked-out state and return the total lines of code (TLOC).
    """
    try:
        result = subprocess.check_output(['scc', '--no-complexity', '--by-file', repo_path], universal_newlines=True)

        total_tloc = 0
        for line in result.splitlines():
            parts = line.split()
            if len(parts) >= 5 and parts[4].isdigit():
                total_tloc += int(parts[4])  

        return total_tloc

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running SCC: {e}")
        return 0

def calculate_tloc_with_git_diff(repo_path, commit_hash):
    """
    Calculate TLOC in a commit using git diff.
    """
    try:
        diff_result = subprocess.check_output(
            ['git', 'diff', '--numstat', commit_hash + '^!', '--'],
            cwd=repo_path, universal_newlines=True
        )

        total_tloc = 0
        for line in diff_result.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                total_tloc += int(parts[0])  # Lines added
                total_tloc += int(parts[1])  # Lines deleted

        return total_tloc

    except subprocess.CalledProcessError as e:
        print(f"Error calculating TLOC for commit {commit_hash}: {e}")
        return 0

def collect_refactoring_developer_effort(repo_path, refminer_output_path, output_csv_path):
    """
    Collect developer effort (TLOC) for commits with refactorings only and save to CSV.
    """
    with open(refminer_output_path, 'r') as json_file:
        refactorings_data = json.load(json_file)

    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Developer', 'Refactoring Hash', 'Previous Hash', 'TLOC (Touched Lines of Code)'])

        for commit in refactorings_data['commits']:
            commit_hash = commit['sha1']
            if commit['refactorings']:  # Only process commits with refactorings
                print(f"Processing commit {commit_hash} with refactorings")
                
                git_log = subprocess.check_output(
                    ['git', 'log', '--pretty=format:%P,%an', '-n', '1', commit_hash],
                    cwd=repo_path, universal_newlines=True,
                    encoding='utf-8'
                )

                git_log_split = git_log.split(',')
                parent_hash = git_log_split[0].strip()
                developer = ','.join(git_log_split[1:]).strip()

                total_tloc = calculate_tloc_with_git_diff(repo_path, commit_hash)

                writer.writerow([developer, commit_hash, parent_hash, total_tloc])
            else:
                print(f"Skipping commit {commit_hash} with no refactorings")

    print(f"Developer effort data saved to {output_csv_path}")
