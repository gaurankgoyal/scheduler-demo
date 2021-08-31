import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from .models import AWS, CronJob


def get_ec2_instance(region, aws_access_key, aws_secret_key, aws):
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
        if CronJob.objects.all().filter(account=aws, instance_id=instance['Instances'][0]['InstanceId']).exists():
            cronjob = CronJob.objects.all().filter(account=aws, instance_id=instance['Instances'][0]['InstanceId']).first()
            start_cron = cronjob.start_cronjob
            stop_cron = cronjob.stop_cronjob
        else:
            start_cron = 'NA'
            stop_cron = 'NA'
        if instance['Instances'][0]['State']['Name'] == 'terminated':
            pass
        else:
            ec2_dict = {
                'instance_id': instance['Instances'][0]['InstanceId'],
                'instance_state': instance['Instances'][0]['State']['Name'],
                'instance_ip': instance['Instances'][0]['PrivateIpAddress'],
                'start_cron': start_cron,
                'stop_cron': stop_cron
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


def get_rds_instance(region, aws_access_key, aws_secret_key, aws):
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


def create_start_cron_job(region, aws_access_key, aws_secret_key, instance_id, start_cron, user):
    my_config = Config(
        region_name=region,
    )
    client = boto3.client(
        'events',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=my_config,
    )
    cron_name = instance_id + "_" + user + "_start"
    input_string = '{"instance_id": "' + instance_id+'","action":"start"}'
    try:
        # Put an event rule
        response = client.put_rule(
            Name=cron_name,
            ScheduleExpression=start_cron,
            State='ENABLED'
        )
        response = client.put_targets(
            Rule=cron_name,
            Targets=[
                {
                    'Arn': 'arn:aws:lambda:eu-central-1:408446414824:function:start-stop-lambda',
                    'Id': cron_name,
                    'Input': input_string,
                }
            ]
        )

    except ClientError as e:
        print(e)
        return str(e)
    return "Cron Job has been configured for instance - {}".format(instance_id)


def create_stop_cron_job(region, aws_access_key, aws_secret_key, instance_id, stop_cron, user):
    my_config = Config(
        region_name=region,
    )
    client = boto3.client(
        'events',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=my_config,
    )
    cron_name = instance_id + "_" + user + "_stop"
    input_string = '{"instance_id": "' + instance_id+'","action":"start"}'
    try:
        # Put an event rule
        response = client.put_rule(
            Name=cron_name,
            ScheduleExpression=stop_cron,
            State='ENABLED'
        )
        response = client.put_targets(
            Rule=cron_name,
            Targets=[
                {
                    'Arn': 'arn:aws:lambda:eu-central-1:408446414824:function:start-stop-lambda',
                    'Id': cron_name,
                    'Input': input_string,
                }
            ]
        )

    except ClientError as e:
        print(e)
        return str(e)
    return "Cron Job has been configured for instance - {}".format(instance_id)


def aws_delete_schedule(region, aws_access_key, aws_secret_key, aws_start_cron):
    print("inside delete")
    my_config = Config(
        region_name=region,
    )
    client = boto3.client(
        'events',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=my_config,
    )

    try:
        client.remove_targets(Rule=aws_start_cron, Ids=[aws_start_cron])
        client.delete_rule(Name=aws_start_cron)
        client.remove_targets(Rule=aws_start_cron.replace("start", "stop"), Ids=[aws_start_cron.replace("start", "stop")])
        client.delete_rule(Name=aws_start_cron.replace("start", "stop"))
        return True
    except ClientError as e:
        print(e)
        return str(e)
