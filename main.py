import boto3
import json
import os


def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    s3 = boto3.resource('s3')
    tag = os.getenv("tag")
    region = os.getenv("region")
    ec2_resource = boto3.resource('ec2', region_name=region)

    file_name = 'disks-size-average.json'
    bucket_name = os.getenv("bucket")

    volume_id = []
    volume_size = []
    volume_state = []

    s3object = s3.Object(bucket_name, file_name)

    for volume in ec2_resource.volumes.filter(
            Filters=[
                {
                    'Name': 'tag:usecase',
                    'Values': [
                        tag
                    ]
                },
                {
                    'Name': 'encrypted',
                    'Values': [
                        'false'
                    ]
                }
            ]

    ):
        volume_id.append(volume.id)
        volume_size.append(volume.size)
        print(f'Volume {volume.id} ({volume.size} GiB) -> {volume.state}')

    data = {
        volume_id[0]: volume_size[0],
        volume_id[1]: volume_size[1],
        volume_id[2]: volume_size[2]
    }

    s3object.put(
        Body=(bytes(json.dumps(data).encode('UTF-8')))
    )

    print(data)
