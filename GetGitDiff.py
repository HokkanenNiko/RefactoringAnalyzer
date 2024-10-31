import json
from pydriller import Repository
from pathlib import Path

def get_refactorings(refactoring_miner_output_file_path):
    refactoring_commits = []
    if(refactoring_miner_output_file_path == None):
        return refactoring_commits
    
    with open(refactoring_miner_output_file_path, 'r') as json_file:
        refactorings_data = json.load(json_file)
        if refactorings_data == None:
            return refactoring_commits
    
    # Iterate over the commits with refactorings
    for commit in refactorings_data['commits']:
        if commit['refactorings']:  # Only consider commits with refactorings
            commit_hash = commit['sha1']
            refactoring_commits.append(commit_hash)

    return refactoring_commits


def get_commit_diff(repo_path, output_file, refactoring_miner_output_file_path):
    # Container for the JSON output
    commit_diffs = []

    refactoring_commit_hashes = get_refactorings(refactoring_miner_output_file_path)

    # Iterate through the commits in the repository
    for commit in Repository(repo_path, only_commits=refactoring_commit_hashes).traverse_commits():
        
        # Check if the commit has a parent (meaning its not the first commit)
        if len(commit.parents) == 0:
            continue
        
        # Get the previous commit hash
        prev_commit_hash = commit.parents[0]
        
        # Collect diff stats and parsed diff content for each modified file in the commit
        diff_stats = {
            'insertions': commit.insertions,
            'deletions': commit.deletions,
            'files_modified': len(commit.modified_files)
        }
        diff_content = []

        for modified_file in commit.modified_files:
            if modified_file.diff_parsed:
                # Collecting added and removed lines
                added_lines = modified_file.diff_parsed['added']
                deleted_lines = modified_file.diff_parsed['deleted']

                # Prepare structured diff content
                diff_content.append({
                    'filename': modified_file.filename,
                    'added_lines': [{'line_number': line[0], 'content': line[1]} for line in added_lines],
                    'deleted_lines': [{'line_number': line[0], 'content': line[1]} for line in deleted_lines]
                })

        # Store commit information
        commit_info = {
            'commit_hash': commit.hash,
            'previous_commit_hash': prev_commit_hash,
            'diff_stats': diff_stats,
            'diff_content': diff_content
        }

        # Add to the list
        commit_diffs.append(commit_info)

    # Ensure that the directory exists
    p = Path(output_file)
    directory = str(p.parent)
    Path(directory).mkdir(parents=True, exist_ok=True)

    # Write the collected data to a JSON file
    with open(output_file, 'w') as f:
        json.dump(commit_diffs, f, indent=4)