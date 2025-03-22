#!/usr/bin/env python3

"""
Script to push WeyFusion to GitHub
This handles authentication and pushes the entire project
"""

import os
import subprocess
import getpass
import argparse
import shutil

def run_command(cmd, show_output=True):
    """Run a shell command and optionally display output"""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        universal_newlines=True
    )
    
    output = []
    for line in process.stdout:
        if show_output:
            print(line, end='')
        output.append(line)
    
    returncode = process.wait()
    return returncode, '\n'.join(output)

def copy_colab_notebook(source_path, destination_path="weyfusion/"):
    """Copy the Colab notebook to the repository"""
    if os.path.exists(source_path):
        target_path = os.path.join(destination_path, os.path.basename(source_path))
        print(f"Copying {source_path} to {target_path}")
        shutil.copy2(source_path, target_path)
        return True
    else:
        print(f"Error: Could not find {source_path}")
        return False

def push_to_github(github_username, github_token, repository="weyfusion", branch="main"):
    """Push the WeyFusion repository to GitHub"""
    # Ensure we're in the right directory
    if not os.path.exists("weyfusion"):
        print("Error: weyfusion directory not found")
        return False
    
    os.chdir("weyfusion")
    
    # Configure git
    print("\n🔧 Configuring Git...")
    run_command(f'git config --global user.email "user@example.com"')
    run_command(f'git config --global user.name "{github_username}"')
    
    # Add remote with authentication embedded in URL
    remote_url = f"https://{github_username}:{github_token}@github.com/{github_username}/{repository}.git"
    print("\n🔄 Setting GitHub remote...")
    run_command(f'git remote set-url origin {remote_url}', show_output=False)  # Hide output to avoid token exposure
    
    # Check if the remote is properly set
    _, output = run_command('git remote -v', show_output=False)
    if github_username not in output and "github.com" not in output:
        print("Error: Failed to set Git remote correctly")
        return False
    else:
        print("✅ GitHub remote set successfully")
    
    # Add changes
    print("\n➕ Adding changes to Git...")
    run_command('git add .')
    
    # Commit changes
    print("\n📝 Committing changes...")
    run_command('git commit -m "Add Google Colab notebook and URL encryption"')
    
    # Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    returncode, _ = run_command(f'git push origin {branch}')
    
    if returncode == 0:
        print("\n✅ Changes pushed to GitHub successfully!")
        print(f"Your repository is available at: https://github.com/{github_username}/{repository}")
        return True
    else:
        print("\n❌ Failed to push to GitHub. Please check your credentials and try again.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Push WeyFusion to GitHub")
    parser.add_argument("--username", help="GitHub username")
    parser.add_argument("--notebook", default="WeyFusion_Colab.ipynb", help="Path to Colab notebook")
    args = parser.parse_args()
    
    # Copy the Colab notebook
    copy_colab_notebook(args.notebook)
    
    # Get GitHub credentials
    github_username = args.username or input("Enter your GitHub username: ")
    github_token = getpass.getpass("Enter your GitHub personal access token: ")
    
    # Push to GitHub
    push_to_github(github_username, github_token) 