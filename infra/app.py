#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Tags
from pipeline.pipeline_stack import MyPipelineStack


app = cdk.App()
pipleine_stack = MyPipelineStack(app, "EmailAssistantPipelineStack")

# Add a tag to all constructs in the stack
Tags.of(pipleine_stack).add("app_name", "EmailAssistant")
Tags.of(pipleine_stack).add("app_cost_center", "1234")
Tags.of(pipleine_stack).add("component_type", "Application Infra")

app.synth()

