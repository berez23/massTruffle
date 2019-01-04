# massTruffle

Run trufflehog against targets in GitHub.

1. You can specify the number of trufflehog processes to run concurrently.
2. You can't specify an individual repo to scan, you must specify a user or an
   organisation.
3. If you specify a user, all repos belonging to this user which you can
   access will be scanned with trufflehog.
4. If you specify an organisation and use the ```--members``` flag, all repos
   for all members you can see of that organisation will be scanned (no repos
   belonging to the organisation will be scanned if the ```--members``` flag
   is provided).

# Install

```
git clone https://github.com/ministryofjustice/massTruffle
docker build . -t truffle
```

# Run

## Scan organisation repos

```docker run -v `pwd`/output:/output truffle --org ministryofjustice --pat [[YOUR-GITHUB-PAT]] --public --processes 5```

## Scan user repos

```docker run -v `pwd`/output:/output truffle --user aidan-moj --pat [[YOUR-GITHUB-PAT]] --public --processes 5```

## Scan repos of all members of an organisation

```docker run -v `pwd`/output:/output truffle --org ministryofjustice --pat [[YOUR-GITHUB-PAT]] --members --public --processes 5```

# Usage

```
usage: massTruffle.py [-h] [--org ORG] --pat PAT [--user USER]
                      [--processes PROCESSES]
                      [--output-directory OUTPUT_DIRECTORY] [--public]
                      [--private] [--all] [--members]

Run trufflehog against targets in GitHub.

optional arguments:
  -h, --help            show this help message and exit
  --org ORG             GitHub organisation.
  --pat PAT             GitHub PAT (Personal Access Token).
  --user USER           Scan repos of this GitHub user.
  --processes PROCESSES
                        Max Trufflehog processes at a time (default is 1).
  --output-directory OUTPUT_DIRECTORY
                        Output directory (default is /tmp).
  --public              Scan only public repos.
  --private             Scan only private repos.
  --all                 Scan all repos PAT can see.
  --members             Scan only repos of members in an organisation.
```

# Help

## What's a PAT (Personal Access Token)?

You need to be authenticated to use the GitHub API (which is what PyGithub
relies on). Get a PAT at https://github.com/settings/tokens

## Does this tool let me see private repos?

Only if you have access to them.

## Does this tool let me see members of an organisation?

Only if this information is public or you are a member of the
organisation.
