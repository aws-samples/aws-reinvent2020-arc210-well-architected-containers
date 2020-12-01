
import boto3
import json
import re
import time
import logging

from crhelper import CfnResource

logger = logging.getLogger(__name__)
# Initialise the helper, all inputs are optional, this example shows the defaults
helper = CfnResource(json_logging=False, log_level='DEBUG', boto_level='CRITICAL', sleep_on_delete=120)

CDepClient = boto3.client('codedeploy')

helper = CfnResource()

@helper.create
@helper.update
def create_deployment_group(event, _):
    
    logger.info("Got Create")
    
    AppName = event['ResourceProperties']['appname'] # Code Deploy Application Name
    Arn = event['ResourceProperties']['rolearn'] # CodeDeploy4ECS Role Arn
    ServiceName = event['ResourceProperties']['ecsservicename'] # ECS Service Name
    ClusterName = event['ResourceProperties']['ecsclustername'] # ECS Cluser Name
    ListenerArn = event['ResourceProperties']['prodlistarn'] # Production Listener Arn

    response = CDepClient.create_deployment_group(
        applicationName=AppName,
        deploymentGroupName='MyDeploymentGroup',
        deploymentConfigName='CodeDeployDefault.ECSLinear10PercentEvery1Minutes',
        serviceRoleArn=Arn,
        ecsServices=[
        {
            'serviceName': ServiceName,
            'clusterName': ClusterName
        }],
        deploymentStyle={
            'deploymentType': 'BLUE_GREEN',
            'deploymentOption': 'WITH_TRAFFIC_CONTROL'
        },
        blueGreenDeploymentConfiguration={
            'terminateBlueInstancesOnDeploymentSuccess': {
                'action': 'TERMINATE',
                'terminationWaitTimeInMinutes': 5
            },
            'deploymentReadyOption': {
                'actionOnTimeout': 'CONTINUE_DEPLOYMENT',
                'waitTimeInMinutes': 0
            }
        },
        loadBalancerInfo={
        'targetGroupPairInfoList': [
            {
                'targetGroups': [
                    {
                        'name': 'ARC210-Blue-TG'
                    },
                    {
                        'name': 'ARC210-Green-TG'
                    },
                ],
                'prodTrafficRoute': {
                    'listenerArns': [
                        ListenerArn
                    ]
                }
            },
        ]},
    )
    print(response)
    
@helper.delete
def no_op(_, __):
    logger.info("Got Delete")
    pass    

def lambda_handler(event, context):
    helper(event, context)