#!/bin/bash

# Usage: git-group-clone.sh -s <gitlab-server> -id <group-id> -tok <access-token>
# -s is optional, if not provided, it defaults to gitlab.telecom-paris.fr

# Check if the current directory is empty
if [ "$(ls -A .)" ]; then
    echo "Error: Current directory is not empty. Please run this script in an empty directory."
    exit 1
fi

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    # echo "Processing arguments: $1 $2"
    case "$1" in
        -s)
            GITLAB_SERVER="$2"
            shift 2
            ;;
        -id)
            GROUP_ID="$2"
            shift 2
            ;;
        -tok)
            ACCESS="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 -s <gitlab-server> -id <group-id> -tok <access-token>"
            exit 1
            ;;
    esac
done


# Set defaults if not provided
GITLAB_SERVER="${GITLAB_SERVER:-gitlab.telecom-paris.fr}"

if [[ -z "$GROUP_ID" || -z "$ACCESS" ]]; then
    echo "Usage: $0 -s <gitlab-server> -id <group-id> -tok <access-token>"
    exit 1
fi

# form command : curl --header "PRIVATE-TOKEN: <access-token>" "https://<gitlab-server>/api/v4/groups/<group-id>/projects?per_page=100" | jq -r '.[].ssh_url_to_repo'
url_list=`curl --header "PRIVATE-TOKEN: $ACCESS" "https://$GITLAB_SERVER/api/v4/groups/$GROUP_ID/projects?per_page=100" | jq -r '.[].ssh_url_to_repo'`

# print the list of URLs
echo "List of repository URLs:"
echo "$url_list"

echo "$url_list" | while read -r url; do
    echo "Cloning $url..."
    git clone "$url"
done
