import os
import sys
import subprocess
import tempfile
import shutil
import time
from datetime import date

script_ran_independently = False

def check_executable_exists(executable):
    from shutil import which
    if which(executable) is None:
        print(f"Error: {executable} is not available. Please install it and ensure it's in your PATH.")
        sys.exit(1)

def main(args):
    if script_ran_independently and len(sys.argv) < 2:
        print("Usage: python RefactoringRunner.py <GitHub_Repo_URL>")
        sys.exit(1)

    github_repo_url = sys.argv[1] if script_ran_independently else args
    github_repo_name = github_repo_url.split('/')[-1]
    refactoringminer_path = os.path.dirname(os.path.realpath(__file__)) + '/RefactoringMiner-3.0.8/bin/RefactoringMiner'
    
    # Check if git is available
    check_executable_exists('git')
    
    # Check if java is available
    check_executable_exists('java')
    
    # Check if RefactoringMiner exists
    if not os.path.exists(refactoringminer_path):
        print(f"Error: RefactoringMiner file not found at {refactoringminer_path}")
        sys.exit(1)
    
    # Create a temporary directory to clone the repo
    temp_dir = tempfile.mkdtemp()
    print(f"Cloning repository to {temp_dir}")
    
    try:
        # Clone the repository
        subprocess.check_call(['git', 'clone', github_repo_url, temp_dir])
        
        print("Running RefactoringMiner...")
        subprocess.check_call([refactoringminer_path, '-a', temp_dir, '-json', f'RefactoringMinerOutputs/{github_repo_name}_{date.today()}.json'], shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    finally:
        # Remove the repository
        print(f"Removing repository at {temp_dir}")
        time.sleep(10)
        shutil.rmtree(temp_dir, onerror=onerror)

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

if __name__ == '__main__':
    script_ran_independently = True
    main(sys.argv[1:])