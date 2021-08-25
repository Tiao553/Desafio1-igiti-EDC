import boto3
from datetime import datetime

sageclient = boto3.client('sagemaker', region_name='us-east-2')
sagemaker_role = 'arn:aws:iam::531477333755:role/teste_sage_maker'

def handler(event, context):
    process_job_arn = sageclient.create_processing_job(
        ProcessingJobName = f"censoescolar-extraction-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}",
        ProcessingOutputConfig={
            'Outputs': [
                {
                    "OutputName": "censo",
                    "S3Output": {
                        "S3Uri" : 's3://landing-zone-531477333755/censo',
                        "LocalPath" : '/opt/ml/processing/output/censo',
                        "S3UploadMode" : 'endjob'
                    }
                }
            ]
        },
        ProcessingResources={
            "ClusterConfig": {
                'InstanceCount': 1,
                'InstanceType': 'ml.m5.xlarge',
                'VolumeSizeInGB': 50,
            }
        },
        AppSpecification={
            'ImageUri': '531477333755.dkr.ecr.us-east-2.amazonaws.com/Sebastiao-igti-prod-censo-escolar-extration-job'
        },
        RoleArn = sagemaker_role
    )