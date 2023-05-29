import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from pipeline.infra_stage import InfraStage

class MyPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Configure CodeBuild to use a drop-in Docker replacement.
        code_build_defaults=cdk.pipelines.CodeBuildOptions(
            partial_build_spec=cdk.aws_codebuild.BuildSpec.from_object({
                "phases": {
                    "install": {
                        "commands": [
                            "echo Installing...",
                            "apt-get update",
                            "apt-get install -y zip"
                        ]
                    },
                    "build": {
                        "commands": [
                            "echo Building...",
                            "zip -r application.zip application_source/backend/"
                        ]
                    },
                }
            })
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
                        ),
                        code_build_defaults = code_build_defaults
                        
                    )
        
        pipeline.add_stage(InfraStage(self, "Deploy-AppInfra-Stack"))