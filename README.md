
# Well-architected containers: 10x performance with DevOps

The purpose of this project is to showcase safe and secure software deployments using AWS container management and developer tools. The project includes a deloyment pipeline which enforces image scanning using Amazon ECRs image scanning functionality. The pipeline is also configured to do blue-green deployments using Amazon CodeDepoy.

> TODO: Add capacity providers with EC2 instances.

> TODO: Configure scaling - show how spot can be used to scale up.

> TODO: Include load generation to generate load to scale up on to spot.

## Prerequisites

Before getting started this project should be forked.

1. In the top right hand corner of the screen, click on the  **Fork** button.

2. Follow the onscreen prompts to fork this project in to your own Github account.

Once you have sucessfully forked the project, continue on to the next steps.

### Create a Github secret

1. Login to [GitHub](https://www.github.com).

2. From the user account menu click **Settings**.

3. From the Personal settings menu on the left hand side choose **Developer Settings**.

4. Choose **Personal access tokens**.

5. Click **Generate new token**.

6. In the **Note** field, enter a short description of the use case for this personal access token.

7. Check the permissions **admin:repo_hook** and **repo**.

8. Click **Generate token**.

9. Record the personal access token. You will need this in the next step.

## Deploy the base stack

To get started, you will need to deploy the base stack. Click on the button below to deploy the base stack using AWS CloudFormation.

1. On the **Create stack** screen click **Next**.

2. On the **Specify stack details** screen enter the following for the stack parameters, and then click **Next**.:

    1. **githubUsername**: Enter your Github username. 

    2. **githubRepo**: Enter the name of the forked Github repository. This should be **aws-reinvent2020-arc210-well-architected-containers**.

    3. **githubAccessToken**: Enter the Github access token you created above.

2. Accept the defaults on the **Configure stack options** and click **Next**.

3. Scroll to the bottom of the **Review arc210-stack** screen.

4. Tick **I acknowledge that AWS CloudFormation might create IAM resources with custom names.** This needs to be done becuase this template creates a number of IAM related resources.

5. Finally, click **Create stack**.

## Create the CodeBuild Deployment Group

In this step you will create a DeploymentGroup that will be used by Amazon CodeDeploy to manage the blue-green deployment of application updates to the Amazon ECS service that was deployed as part of the base environment.

1.	In the AWS Console, ensure you have the correct region selected.

2.	In the **Management Tools** search for **CodeDeploy** and click on the link that appears.

3.	On the left hand menu, click on **Applications**.

4. Click on the application with **arc210-stack-** in the name.

5. At the bottom of the screen, click **Create deployment group**.

6. On the **Create deployment group** screen:

    1. Enter a name for the deployment group. e.g. **arc210-dg**

    2. Under **Service role** choose the named **CodeDeploy4ECSRole**

    3. Next, from the ***Choose an ECS cluster name** drop down, choose the ECS cluster called **Cluster-arc210-stack**.

    4. From the **Choose an ECS service name** drop down, choose the service with the name that starts  **arc210-stack-**.

    5. In the **Choose a load balancer** drop down, select the load balancer with the name that starts **arc21-ARC21-**.

    6. Choose **HTTP:80** for the **Production listener port**.

    7. Do not select a **Test listener port - optional**.

    8. From the **Target group 1 name**  drop down, chosoe **ARC210-Blue-TG**.

    9. From the **Target group 2 name**  drop down, chosoe **ARC210-Green-TG**.

    10. Finally, under the **Deployment settings** change the **Deployment configuration** to  **CodeDeployDefault.ECSLinear10PercentEvery1Minutes**.

    11. Click **Create deployment group**.

## Update the CodePipeline Pipeline

Now that you've created the

1. Open the [AWS CodePipline management console](console.aws.amazon.com/codesuite/codepipeline/pipelines)

2. Click on the pipeline called **ARC210-Pipeline**.

3. At the top of the screen, click **Edit** to edit the pipeline.

4. Scroll down to the **Deploy** stage and click on the **Edit stage** button.

5. Once the stage becomes editable, two small icons will appear under the world **Deploy**. Click on the one which looks like a small rectangle with a line going up and to the right.

6. On the **Edit action** screen:

    1. Find the **AWS CodeDeploy application name** field, delete the placeholder value and choose the application with the name that starts **arc210-stack-**.

    2. In the **AWS CodeDeploy deployment group** choose the deployment group you created above.

    3. Click **Done**.

7. Back on the **Editing: ARC210-Pipeline** screeen, at the top, click **Save**.

8. On the **Save pipeline changes** confirmation screen, click **Save**.

The environment is now setup. You can now proceed with the demo.

## Well Architected Design Principles 

### Cost Optimisation

Implement Cloud Financial Management | Adopt a consumption model | Measure overall efficiency | Stop spending money on undifferentiated heavy lifting | Analyze and attribute expenditure

### Performance

Democratize advanced technologies | Go global in minutes | Use serverless architectures | Experiment more often | Consider mechanical sympathy

### Security

Implement a strong identity foundation | Enable traceability | Apply security at all layers | Automate security best practices | Protect data in transit and at rest | Keep people away from data | Prepare for security events

### Operational Excellence

Perform operations as code | Make frequent, small, reversible changes | Refine operations procedures frequently | Anticipate failure | Learn from all operational failures

### Reliability

Automatically recover from failure | Test recovery procedures | Scale horizontally to increase aggregate workload availability | Stop guessing capacity | Manage change in automation


## Demo walkthrough

### A diagram of what we've just deployed

Here is what we've just deployed.

![Arch Diagram](/images/arc_diagram.png)

### Confirming everything deployed correctly

Let's test that the application which we just deployed is up and running.

1. In the AWS Console, ensure you have the correct region selected.

2. In the Management Tools search for CloudFormation and click on the link that appears.

3. Click on the CloudFormation stack that was created as part of this lab. It is probably called **arch210-stack**. 

4. Choose the **Outputs** tab from stack details (The right hand side of the screen).

5. You should see a value labelled **LoadBalancerDnsName** value. This is the URL of the load balancer which will host the application.

6. Click on the link an ensure that you are successfully able to connect to the the **Welcome to nginx** home page.

#### Checkpoint:

Nice work! You have verified that your containerized application is working as exepcted. Next, lets make some changes to see our blue-green deployments in action.

### Push changes and see blue-green deployments in action

In this task, you will make a change to the project and monitor the **SAFE** deployment that is done using AWS CodeDeploy and the ECS blue-green deployment provider.

### Push changes and see container image scanning in actions

In this task, you will update the container image used by the application to one which container vulnerabilites. You will monitor the deploymen to see how the ECRs native container image scanning solution can be used to stop deployments of artifacts that container vulnerabilites. 

### Push change and see how blue-green deployments can save your bacon!

In this task, you will generate load to cause the ECS service to scale. As more tasks are added to the cluster, the MemoryReservation metric for the cluster will increase. Because the EC2 Spot fleet Auto Scaling is set up to scale based on MemoryReservation, this will cause the underlying EC2 Spot fleet to scale. 

### Launch load generator to tirgger some scaling

In this task, you will generate load to cause the ECS service to scale. As more tasks are added to the cluster, the MemoryReservation metric for the cluster will increase. Because the EC2 Spot fleet Auto Scaling is set up to scale based on MemoryReservation, this will cause the underlying EC2 Spot fleet to scale. 

You will create a CloudFormation stack containing a load generator that sends load to the cats and dogs containers, and then verify the tasks scale as expected.

1. Let's get started by deploying the load generator instance by clicking on this button:

    [![Launch load generator](images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=ecsServiceloadgenerator&templateURL=https://s3.amazonaws.com/mythical-mysfits-website/fargate/core.yml)

4. In **Stack name**, enter **ecsServiceloadgenerator**.

5. Leave the LabSetupStackName parameter at its default, unless you changed the name of the CloudFormation stack from the Lab setup.

6. Click **Next**, then click **Next** again, then click **Create**.

7. Wait until the stack status is **CREATE_COMPLETE**.

**Note:** the LoadGenerator instance uses the Vegeta load generator. More information about this is available at: https://github.com/tsenart/vegeta . The CloudFormation template injects the URL of your load balancer so Vegeta sends requests to the correct endpoint

8. In the AWS Console, under **Management Tools** click **CloudWatch**.

9. Click **Metrics**.

10.	On the **All metrics** tab, click **ApplicationELB**, then **Per AppELB, per AZ, per TG Metrics**.

11.	Find the LoadBalancer where the name starts with **arc210-ARC210** and select the **RequestCount** metrics.

12.	On the **Graphed metrics** tab, change the **Statistic** to **Sum**, and the **Period to 10 seconds**.

13.	After a minute or two you should start to see an increase in request counts, to around 1500 each for the cats and dogs target groups. Note that the simpleHomepage target group is not accessed by the load generator.

14.	Click **Alarms**.

15.	After the load has been sustained for two minutes, the **Lab2-CatsScaleUpAlarm** and **Lab2-DogsScaleUpAlarm** should enter the ALARM state.

16.	In the AWS Console, under **Compute** click **EC2 Container Service**.

17.	In the ECS console click **Clusters**, then click the cluster **catsndogsECScluster**.

18.	Click Services and click either the cats or dogs service.

19.	Click the Events tab. You should see events as ECS adds more tasks to the Service

## Additional container resources

[Domain reduces scaling time for their mobile API services with Amazon ECS](https://aws.amazon.com/blogs/containers/domain-reduces-scaling-time-for-their-mobile-api-services-with-amazon-ecs/ "AWS Container Blog")

[Self-Paced Workshop - Amazon ECS on AWS Fargate](https://github.com/aws-samples/amazon-ecs-mythicalmysfits-workshop "From Monoliths to Microservices with Mythical Mysfits")

[Self-Paced Workshop – Amazon ECS Capacity Providers](https://ecsworkshop.com/capacity_providers/ "Amazon ECS Workshop Series")