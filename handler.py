import subprocess
import os
import json

def lambda_handler(event, context):

    command = [
        "/var/task/FastTransfer",
        "--sourceconnectiontype", event.get("sourceconnectiontype", "mssql"),
        "--sourceserver", event.get("sourceserver"),
        "--sourceuser", event.get("sourceuser"),
        "--sourcepassword", event.get("sourcepassword"),
        "--sourcedatabase", event.get("sourcedatabase"),
        "--sourceschema", event.get("sourceschema"),
        "--sourcetable", event.get("sourcetable"),
        "--targetconnectiontype", event.get("targetconnectiontype", "pgsql"),
        "--targetserver", event.get("targetserver"),
        "--targetuser", event.get("targetuser"),
        "--targetpassword", event.get("targetpassword"),
        "--targetdatabase", event.get("targetdatabase"),
        "--targetschema", event.get("targetschema"),
        "--targettable", event.get("targettable"),
        "--method", event.get("method", "None"),
        "--loadmode", event.get("loadmode", "Truncate"),
        "--batchsize", event.get("batchsize", "1048576"),
        "--settingsfile", event.get("settingsfile", "/var/task/FastTransfer_Settings.json")
    ]

    print(f"Executing command: {' '.join(command)}")

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
        print(f"Error executing command: {e.stderr}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {e.stderr}'),
        }



