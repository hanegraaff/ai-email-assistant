from aws_cdk.aws_lambda import AssetCode
from aws_cdk import Tags


component_name = "Application Bakend"

'''frontend_package = AssetCode.from_asset(
            "../application_source/frontend/target/frontend_application.zip",
        )
        
    Tags.of(frontend_package).add("component_name", component_name)
    Tags.of(frontend_package).add("Name", "FrontendServiceAsset")
'''

backend_package = AssetCode.from_asset(
            "../application_source/backend/target/handlers.zip",
        )

Tags.of(backend_package).add("component_name", component_name)
Tags.of(backend_package).add("Name", "BackendServiceAsset")
