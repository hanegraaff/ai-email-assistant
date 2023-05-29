import aws_cdk as cdk
from constructs import Construct
from backend.infra_stack import InfraStack


class InfraStage(cdk.Stage):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        infra_stack = InfraStack(self, "InfraStack")