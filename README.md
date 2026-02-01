# Git-Group-Mass-Clone
A simple bash script to clone all repositories from a specified git group

## Installation

Dependencies:
- `git-group-clone.sh` script:
    - `curl`
    - `jq`
    - `git` (obviously)
- `git-group-clone-recurse.py` script:
    - `git` (obviously)
    - `python3` (obviously)
    - `python-gitlab` package 
        - Install with `pip install python-gitlab`

Now you may clone the repository wherever you want, add execute permissions to the scripts and symlink them to any directory in your `$PATH`. 

## Usage

First, you need to get a GitLab personal access token with `api_read` scope and `read_repository` scope. 

Second, you need to unlock your ssh keys for git access. 

```bash
ssh-add -t 1800 ~/.ssh/id_ed25519
```
Adjust the path and timeout as needed.

Then, you can use the scripts. You have to use the same terminal as the one where you unlocked your ssh keys.

