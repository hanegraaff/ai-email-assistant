import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from pipeline.infra_stage import InfraStage
class MyPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline =  CodePipeline(self, "Pipeline",
                        pipeline_name="EmailAssistantPipeline",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.git_hub("hanegraaff/ai-email-assistant", "feature/initial-development", authentication=cdk.SecretValue.secrets_manager("emailassistant/githubtoken")),
                            commands=["npm install -g aws-cdk", 
                                "cd infra",
                                "python -m pip install -r requirements.txt",
                                "cdk synth",
                                "mv cdk.out .."
                                ]#,
                                #primary_output_directory= 'infra'
                        )
                    )
        
        pipeline.add_stage(InfraStage(self, "InfraState"))