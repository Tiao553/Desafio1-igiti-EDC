from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import boto3
from airflow.models import Variable

aws_access_key_id = Variable.get("aws_access_key_id")
aws_secret_access_key = Variable.get("aws_secret_access_key")

client = boto3.client("emr", region_name="us-east-2",
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

s3client = boto3.client("s3", aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)

sageclient = boto3.client('sagemaker', region_name='us-east-2',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
sagemaker_role = 'arn:aws:iam::531477333755:role/teste_sage_maker'

# Usando a novíssima Taskflow API
default_args = {
    'owner': 'Sebastiao Ferreira',
    "depends_on_past": False,
    "start_date": days_ago(2),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False
}

@dag(default_args=default_args, schedule_interval=None, catchup=False, tags=["emr", "aws", "censo"], description="Pipeline para processamento de dados do CENSO escolar")
def pipeline_enem():
    """
    Pipeline para processamento de dados do CENSO escolar.
    """
    @task
    #running docker image and start processing data in sagemaker
    def start_job_sagemaker():
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

    @task
    def run_emr():
        cluster_id = client.run_job_flow(
                    Name='EMR-processing-censu-challenger-mod1',
                    ServiceRole='EMR_DefaultRole',
                    JobFlowRole='EMR_EC2_DefaultRole',
                    VisibleToAllUsers=True,
                    LogUri='s3://processing-zone-531477333755/emr-logs',
                    ReleaseLabel='emr-6.3.0',
                    Instances={
                        'InstanceGroups': [
                            {
                                'Name': 'Master nodes',
                                'Market': 'SPOT',
                                'InstanceRole': 'MASTER',
                                'InstanceType': 'm5.micro',
                                'InstanceCount': 1,
                            },
                            {
                                'Name': 'Worker nodes',
                                'Market': 'SPOT',
                                'InstanceRole': 'CORE',
                                'InstanceType': 'm5.micro',
                                'InstanceCount': 3,
                            }
                        ],
                        'Ec2KeyName': 'sebastiao-igti-teste', #keypair EC2
                        'KeepJobFlowAliveWhenNoSteps': True,
                        'TerminationProtected': False,
                        'Ec2SubnetId': 'subnet-1df20360' #SubnetEC2
                    },

                    Applications=[
                        {'Name': 'Spark'},
                        {'Name': 'Hive'},
                        {'Name': 'Pig'},
                        {'Name': 'Hue'},
                        {'Name': 'JupyterHub'},
                        {'Name': 'JupyterEnterpriseGateway'},
                        {'Name': 'Livy'},
                    ],

                    Configurations=[{
                        "Classification": "spark-env",
                        "Properties": {},
                        "Configurations": [{
                            "Classification": "export",
                            "Properties": {
                                "PYSPARK_PYTHON": "/usr/bin/python3",
                                "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3"
                            }
                        }]
                    },
                        {
                            "Classification": "spark-hive-site",
                            "Properties": {
                                "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
                            }
                        },
                        {
                            "Classification": "spark-defaults",
                            "Properties": {
                                "spark.submit.deployMode": "cluster",
                                "spark.speculation": "false",
                                "spark.sql.adaptive.enabled": "true",
                                "spark.serializer": "org.apache.spark.serializer.KryoSerializer"
                            }
                        },
                        {
                            "Classification": "spark",
                            "Properties": {
                                "maximizeResourceAllocation": "true"
                            }
                        }
                    ],
                    
                    StepConcurrencyLevel=1,
                    
                    Steps=[{
                        'Name': 'Trnasformando em parquet e particionando os dados',
                        'ActionOnFailure': 'CONTINUE',
                        'HadoopJarStep': {
                            'Jar': 'command-runner.jar',
                            'Args': ['spark-submit',
                                    '--master', 'yarn',
                                    '--deploy-mode', 'cluster',
                                    's3://processing-zone-531477333755/emr-code/pyspark/job_census.py'
                                    ]
                        }
                    }],
                )
        
        return {
            'statusCode': 200,
            'body': f"Started job flow {cluster_id['JobFlowId']}"
        }


    @task
    def wait_emr_step(cid: str):
        waiter = client.get_waiter('step_complete')
        steps = client.list_steps(
            ClusterId=cid
        )
        stepId = steps['Steps'][0]['Id']

        waiter.wait(
            ClusterId=cid,
            StepId=stepId,
            WaiterConfig={
                'Delay': 30,
                'MaxAttempts': 120
            }
        )
        return True


    @task
    def terminate_emr_cluster(success_before: str, cid: str):
        if success_before:
            res = client.terminate_job_flows(
                JobFlowIds=[cid]
            )


    # Encadeando a pipeline
    start = start_job_sagemaker()
    cluid = run_emr()
    res_emr = wait_emr_step(cluid)
    res_ter = terminate_emr_cluster(res_emr, cluid)


execucao = pipeline_enem()