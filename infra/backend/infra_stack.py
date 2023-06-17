from aws_cdk import Stack, aws_lambda, aws_iam
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_route53, Tags, aws_route53_targets, aws_certificatemanager
from constructs import Construct
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

        Tags.of(role).add("component_name", component_name)
        Tags.of(role).add("Name", "LambdaAssumeRole")


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
        Tags.of(backend_lambda_function).add("component_name", component_name)
        Tags.of(backend_lambda_function).add("Name", "BackendService")


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
        Tags.of(frontend_lambda_function).add("component_name", component_name)
        Tags.of(frontend_lambda_function).add("Name", "FrontEndService")


        cert = aws_certificatemanager.Certificate(self, 
            "emailassistant-frontend-cert", 
            domain_name="*.hal-9001.com",
            validation=aws_certificatemanager.CertificateValidation.from_dns())
        
        api = apigateway.LambdaRestApi(self, "FronfEndAPI",
            handler=frontend_lambda_function,
            domain_name=apigateway.DomainNameOptions(
                domain_name="test.hal-9001.com",
                certificate=cert
            ),
            proxy=False
        )
        

        items = api.root.add_resource("items")
        items.add_method("GET") # GET /items

        item = items.add_resource("{method}")
        item.add_method("GET") # GET /items/{method}
        
        Tags.of(api).add("component_name", component_name)
        Tags.of(api).add("Name", "FrontEndAPI")
        

        hosted_zone = aws_route53.HostedZone(self, "FrondEndAPI", zone_name="hal-9001.com")

        record = aws_route53.ARecord(self, "AliasRecord",
            zone=hosted_zone,
            #target=aws_route53.RecordTarget.from_alias(aws_events_targets.ApiGateway(api))
            target=aws_route53.RecordTarget(
                alias_target=aws_route53_targets.ApiGateway(api)
            )
        )

        #Tags.of(record).add("component_name", component_name)
        #Tags.of(record).add("Name", "FrontEndRoute53Record")

