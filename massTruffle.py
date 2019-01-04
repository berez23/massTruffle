#!/usr/bin/env python3

from github import Github
from multiprocessing import Pool

import argparse
import github
import os
import sys

# Global vars ftw
glob_output_directory = "/output"

def main():
    parser = argparse.ArgumentParser(description="Run trufflehog against all " + 
                                     "repos in an organisation on GitHub.")
    parser.add_argument("--org", required=True,
                        help="GitHub organisation.")
    parser.add_argument("--pat", required=True,
                        help="GitHub PAT (Personal Access Token).")
    parser.add_argument("--processes", default=1, type=int,
                        help="Max Trufflehog processes at a time (default is 1).")
    parser.add_argument("--output-directory", default="/tmp",
                        help="Output directory (default is /tmp).")
    parser.add_argument("--public", action="store_const", const="public",
                        dest="view", help="List only public repos.")
    parser.add_argument("--private", action="store_const", const="private",
                        dest="view", help="List only private repos.")
    parser.add_argument("--all", action="store_const", const="all",
                        dest="view", help="List all repos user can see.")
    parsed = parser.parse_args()

    if not parsed.view:
        parser.error("One of --all, --public or --private required.")

    # How to map more than one argument?
    glob_output_directory = parsed.output_directory

    # Get repos from org
    get_repos(parsed)

    return 0

def run_trufflehog(repo):
    print("Processing " + repo)
    os.system("trufflehog " + repo + " > " + glob_output_directory + "/th_" + repo.split('/')[-1])

def get_repos(var):
    # Login
    g = Github(var.pat)

    # Debug
    # If you can't see private repos, check your PAT permissions
    #github.enable_console_debug_logging()

    repo_list = []

    print("Getting repo list... ", end='')

    # Append repo URLs to list
    for repo in g.get_organization(var.org).get_repos(type=var.view):
        repo_list.append(repo.html_url)

    print("Done")

    print("Running trufflehogs")

    # Run trufflehog against each URL
    with Pool(var.processes) as p:
        p.map(run_trufflehog, repo_list)

    return 0

if __name__ == "__main__":
    main()
