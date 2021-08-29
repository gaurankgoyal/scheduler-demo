import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


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
    try:
        ec2 = client.describe_instances()
    except ClientError as e:
        return e
    ec2_list = []
    for instance in ec2['Reservations']:
        print(instance['Instances'][0]['State']['Name'])
        if instance['Instances'][0]['State']['Name'] == 'terminated':
            pass
        else:
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


def get_rds_instance(region, aws_access_key, aws_secret_key):
    my_config = Config(
        region_name=region,
    )
    client = boto3.client(
        'rds',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=my_config,
    )
    rds = client.describe_db_instances()
    rds_list = []
    for dbinstance in rds['DBInstances']:
        if 'Endpoint' not in dbinstance:
            rds_endpoint = '-'
        else:
            rds_endpoint = dbinstance['Endpoint']['Address']
        rds_dict = {
            'rds_identifier': dbinstance['DBInstanceIdentifier'],
            'rds_state': dbinstance['DBInstanceStatus'],
            'rds_endpoint': rds_endpoint
        }
        rds_list.append(rds_dict)
    return rds_list


def stop_rds_instance(region, aws_access_key, aws_secret_key, rds_identifier):
    my_config = Config(
        region_name=region,
    )
    client = boto3.client(
        'rds',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=my_config,
    )
    try:
        client.stop_db_instance(DBInstanceIdentifier=rds_identifier)
    except ClientError as e:
        return str(e)
    return "Request to Stop RDS-{} has been trigger successfully".format(rds_identifier)


def start_rds_instance(region, aws_access_key, aws_secret_key, rds_identifier):
    my_config = Config(
        region_name=region,
    )
    client = boto3.client(
        'rds',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=my_config,
    )
    try:
        client.start_db_instance(DBInstanceIdentifier=rds_identifier)
    except ClientError as e:
        return str(e)
    return "Request to Start RDS-{} has been trigger successfully".format(rds_identifier)
