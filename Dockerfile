FROM public.ecr.aws/lambda/python:3.12

# Install libicu using dnf (package manager for Amazon Linux 2)
RUN dnf install -y icu libicu

# Set necessary environment variables
ENV HOME=/tmp
ENV DOTNET_BUNDLE_EXTRACT_BASE_DIR=/tmp
#ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=true  # Optional, use it to disable globalization support

# Copy necessary files into the container
COPY FastTransfer /var/task/FastTransfer
COPY FastTransfer_Settings.json /var/task/FastTransfer_Settings.json
COPY handler.py /var/task/handler.py

# Set proper permissions for the binary
RUN chmod +x /var/task/FastTransfer

# Lambda command
CMD ["handler.lambda_handler"]


