import json
import subprocess
import csv
import os

def run_scc(repo_path):
    """
    Run SCC on the current checked-out commit and return the TLOC (Total Lines of Code)
    """
    include_ext = 'c,cpp,h,hpp,py,java,js,rb,go,cs,php,swift,ts,rs,kt,scala,pl,sh,ps1'  # Include only these languages (can be modified)

    try:
        scc_command = f'scc --no-complexity --by-file --include-ext {include_ext}'

        result = subprocess.check_output(
            scc_command,
            shell=True,  
            cwd=repo_path,  
            universal_newlines=True
        )

        total_tloc = 0
        for line in result.splitlines():
            print(f"Processing line: {line}") 
            if "Total" in line:
                parts = line.split()
                if len(parts) >= 3 and parts[2].isdigit(): 
                    total_tloc = int(parts[2])  # Use the third value as TLOC
                    break 

        print(f"Total TLOC from SCC: {total_tloc}") 
        return total_tloc

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running SCC: {e}")
        return 0

def calculate_tloc_diff(repo_path, commit_hash):
    """
    Calculate the TLOC difference between the refactoring commit and its previous commit.
    """
    try:
        # Get the LOC for the current commit
        subprocess.check_call(['git', 'checkout', commit_hash], cwd=repo_path)
        current_tloc = run_scc(repo_path)

        # Checkout to the previous commit
        subprocess.check_call(['git', 'checkout', commit_hash + '^'], cwd=repo_path)
        previous_tloc = run_scc(repo_path)

        # The absolute difference between the two TLOCs
        tloc_diff = abs(current_tloc - previous_tloc)
        return tloc_diff, current_tloc, previous_tloc

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while calculating TLOC difference for commit {commit_hash}: {e}")
        return 0, 0, 0

def collect_refactoring_developer_effort(repo_path, refminer_output_path, output_csv_path):
    """
    Collect developer effort for refactorings and store the results in a CSV file.
    """
    with open(refminer_output_path, 'r') as json_file:
        refactorings_data = json.load(json_file)

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Add columns for both current and previous LOC
        writer.writerow(['Developer', 'Refactoring Hash', 'Previous Hash', 'TLOC (Touched Lines of Code)', 'Current LOC', 'Previous LOC'])

        # Iterate over the commits with refactorings
        for commit in refactorings_data['commits']:
            commit_hash = commit['sha1']
            if commit['refactorings']:  # Only consider commits with refactorings
                print(f"Processing commit {commit_hash} with refactorings")

                # Get commit metadata (developer and parent hash)
                git_log = subprocess.check_output(
                    ['git', 'log', '--pretty=format:%P,%an', '-n', '1', commit_hash],
                    cwd=repo_path, universal_newlines=True, encoding='utf-8'
                )
                parent_hash, developer = git_log.split(',', 1)

                # Calculate the TLOC difference and get current and previous LOC
                tloc_diff, current_tloc, previous_tloc = calculate_tloc_diff(repo_path, commit_hash)

                # Write the results to the CSV
                writer.writerow([developer, commit_hash, parent_hash, tloc_diff, current_tloc, previous_tloc])

            else:
                print(f"Skipping commit {commit_hash} (no refactorings)")

    print(f"Developer effort analysis saved to {output_csv_path}")