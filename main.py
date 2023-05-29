import boto3
import json

S3_BUCKET = 'temp-460453255610'


dms_client = boto3.client('dms')
s3_client = boto3.client('s3')


# List DMS instances
response = dms_client.describe_replication_instances()
instances = response.get('ReplicationInstances',[])
# Save instance settings as JSON file in S3 bucket
for instance in instances:
    instance_name = instance.get('ReplicationInstanceIdentifier', 'unknown')
    s3_client.put_object(Body=json.dumps(instance,indent=4, sort_keys=True, default=str), 
                        Bucket=S3_BUCKET, 
                        Key=f'dms-instances/{instance_name}.json')


# List Tasks
response = dms_client.describe_replication_tasks()
tasks = response.get('ReplicationTasks', [])
# Save task settings as JSON file in S3 bucket
for task in tasks:
    print(json.dumps(task,indent=4, sort_keys=True, default=str))
    task_name = task.get('ReplicationTaskIdentifier', 'unknown')
    s3_client.put_object(Body=json.dumps(task, indent=4, sort_keys=True, default=str), 
                        Bucket=S3_BUCKET, 
                        Key=f'dms-tasks/{task_name}.json')

