# FastTransfer-AWS-Lambda

# Steps to Deploy the Application

## 1. Prepare the Code and Necessary Files
Make sure you have the following files in your project:

- **FastTransfer**: The compiled binary of `FastTransfer` link to the page [FastTransfer documentation](https://aetperf.github.io/FastTransfer-Documentation/).
- **FastTransfer_Settings.json**: The JSON configuration file for the application.
- **handler.py**: The Python script that serves as the entry point for AWS Lambda. You need to modify the parameters inside this file

## 2. Create the Dockerfile
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

## 3. Build the Docker Image
Build the Docker image with the following command:

```bash
docker build -t fasttransfer-lambda-image .
```
This will create a Docker image called `fasttransfer-lambda-image`.

## 4. Push the Docker Image to Amazon ECR

### 1. Create an ECR repository (if you don't have one already):
```bash
aws ecr create-repository --repository-name fasttransfer-lambda-repo
```

### 2. Authenticate Docker with ECR:
```bash
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.eu-west-1.amazonaws.com
```
Replace `<aws_account_id>` with your AWS account ID.

### 3. Tag the Docker image to push it to ECR:
```bash
docker tag fasttransfer-lambda-image:latest <aws_account_id>.dkr.ecr.eu-west-1.amazonaws.com/fasttransfer-lambda-repo:latest
```

### 4. Push the Docker image to your ECR repository:
```bash
docker push <aws_account_id>.dkr.ecr.eu-west-1.amazonaws.com/fasttransfer-lambda-repo:latest
```

## 5. Create a Lambda Function with the Docker Image

Create a Lambda function using the Docker image you've just pushed:

```bash
aws lambda create-function \
  --function-name FastTransferLambda \
  --package-type Image \
  --image-uri <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/fasttransfer-lambda-repo:latest \
  --role arn:aws:iam::<aws_account_id>:role/<lambda_execution_role> \
  --timeout 120 \
  --memory-size 5000 \
  --ephemeral-storage 10000
```
Replace `<aws_account_id>` with your AWS account ID and `<lambda_execution_role>` with the IAM role that has the necessary permissions to run Lambda.

## Environment Variables

Here are the environment variables you need to set in your Dockerfile or Lambda:

- **HOME**: Sets the default working directory.
- **DOTNET_BUNDLE_EXTRACT_BASE_DIR**: Temporary directory for extracted files.

