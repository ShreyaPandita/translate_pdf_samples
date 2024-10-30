import boto3
import os
import uuid
import time

def upload_to_s3(bucket_name, file_path, s3_key):
    """
    Upload a file to an S3 bucket.
    
    Args:
        bucket_name (str): Name of the S3 bucket
        file_path (str): Local path of the file to upload
        s3_key (str): Destination path in S3 bucket
    
    Returns:
        str: S3 URI of the uploaded file
    """
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, s3_key)
    return f"s3://{bucket_name}/{s3_key}"

def start_translation_job(input_s3_uri, output_s3_uri, job_name, source_lang, target_lang, data_access_role_arn):   
    """
    Start an AWS Translate batch translation job for documents.
    
    Args:
        input_s3_uri (str): S3 URI for input documents
        output_s3_uri (str): S3 URI for translated output
        job_name (str): Unique name for the translation job
        source_lang (str): Source language code
        target_lang (str): Target language code
        data_access_role_arn (str): IAM role ARN for S3 access
    
    Returns:
        str: Job ID of the started translation job
    """    
    translate = boto3.client('translate')
    response = translate.start_text_translation_job(
        JobName=job_name,
        InputDataConfig={
            'S3Uri': input_s3_uri,
            'ContentType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        },
        OutputDataConfig={
            'S3Uri': output_s3_uri
        },
        DataAccessRoleArn=data_access_role_arn,
        SourceLanguageCode=source_lang,
        TargetLanguageCodes=[target_lang]
    )
    return response['JobId']

def check_job_status(job_id):
    """
    Poll the status of a translation job until completion.
    
    Args:
        job_id (str): ID of the translation job to monitor
    
    Returns:
        str: Final status of the job (COMPLETED, COMPLETED_WITH_ERROR, FAILED, or STOPPED)
    """
    translate = boto3.client('translate')
    while True:
        response = translate.describe_text_translation_job(JobId=job_id)
        status = response['TextTranslationJobProperties']['JobStatus']
        if status in ['COMPLETED', 'COMPLETED_WITH_ERROR', 'FAILED', 'STOPPED']:
            return status
        time.sleep(60)  # Wait for 60 seconds before checking again

def download_from_s3(bucket_name, s3_key, local_path):
    """
    Download a file from an S3 bucket.
    
    Args:
        bucket_name (str): Name of the S3 bucket
        s3_key (str): Path of the file in S3 bucket
        local_path (str): Local path where file should be saved
    """
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, s3_key, local_path)

def main():
    """
    Main function to orchestrate the document translation workflow:
    1. Upload document to S3
    2. Start translation job
    3. Monitor job status
    4. Download translated document
    """
    # Configuration (update this with your values)
    input_file = "input1.docx"
    bucket_name = "vsp-translate"
    source_lang = "en"
    target_lang = "es"
    data_access_role_arn = "arn:aws:iam::767397978963:role/service-role/AmazonTranslateServiceRoleS3FullAccess-testrole"

    # Generate unique identifiers
    job_name = f"translate-job-{uuid.uuid4()}"
    print(job_name)
    s3_input_key = f"input/{os.path.basename(input_file)}"
    print(s3_input_key)
    s3_output_prefix = f"output/{job_name}/"
    print(s3_output_prefix)
    input_s3_uri = f"s3://{bucket_name}/input/"
    print(input_s3_uri)
    output_s3_uri = f"s3://{bucket_name}/{s3_output_prefix}"
    print(output_s3_uri)

    # Upload the input file to S3
    upload_to_s3(bucket_name, input_file, s3_input_key)
 
    # Start the translation job
    job_id = start_translation_job(input_s3_uri, output_s3_uri, job_name, source_lang, target_lang, data_access_role_arn)

    print(f"Translation job started. Job ID: {job_id}")
    print(f"Input S3 URI: {input_s3_uri}")
    print(f"Output S3 URI: {output_s3_uri}")

    # Wait for job completion
    job_status = check_job_status(job_id)
    print(f"Job completed with status: {job_status}")

    if job_status == 'COMPLETED':
        output_key = f"{s3_output_prefix}{os.path.basename(input_file)}.es"
        download_from_s3(bucket_name, output_key, "translated_document.docx")
        print("Translated document downloaded as 'translated_document.docx'")

if __name__ == "__main__":
    main()
