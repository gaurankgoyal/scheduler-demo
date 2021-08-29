import boto3
from botocore.config import Config


def get_ec2_instance(region, aws_access_key, aws_secret_key):
    my_config = Config(
        region_name=region,
    )
    client = boto3.client(
        'ec2',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=my_config,
    )
    ec2 = client.describe_instances()
    ec2_details = {}
    ec2_list = []
    for instance in ec2['Reservations']:
        ec2_dict = {
            'instance_id': instance['Instances'][0]['InstanceId'],
            'instance_state': instance['Instances'][0]['State']['Name'],
            'instance_ip': instance['Instances'][0]['PrivateIpAddress']
        }
        ec2_list.append(ec2_dict)
    return ec2_list


def start_instance(region, aws_access_key, aws_secret_key, instance_id):
    my_config = Config(
        region_name=region,
    )
    client = boto3.client(
        'ec2',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=my_config,
    )
    response = client.start_instances(InstanceIds=[
        instance_id,
    ]
    )
    return True


def stop_instance(region, aws_access_key, aws_secret_key, instance_id):
    my_config = Config(
        region_name=region,
    )
    client = boto3.client(
        'ec2',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=my_config,
    )
    response = client.stop_instances(InstanceIds=[
        instance_id,
    ]
    )
    return True
