import aws_cdk as core
import aws_cdk.assertions as assertions
from aws_cdk.assertions import Match

from backend.infra_stack import InfraStack

# example tests. To run these tests, uncomment this file along with the example
# resource in infra/infra_stack.py
def test_lambda_function_created():
    app = core.App()
    stack = InfraStack(app, "infra")
    template = assertions.Template.from_stack(stack)


    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "python3.8"
    })

    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "nodejs18.x"
    })


    template.has_resource_properties("AWS::Lambda::Function", {
        "Tags": Match.array_with([
            {
                "Key": "component_name",
                "Value": "Application Bakend"
            },
            {
                "Key": "Name",
                "Value": Match.any_value()
            }
        ])})





    

    
