#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <s3_bucket_name>"
  exit 1
fi

S3_BUCKET=$1
SOURCE_DIR="build"

# Check if AWS CLI is installed
command -v aws >/dev/null 2>&1 || {
  echo >&2 "AWS CLI is required but not installed. Aborting."
  exit 1
}

npm run build

# Sync files to S3 bucket
aws s3 sync "$SOURCE_DIR" "s3://$S3_BUCKET"
