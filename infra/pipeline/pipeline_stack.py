import aws_cdk as cdk
from constructs import Construct
from aws_cdk import Tags
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from pipeline.infra_stage import InfraStage

class MyPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline =  CodePipeline(self, "Pipeline",
                        pipeline_name="EmailAssistantPipeline",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.git_hub("hanegraaff/ai-email-assistant", "feature/initial-development", authentication=cdk.SecretValue.secrets_manager("emailassistant/githubtoken")),
                            commands=[
                                # Build the backend code
                                "make -C application_source/backend",

                                # Build the assembly
                                "npm install -g aws-cdk", 
                                "cd infra",
                                "python -m pip install -r requirements.txt",
                                "cdk synth",
                                "mv cdk.out .."
                            ]
                        )
                    )
        
        infrastrage = InfraStage(self, "Email-Assistant-Infra")

        Tags.of(pipeline).add("Name", "Pipeline")


        # Add a tag to all constructs in the stack
        Tags.of(infrastrage).add("app_name", "EmailAssistant")
        Tags.of(infrastrage).add("app_cost_center", "1234")
        Tags.of(infrastrage).add("component_type", "Application Infra")

        pipeline.add_stage(infrastrage)