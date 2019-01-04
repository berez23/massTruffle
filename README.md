# osot-scripts
Run trufflehog against all repos in a GitHub organisation.

# Install

```docker build . -t truffle```

# Run

## Scan organisation repos

```docker run -v `pwd`/output:/output truffle --org ministryofjustice --pat [[YOUR-GITHUB-PAT]] --public --processes 5```

## Scan user repos

```docker run -v `pwd`/output:/output truffle --user aidan-moj --pat [[YOUR-GITHUB-PAT]] --public --processes 5```

## Scan repos of all members of an organisation

```docker run -v `pwd`/output:/output truffle --org ministryofjustice --pat [[YOUR-GITHUB-PAT]] --members --public --processes 5```
