import os
import subprocess
import sys
import tempfile
import time

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
        logger.info("Usage: python <GitHub_Repo_URL>")
        sys.exit(1)

    github_repo_url = sys.argv[1] if script_ran_independently else args
    github_repo_name = github_repo_url.split('/')[-1]

    logger.info(f"GitHub repo URL: {github_repo_url}")
    logger.info(f"Repo name extracted: {github_repo_name}")

    # Check if git is available
    check_executable_exists('git', logger)

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

        # Return the paths to the cloned repo and the JSON file for later use
        return temporary_dir

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
    temp_dir = main(sys.argv[1:])
    print(f"Cloned repository path: {temp_dir}")