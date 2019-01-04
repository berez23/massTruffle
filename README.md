# osot-scripts
Run trufflehog against targets in GitHub.

# Install

```docker build . -t truffle```

# Run

## Scan organisation repos

```docker run -v `pwd`/output:/output truffle --org ministryofjustice --pat [[YOUR-GITHUB-PAT]] --public --processes 5```

## Scan user repos

```docker run -v `pwd`/output:/output truffle --user aidan-moj --pat [[YOUR-GITHUB-PAT]] --public --processes 5```

## Scan repos of all members of an organisation

```docker run -v `pwd`/output:/output truffle --org ministryofjustice --pat [[YOUR-GITHUB-PAT]] --members --public --processes 5```

# Usage

```usage: massTruffle.py [-h] [--org ORG] --pat PAT [--user USER]
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
  --members             Scan only repos of members in an organisation.```
