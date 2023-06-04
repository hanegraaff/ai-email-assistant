from aws_cdk import Stack, aws_lambda, aws_iam
from constructs import Construct
from aws_cdk import Tags
from pipeline.assets import backend_package

class InfraStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        component_name = "Application Bakend"

        # Create the IAM role
        role = aws_iam.Role(
            self, "LambdaRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # Create the Lambda function
        
        backend_lambda_function = aws_lambda.Function(
            self, "emailassistant-backend-test",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="handlers.lambda_handler.handler",
            code=backend_package,
            role=role
        )


        frontend_lambda_function = aws_lambda.Function(
            self, "emailassistant-frontend-test",
            runtime=aws_lambda.Runtime.NODEJS_18_X,
            handler="index.handler",
            code=aws_lambda.Code.from_inline("export const handler = async(event) => {\n   return null;\n};"),
            role=role
        )


        #
        # Tags
        #
        Tags.of(role).add("component_name", component_name)
        Tags.of(role).add("Name", "LambdaAssumeRole")

        Tags.of(backend_lambda_function).add("component_name", component_name)
        Tags.of(role).add("Name", "BackendService")

        Tags.of(frontend_lambda_function).add("component_name", component_name)
        Tags.of(role).add("Name", "FrontEndService")

