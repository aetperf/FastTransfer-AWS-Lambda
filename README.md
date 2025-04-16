# FastTransfer-AWS-Lambda

This project demonstrates how to package and deploy the `FastTransfer` binary inside an AWS Lambda function using a custom Docker image.  
The goal is to automate and scale the execution of the `FastTransfer` tool in a serverless environment.  

By containerizing the binary and its configuration, we can take full advantage of Lambda's flexibility while keeping deployment simple and reproducible.

The `FastTransfer` binary is a compiled application designed to move data between different types of databases.  
This guide walks through the steps needed to build a Docker image containing the executable, upload it to Amazon ECR, and deploy it as a Lambda function using the AWS CLI.

---

## 🧾 Project Structure

Make sure you have the following files in your project directory:

- **FastTransfer**: The compiled binary of `FastTransfer` ([documentation](https://aetperf.github.io/FastTransfer-Documentation/))
- **FastTransfer_Settings.json**: Optional configuration file used by `FastTransfer`
- **handler.py**: Python script that controls the binary execution from within the Lambda
- **Dockerfile**: Builds a container image for the Lambda
- **event.json**: JSON file used to invoke the Lambda and pass dynamic parameters (see below)

---

## ⚙️ 1. Create and build the Docker Image
Create a file named `Dockerfile` and add the following content:
```dockerfile
FROM public.ecr.aws/lambda/python:3.12

# Install libicu using dnf (package manager for Amazon Linux 2)
RUN dnf install -y icu libicu

# Set necessary environment variables
ENV HOME=/tmp
ENV DOTNET_BUNDLE_EXTRACT_BASE_DIR=/tmp

# Copy necessary files into the container
COPY FastTransfer /var/task/FastTransfer
COPY FastTransfer_Settings.json /var/task/FastTransfer_Settings.json
COPY handler.py /var/task/handler.py

# Set proper permissions for the binary
RUN chmod +x /var/task/FastTransfer

# Lambda command
CMD ["handler.lambda_handler"]
```

build the Docker Image
```bash
docker build -t fasttransfer-lambda-image .
```

## 🚀 2. Push the Docker Image to Amazon ECR
### 1. Create an ECR repository (if needed):
```bash
aws ecr create-repository --repository-name fasttransfer-lambda-repo
```

### 2. Authenticate Docker with ECR:
```bash
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.eu-west-1.amazonaws.com
```

### 3. Tag your image:
```bash
docker tag fasttransfer-lambda-image:latest <aws_account_id>.dkr.ecr.eu-west-1.amazonaws.com/fasttransfer-lambda-repo:latest
```

### 4. Push it to ECR:
```bash
docker push <aws_account_id>.dkr.ecr.eu-west-1.amazonaws.com/fasttransfer-lambda-repo:latest
```

## 🛠 3. Create the Lambda Function (one time)
```bash
aws lambda create-function \
  --function-name FastTransferLambda \
  --package-type Image \
  --code ImageUri=<aws_account_id>.dkr.ecr.eu-west-1.amazonaws.com/fasttransfer-lambda-repo:latest \
  --role arn:aws:iam::<aws_account_id>:role/<lambda_execution_role> \
  --timeout 120 \
  --memory-size 5000
```

## 📦 4. Prepare event.json (Input Parameters)
Create a file named `event.json` locally with the parameters to control `FastTransfer`:
```json
{
    "sourceconnectiontype": "mssql",
    "sourceserver": "database-mssql.xxxxxxx.eu-west-1.rds.amazonaws.com",
    "sourceuser": "xxxxxxx",
    "sourcepassword": "xxxxxx",
    "sourcedatabase": "WIKIPEDIA",
    "sourceschema": "dbo",
    "sourcetable": "dbpedia_14_10K",
    "targetconnectiontype": "pgsql",
    "targetserver": "database-postgres.xxxxxx.eu-west-1.rds.amazonaws.com",
    "targetuser": "xxxxxxx",
    "targetpassword": "xxxxxx",
    "targetdatabase": "postgres",
    "targetschema": "public",
    "targettable": "dbpediamini",
    "method": "None",
    "loadmode": "Truncate",
    "batchsize": "1048576",
    "settingsfile": "/var/task/FastTransfer_Settings.json"
  }
```

## ⚡️ 5. Invoke the Lambda Function via CLI (from your machine)
Once the function is deployed, you can invoke it from your local terminal using the `event.json` file:
```bash
aws lambda invoke \
  --function-name FastTransferLambda \
  --payload fileb://event.json \
  output.json
```

This will:
- Send the parameters to the Lambda
- Run the binary with those values
- Store the result in output.json

To see the result directly in the console:
```bash
aws lambda invoke \
  --function-name FastTransferLambda \
  --payload fileb://event.json \
  --cli-binary-format raw-in-base64-out \
  /dev/stdout
```

## 🧼 Notes
- Make sure your IAM role allows access to RDS and CloudWatch Logs.
- Logs can be viewed via CloudWatch after invocation.
- Sensitive data such as passwords should ideally be encrypted or passed via AWS Secrets Manager for production usage.

## 📄 License
```csharp
Copyright (c) 2025 by Pierre-Antoine Collet  
Licensed under MIT License - https://opensource.org/licenses/MIT
```

## Contact
For more information or if you have any questions, feel free to contact the author, Pierre-Antoine Collet.

