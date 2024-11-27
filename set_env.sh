#!/bin/bash

# Prompt for AWS credentials
echo "Please enter your AWS credentials:"

# Get AWS secret access key
read -p "AWS Secret Access Key: " aws_secret_access_key

# Get AWS access key ID
read -p "AWS Access Key ID: " aws_access_key_id

# Get default region
read -p "Default region (press Enter for us-west-2): " aws_region
aws_region=${aws_region:-us-west-2}  # Set default value if empty

# Get output format
read -p "Output format (press Enter for json): " output_format
output_format=${output_format:-json}  # Set default value if empty

# Configure AWS using provided values
aws configure set aws_secret_access_key "$aws_secret_access_key"
aws configure set aws_access_key_id "$aws_access_key_id"
aws configure set default.region "$aws_region"
aws configure set default.output "$output_format"

echo "AWS credentials have been configured successfully"
