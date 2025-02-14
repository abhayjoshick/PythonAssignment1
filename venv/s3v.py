import boto3

EC2_CLIENT = boto3.client('ec2')
print('My EC2:')

response = EC2_CLIENT.describe_instances()

for res in response['Reservations']:
    for ec2 in res['Instances']:
        print(ec2)
