import subprocess
import os
import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    def get_secret(secret_param):
        secret_name = event.get("secret_name")
        region_name = event.get("region_name")

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        secret_string = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret_string)
        return secret_dict.get(secret_param)

    command = ["/var/task/FastTransfer"]
    
    for key, value in event.items():
        if value is not None and key not in ['secret_name','region_name']:
            if value != event.get("secret_name"):
                command.append(f"--{key.lower()}")
                command.append(str(value))
            else:
                command.append(f"--{key.lower()}")
                command.append(str(get_secret(key)))
                

    print(f"Executing command: {' '.join(command)}")

    try:
        # Exécution de la commande via subprocess
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Log des résultats
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
        print(f"Error executing command: {e.stderr}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {e.stdout}'),
        }



