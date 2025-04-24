import subprocess
import os
import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    def get_secret(secret_param,secret_arn):
        session = boto3.session.Session()
        region_name = session.region_name
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_arn
            )
        except ClientError as e:
            raise e

        secret_string = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret_string)
        clean_secret_param = secret_param.replace('source', '').replace('target', '')

        return secret_dict.get(clean_secret_param)

    command = ["/var/task/FastTransfer"]

    for key, value in event.items():
        if value is not None and not key.startswith("datasource"):
            command.append(f"--{key}")

            if isinstance(value, str) and value.startswith("ref:"):
                ref_key = value[len("ref:"):] 
                if ref_key in event:
                    command.append(str(get_secret(key,event[ref_key])))
                else:
                    print(f"Warning: Key '{ref_key}' not found in event data.")
            else:
                command.append(str(value))

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")

        return {
            'statusCode': 200,
            'body': json.dumps('Command executed successfully'),
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.CalledProcessError as e:
        # Gestion d'erreurs et log des erreurs
        print(f"Error : {e.stdout}")
        print(f"Error : {e.stderr}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error'),
            'stdout': e.stdout,
            'stderr': e.stderr
        }



