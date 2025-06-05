#!/usr/bin/env python3

import gitlab
import os
import subprocess
import argparse

# Usage: git-group-clone.sh -s <gitlab-server> -id <group-id> -tok <access-token> -dest <destination-directory>
# -s is optional, if not provided, it defaults to gitlab.telecom-paris.fr

"""
This script clones all GitLab projects within a specified group and its subgroups recursively.
"""

# Parse command line arguments
parser = argparse.ArgumentParser(description='Clone all GitLab projects in a group and its subgroups.')
parser.add_argument('-s', '--server', type=str, default='gitlab.telecom-paris.fr',
                    help='GitLab server URL (default: gitlab.telecom-paris.fr)')
parser.add_argument('-id', '--group-id', type=int, required=True,
                    help='ID number of the GitLab group to clone projects from')
parser.add_argument('-tok', '--token', type=str, required=True,
                    help='GitLab private access token for authentication')
parser.add_argument('-dest', '--destination', type=str, default='cloned_projects',
                    help='Base directory to clone projects into (default: cloned_projects)')
args = parser.parse_args()


# Configuration
GITLAB_URL      = f"https://{args.server}"
PRIVATE_TOKEN   = args.token
ROOT_GROUP_PATH = args.group_id  # This should be the ID of the group to start cloning from
CLONE_BASE_DIR  = args.destination

# Check if the destination directory exists
if not os.path.exists(CLONE_BASE_DIR):
    os.makedirs(CLONE_BASE_DIR)

# GitLab connection
gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)

def clone_project(project, base_dir):
    repo_url       = project.ssh_url_to_repo  # or project.http_url_to_repo
    namespace_path = project.path_with_namespace  # e.g., company/dev-team/my-project
    local_path     = os.path.join(base_dir, namespace_path)

    if os.path.exists(local_path):
        print(f"Already cloned: {local_path}")
        # Get into the directory and pull latest changes
        os.chdir(local_path)
        subprocess.run(["git", "pull", "--recurse-submodules"])
        print(f"Updated {local_path} with latest changes.")
        return

    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    print(f"Cloning {repo_url} into {local_path}")
    subprocess.run(["git", "clone", "--recurse-submodules", repo_url, local_path])

def process_group(group, base_dir):
    # Clone all projects in the group
    projects = group.projects.list(include_subgroups=False, all=True)
    for project in projects:
        full_project = gl.projects.get(project.id)
        clone_project(full_project, base_dir)

    # Recurse into subgroups
    subgroups = group.subgroups.list(all=True)
    for subgroup in subgroups:
        full_subgroup = gl.groups.get(subgroup.id)
        process_group(full_subgroup, base_dir)

# Start process
root_group = gl.groups.get(ROOT_GROUP_PATH)
process_group(root_group, CLONE_BASE_DIR)
