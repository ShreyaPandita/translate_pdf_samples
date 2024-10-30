# AWS Batch Document Translation

A Python script that automates document translation using AWS Translate batch processing. This tool handles the complete workflow of uploading documents to S3, initiating translation jobs, and retrieving translated documents.

## Features

- Supports batch translation of DOCX documents
- Automatically handles S3 file management
- Monitors translation job status
- Generates unique job identifiers for each translation
- Downloads translated documents automatically upon completion

## Prerequisites

- Python 3.x
- AWS account with appropriate permissions
- Required Python packages:
  - boto3
- AWS credentials configured
- S3 bucket with appropriate permissions
- IAM role with necessary permissions for AWS Translate

## Installation

1. Clone the repository
2. Install required packages:
```bash
pip install boto3
```

## AWS Configuration Requirements

1. S3 Bucket Setup:

Create an S3 bucket for storing documents

Ensure bucket has appropriate read/write permissions

2. IAM Role Requirements: The IAM role needs the following permissions:

s3:GetObject for source bucket

s3:PutObject for destination bucket

translate:StartTextTranslationJob

translate:DescribeTextTranslationJob

## Usage

1. Configure the script parameters in the main function:

```bash
input_file = "input1.docx"              # Your input document
bucket_name = "XXXXXXXXXXXXXXXX"        # Your S3 bucket
source_lang = "en"                      # Source language code
target_lang = "es"                      # Target language code
data_access_role_arn = "your-role-arn" # Your IAM role ARN
```

2. Run the script
```bash
python batch_translation.py
```
