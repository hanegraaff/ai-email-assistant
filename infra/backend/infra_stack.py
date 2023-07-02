from aws_cdk import Stack, aws_lambda, aws_iam
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_route53, Tags, aws_route53_targets, aws_certificatemanager, aws_s3_deployment 
from aws_cdk import aws_s3, RemovalPolicy, aws_cloudfront, aws_cloudfront_origins
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
        Tags.of(role).add("Name", "lambda-assume-role")

        #
        # DNS & Certificates
        #
        hosted_zone = aws_route53.HostedZone.from_hosted_zone_attributes(self, "hosted_zone", zone_name=DOMAIN_NAME, hosted_zone_id=HOSTED_ZONE_ID)

        cert = aws_certificatemanager.Certificate(self, 
            "emailassistant-frontend-cert", 
            domain_name="*.%s" % DOMAIN_NAME ,
            validation=aws_certificatemanager.CertificateValidation.from_dns(hosted_zone=hosted_zone))
        


        #
        # Public Website
        # S3 / Cloudfront / Static Content
        #

        static_content_bucket = aws_s3.Bucket(self, id + "_s3-bucket",
            encryption=aws_s3.BucketEncryption.S3_MANAGED,
            #website_index_document='index.html',
            #website_error_document='error.html',
            public_read_access=True,
            enforce_ssl=False,
            removal_policy= RemovalPolicy.DESTROY,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ACLS,
            access_control=aws_s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL
        )

        aws_s3_deployment.BucketDeployment(self, "static-content-deployment",
            sources=[aws_s3_deployment.Source.asset("../application_source/static_content")],
            destination_bucket=static_content_bucket
        )

        static_content_distribution = aws_cloudfront.Distribution(self, "email-assistant-website",
            default_behavior=aws_cloudfront.BehaviorOptions(origin=aws_cloudfront_origins.S3Origin(static_content_bucket)),
            domain_names=["www.%s" % DOMAIN_NAME],
            certificate=cert,
            default_root_object="index.html"
        )


        static_content_record = aws_route53.ARecord(self, "static_content_alias_record",
            zone=hosted_zone,
            record_name="www",
            target=aws_route53.RecordTarget(
                alias_target=aws_route53_targets.CloudFrontTarget(static_content_distribution)
            )
        )

        Tags.of(static_content_record).add("component_name", component_name)
        Tags.of(static_content_record).add("Name", "frontend_alias_record")


        # Serverless APIs
        #

        backend_lambda_function = aws_lambda.Function(
            self, "emailassistant-api-service",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="handlers.lambda_handler.handler",
            code=assets.backend_package,
            role=role
        )
        Tags.of(backend_lambda_function).add("component_name", component_name)
        Tags.of(backend_lambda_function).add("Name", "backend-service")
        
        #
        #
        #
        
        #
        # Lambda/API frontend
        #
        '''
            frontend_lambda_function = aws_lambda.Function(
                self, "emailassistant-frontend-service",
                runtime=aws_lambda.Runtime.NODEJS_18_X,
                handler="lambda.handler",
                code=assets.frontend_package,
                role=role
            )
            Tags.of(frontend_lambda_function).add("component_name", component_name)
            Tags.of(frontend_lambda_function).add("Name", "frontend_service")
        '''

        api = apigateway.LambdaRestApi(self, "backend-api",
            handler=backend_lambda_function,
            proxy=False
        )

        items = api.root.add_resource("test-data")
        items.add_method("GET") # GET /test-data

        #api.root.add_method("GET")

        '''
        items = api.root.add_resource("items")
        items.add_method("GET") # GET /items

        item = items.add_resource("{method}")
        item.add_method("GET") # GET /items/{method}
        '''
        
        Tags.of(api).add("component_name", component_name)
        Tags.of(api).add("Name", "frontend_api")

        # Create a custom domain name for the API that will be
        # mapped to route 53 via an "A" record
        custom_domain_name = apigateway.DomainName(self, "frontend_custom_domain-name", 
            domain_name = "api-prod.%s" % DOMAIN_NAME,
            certificate=cert,
            mapping=api)
        
        # note that the domain name for the custom domain and A record must match.
        api_record = aws_route53.ARecord(self, "api_alias_record",
            zone=hosted_zone,
            record_name="api-prod",
            target=aws_route53.RecordTarget(
                alias_target=aws_route53_targets.ApiGatewayDomain(custom_domain_name)
            )
        )

        Tags.of(api_record).add("component_name", component_name)
        Tags.of(api_record).add("Name", "frontend_alias_record")

