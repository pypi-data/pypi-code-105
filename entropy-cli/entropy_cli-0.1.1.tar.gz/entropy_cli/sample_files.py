ENTROPY_MAIN = """import json
from sys import argv

# edit your function from the entry point
# the event is the parameters
# do not change the signature

def entropy_main(event, context):
    # this is the entry point
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return "this is another test"
"""


DOCKER_CONTENT = """
FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY entropy_main.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "entropy_main.entropy_main" ]
"""
