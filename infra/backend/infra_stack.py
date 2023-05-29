from aws_cdk import Stack, aws_lambda, aws_iam
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the IAM role
        role = aws_iam.Role(
            self, "LambdaRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # Create the Lambda function
        lambda_function = aws_lambda.Function(
            self, "emailassistant-backend-test",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="index.handler",
            code=aws_lambda.Code.from_inline("def handler(event, context):\n    print('Hello, World!')"),
            role=role
        )

        lambda_function = aws_lambda.Function(
            self, "emailassistant-frontend-test",
            runtime=aws_lambda.Runtime.NODEJS_18_X,
            handler="index.handler",
            code=aws_lambda.Code.from_inline("export const handler = async(event) => {\n   return null;\n};"),
            role=role
        )

