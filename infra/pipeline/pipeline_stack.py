import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from pipeline.infra_stage import InfraStage
from aws_cdk.aws_lambda import AssetCode
from aws_cdk import BundlingOptions, DockerImage

class MyPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        backend_package = AssetCode.from_asset(
            "backend.zip",
            bundling=BundlingOptions(
                image=DockerImage.from_registry("alpine"),
                command=["sh", "-c", "pwd"]
            )
        )


        pipeline =  CodePipeline(self, "Pipeline",
                        pipeline_name="EmailAssistantPipeline",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.git_hub("hanegraaff/ai-email-assistant", "feature/initial-development", authentication=cdk.SecretValue.secrets_manager("emailassistant/githubtoken")),
                            commands=["npm install -g aws-cdk", 
                                "cd infra",
                                "python -m pip install -r requirements.txt",
                                "cdk synth",
                                "mv cdk.out .."
                            ]
                        )
                    )
        
        pipeline.add_stage(InfraStage(self, "Deploy-AppInfra-Stack"))