from aws_cdk import Stack, aws_lambda, aws_iam
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_route53, Tags, aws_route53_targets, aws_certificatemanager
from constructs import Construct
from pipeline import assets

#
# These need to be moved to a configuration file
#

# Assume an existing hosted zone and domain name
HOSTED_ZONE_ID = "Z07532851215U9SGEZIMZ"
DOMAIN_NAME = "hal-9001.com"

class InfraStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        component_name = "Application Bakend"

        # IAM roles
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
        # DNS & Certificates
        #
        hosted_zone = aws_route53.HostedZone.from_hosted_zone_attributes(self, "hosted_zone", zone_name=DOMAIN_NAME, hosted_zone_id=HOSTED_ZONE_ID)

        cert = aws_certificatemanager.Certificate(self, 
            "emailassistant-frontend-cert", 
            domain_name="*.%s" % DOMAIN_NAME ,
            validation=aws_certificatemanager.CertificateValidation.from_dns(hosted_zone=hosted_zone))
        

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

        api = apigateway.LambdaRestApi(self, "FronfEndAPI",
            handler=frontend_lambda_function,
            proxy=False
        )

        '''
            domain_name=apigateway.DomainNameOptions(
                domain_name="test.%s" % DOMAIN_NAME,
                certificate=cert
            ),
        '''

        items = api.root.add_resource("items")
        items.add_method("GET") # GET /items

        item = items.add_resource("{method}")
        item.add_method("GET") # GET /items/{method}
        
        Tags.of(api).add("component_name", component_name)
        Tags.of(api).add("Name", "FrontEndAPI")

        # Create a custom domain name for the API that will be
        # mapped to route 53 via an "A" record
        custom_domain_name = apigateway.DomainName(self, "CustomDomainName", 
            domain_name = "test.%s" % DOMAIN_NAME,
            certificate=cert,
            mapping=api)
        
        record = aws_route53.ARecord(self, "AliasRecord",
            zone=hosted_zone,
            target=aws_route53.RecordTarget(
                #alias_target=aws_route53_targets.ApiGateway(api)
                alias_target=aws_route53_targets.ApiGatewayDomain(custom_domain_name)
            )
        )

        Tags.of(record).add("component_name", component_name)
        Tags.of(record).add("Name", "FrontEndRoute53Record")

