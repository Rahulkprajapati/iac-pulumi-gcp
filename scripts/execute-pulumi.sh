#!/bin/bash

# exit if a command returns a non-zero exit code and also print the commands and their args as they are executed
set -e -x


# Add the pulumi CLI to the PATH
export PATH=$PATH:$HOME/.pulumi/bin


pulumi stack select gcp-infra-dev
# The following is just a sample config setting that the hypothetical pulumi
# program needs.
# Learn more about pulumi configuration at: https://www.pulumi.com/docs/intro/concepts/config/
pulumi config set gcp:project $PROJECT_ID

pulumi up --plan=./archive/plan.json --yes