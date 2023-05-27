# Instructions

```
$ python3 -m venv .venv
$ source .venv/bin/activate

cd infra

pip install -r requirements.txt

cdk ls
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation