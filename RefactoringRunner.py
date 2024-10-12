import os
import subprocess
import sys
import tempfile
import time
from datetime import date

from LoggerManager import get_logger

script_ran_independently = False

def check_executable_exists(executable, logger):
    from shutil import which
    if which(executable) is None:
        logger.error(f"Error: {executable} is not available. Please install it and ensure it's in your PATH.")
        sys.exit(1)
    else:
        logger.info(f"{executable} is available.")

def main(args, logger):
    if script_ran_independently and len(sys.argv) < 2:
        logger.info("Usage: python RefactoringRunner.py <GitHub_Repo_URL>")
        sys.exit(1)

    github_repo_url = sys.argv[1] if script_ran_independently else args
    github_repo_name = github_repo_url.split('/')[-1]
    refactoringminer_path = os.path.dirname(os.path.realpath(__file__)) + '/RefactoringMiner-3.0.8/bin/RefactoringMiner'

    logger.info(f"GitHub repo URL: {github_repo_url}")
    logger.info(f"Repo name extracted: {github_repo_name}")

    # Check if git is available
    check_executable_exists('git', logger)

    # Check if java is available
    check_executable_exists('java', logger)

    # Check if RefactoringMiner exists
    if not os.path.exists(refactoringminer_path):
        logger.error(f"RefactoringMiner file not found at {refactoringminer_path}")
        sys.exit(1)
    else:
        logger.info(f"RefactoringMiner path: {refactoringminer_path}")

    # Create a temporary directory to clone the repo
    temporary_dir = tempfile.mkdtemp()
    logger.info(f"Temporary directory created at {temporary_dir} for cloning.")

    start_time = time.time() # Start timer for cloning
    try:
        # Clone the repository
        logger.info(f"Cloning repository {github_repo_url} to {temporary_dir}...")
        subprocess.check_call(['git', 'clone', github_repo_url, temporary_dir])
        clone_duration = time.time() - start_time
        logger.info(f"Repository cloned successfully in {clone_duration:.2f} seconds.")

        # Run RefactoringMiner
        logger.info("Running RefactoringMiner...")
        json_output_file = f'RefactoringMinerOutputs/{github_repo_name}_{date.today()}.json'
        refactoringminer_start = time.time()  # Start timer for RefactoringMiner

        subprocess.check_call([refactoringminer_path, '-a', temporary_dir, '-json', json_output_file], shell=True)
        refactoringminer_duration = time.time() - refactoringminer_start
        logger.info(f"RefactoringMiner completed in {refactoringminer_duration:.2f} seconds.")
        logger.info(f"Output saved to {json_output_file}")

        # Return the paths to the cloned repo and the JSON file for later use
        return temporary_dir, json_output_file

    except subprocess.CalledProcessError as ex:
        logger.error(f"Subprocess error occurred: {ex}", exc_info=True)
        return None, None

    except Exception as exception:
        logger.error(f"An unexpected error occurred: {exception}", exc_info=True)
        return None, None

    finally:
        logger.info(f"Repository cloned to {temporary_dir} is available for further analysis.")


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
    refactoring_runner_logger = get_logger("RefactoringRunner")
    temp_dir, json_output = main(sys.argv[1:], refactoring_runner_logger)
    print(f"Cloned repository path: {temp_dir}")
    print(f"RefactoringMiner JSON output: {json_output}")