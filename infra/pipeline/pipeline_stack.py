import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from pipeline.infra_stage import InfraStage
from aws_cdk.aws_s3 import Bucket
from aws_cdk.pipelines import CodeBuildStep
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
from aws_cdk import aws_codepipeline as codepipeline

class MyPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        codebuild_project = codebuild.Project(self, "PackageCode",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
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
                },
            }),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_4_0,
            ),
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