from aws_cdk import Stack, aws_lambda, aws_iam
from aws_cdk import aws_apigateway as apigateway
from constructs import Construct
from aws_cdk import Tags
from pipeline import assets

class InfraStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        component_name = "Application Bakend"

        # Create the IAM role
        role = aws_iam.Role(
            self, "LambdaRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com")
        )

        #
        # Lambda backend
        #

        backend_lambda_function = aws_lambda.Function(
            self, "emailassistant-backend-test",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="handlers.lambda_handler.handler",
            code=assets.backend_package,
            role=role
        )

        #
        # Lambda/API frontend
        #



        frontend_lambda_function = aws_lambda.Function(
            self, "emailassistant-frontend-test",
            runtime=aws_lambda.Runtime.NODEJS_18_X,
            handler="lambda.handler",
            code=assets.frontend_package,
            role=role
        )

        api = apigateway.RestApi(self, "frontend-api",
                  rest_api_name="Frontend Service",
                  description="This is the initial frontend service.")

        get_frontend_integration = apigateway.LambdaIntegration(frontend_lambda_function,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", get_frontend_integration)   # GET /


        #
        # Tags
        #
        Tags.of(role).add("component_name", component_name)
        Tags.of(role).add("Name", "LambdaAssumeRole")

        Tags.of(backend_lambda_function).add("component_name", component_name)
        Tags.of(backend_lambda_function).add("Name", "BackendService")

        Tags.of(frontend_lambda_function).add("component_name", component_name)
        Tags.of(frontend_lambda_function).add("Name", "FrontEndService")

