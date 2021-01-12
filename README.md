
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

[![Launch ARC210](images/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=arc210-stack&templateURL=https://catsndogs-assets.s3.amazonaws.com/arc210-templates/arc210-template.yaml)

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

1. Browse to the forked GitHub repository that you created in step 1 of the **Prerequisites**.

2. Open the **containerApp/** folder and find the **containerApp/index.html** file. Click on the **containerApp/index.html** file.

3. With **containerApp/index.html** open, locate the small pencil icon in the top right of the file viwer window. Click the icon to edit the file.

4. On **line 15** change the value of the **background** property to different colour. For example, **red** or **green** or **blue**.

5. Scroll down. In the **Commit changes** form, enter a title for the change, i.e. **Changing background colour**. 

6. Click the **Commit change** button.

7. Open the [AWS CodePipline management console](console.aws.amazon.com/codesuite/codepipeline/pipelines)

8. Click on the pipeline called **ARC210-Pipeline**.

9. The pipeline should have started to run. You can confirm this by looking for the commit comment next to one or more of the stages.

10. Wait for the pipeline to reach the **Deploy** stage. After a few seconds, you should see a **Details** link appear. Click on that link to reveal details about the status of the deployment.

11. Monitor the progress of the deployment using the **Deployment status** and **Traffic shifting progress** information.

12. From time to time, check the the URL you recorded earlier from the **LoadBalancerDnsName** CloudFormation output. You might need to click the browsers refresh button. You should see a certain number of requests hitting the new version of the application with the updated background colour.

#### Checkpoint:

After about 10-15 minutes, the deployment should complete. Nice work! You have just updated the application, committed the change and safely deployed it using the blue-green deployment pattern.

## Additional container resources

[Domain reduces scaling time for their mobile API services with Amazon ECS](https://aws.amazon.com/blogs/containers/domain-reduces-scaling-time-for-their-mobile-api-services-with-amazon-ecs/ "AWS Container Blog")

[Self-Paced Workshop - Amazon ECS on AWS Fargate](https://github.com/aws-samples/amazon-ecs-mythicalmysfits-workshop "From Monoliths to Microservices with Mythical Mysfits")

[Self-Paced Workshop – Amazon ECS Capacity Providers](https://ecsworkshop.com/capacity_providers/ "Amazon ECS Workshop Series")