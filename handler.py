import subprocess
import os
import json

def lambda_handler(event, context):
    # Définir les paramètres de la commande à exécuter
    command = [
        "/var/task/FastTransfer",
        "--sourceconnectiontype", "mssql",
        "--sourceserver", "database-mssql.xxxxxxxx.eu-west-1.rds.amazonaws.com",
        "--sourceuser", "xxxxxxxx",
        "--sourcepassword", "xxxxxxxxx",
        "--sourcedatabase", "WIKIPEDIA",
        "--sourceschema", "dbo",
        "--sourcetable", "dbpedia_14_10K",
        "--targetconnectiontype", "pgsql",
        "--targetserver", "database-postgres.xxxxxxxxx.eu-west-1.rds.amazonaws.com",
        "--targetuser", "xxxxxxxx",
        "--targetpassword", "xxxxxxxxx",
        "--targetdatabase", "postgres",
        "--targetschema", "public",
        "--targettable", "dbpediamini",
        "--method", "None",
        "--loadmode", "Truncate",
        "--batchsize", "1048576",
        "--settingsfile", "/var/task/FastTransfer_Settings.json"
    ]

   # Log de la commande avant exécution
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
            'body': json.dumps(f'Error: {e.stderr}'),
        }



