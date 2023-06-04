from aws_cdk.aws_lambda import AssetCode

from aws_cdk.aws_lambda import AssetCode
from aws_cdk import BundlingOptions, DockerImage


backend_package = AssetCode.from_asset(
            "../application_source/target/test-handlers.zip",
        )
