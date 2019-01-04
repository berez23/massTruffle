# osot-scripts
Run trufflehog against all repos in a GitHub organisation.

# Install

```docker build . -t truffle```

# Run

```docker run -v `pwd`/output:/output truffle --org ministryofjustice --pat [[YOUR-GITHUB-PAT]] --public```
