#!/usr/bin/env python3

from github import Github
from multiprocessing import Pool

import argparse
import github
import os
import sys

# Ignore this def and the global, all is good from main()
def in_docker():
    """ Returns: True if running in a Docker container, else False """
    with open('/proc/1/cgroup', 'rt') as ifh:
        return 'docker' in ifh.read()

# Global vars ftw
glob_output_directory = "/tmp"
if in_docker():
    glob_output_directory = "/output"

def main():
    parser = argparse.ArgumentParser(description="Run trufflehog against " + 
                                                 "targets in GitHub.")
    parser.add_argument("--org",
                        help="GitHub organisation.")
    parser.add_argument("--pat", required=True,
                        help="GitHub PAT (Personal Access Token).")
    parser.add_argument("--user",
                        help="Scan repos of this GitHub user.")
    parser.add_argument("--processes", default=1, type=int,
                        help="Max Trufflehog processes at a time (default is 1).")
    parser.add_argument("--output-directory", default="/tmp",
                        help="Output directory (default is /tmp).")
    parser.add_argument("--public", action="store_const", const="public",
                        dest="view", help="Scan only public repos.")
    parser.add_argument("--private", action="store_const", const="private",
                        dest="view", help="Scan only private repos.")
    parser.add_argument("--all", action="store_const", const="all",
                        dest="view", help="Scan all repos PAT can see.")
    parser.add_argument("--members", action="store_true",
                        dest="members", help="Scan only repos of members in an organisation.")

    parsed = parser.parse_args()

    # We can't scan a user on GitHub and the members of this user
    if parsed.user and parsed.members:
        parser.erorr("Incompatible options --user <USER> and --members.")

    # Make sure user specifies a user or organisation
    if not parsed.org and not parsed.user:
        parser.error("One of --org or --user required.")

    # Make sure user specifies an appropriate 'view'
    if not parsed.view:
        parser.error("One of --all, --public or --private required.")

    # How to map more than one argument?
    glob_output_directory = parsed.output_directory

    # Org specified and not members of this org
    if parsed.org and not parsed.members:
        # Get repos from org
        get_org_repos(parsed)

    # GH user repos asked for
    if parsed.user:
        get_user_repos(parsed)

    # Get members of org (repos of each member to be scanned)
    if parsed.org and parsed.members:
        get_org_members(parsed)

    return 0

def run_trufflehog(repo):
    print("Processing " + repo)
    os.system("trufflehog --cleanup " + repo + " > " + glob_output_directory + "/mh_" + repo.split('/')[-2] + "_" + repo.split('/')[-1])

def get_org_members(var):
    # Login
    g = Github(var.pat)

    # Debug
    # If you can't see private repos, check your PAT permissions
    #github.enable_console_debug_logging()

    member_list = []
    repo_list = []

    print("Getting member list... ", end='', flush=True)

    # Append repo URLs to list
    for member in g.get_organization(var.org).get_members():
        member_list.append(member.login)

    print("Done")

    # Get repos for each member in org
    for member in member_list:
        print(member)
        for repo in g.get_user(member).get_repos(type=var.view):
            repo_list.append(repo.html_url)

    # Run trufflehog against each URL
    with Pool(var.processes) as p:
        p.map(run_trufflehog, repo_list)

    return 0

def get_user_repos(var):
    # Login
    g = Github(var.pat)

    # Debug
    # If you can't see private repos, check your PAT permissions
    #github.enable_console_debug_logging()

    repo_list = []

    print("Getting repo list... ", end='', flush=True)

    # Append repo URLs to list
    for repo in g.get_user(var.user).get_repos(type=var.view):
        repo_list.append(repo.html_url)

    print("Done")

    print("Running trufflehogs")

    # Run trufflehog against each URL
    with Pool(var.processes) as p:
        p.map(run_trufflehog, repo_list)

    return 0

def get_org_repos(var):
    # Login
    g = Github(var.pat)

    # Debug
    # If you can't see private repos, check your PAT permissions
    #github.enable_console_debug_logging()

    repo_list = []

    print("Getting repo list... ", end='', flush=True)

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
