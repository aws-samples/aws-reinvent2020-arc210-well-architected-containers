# Blue / green deployments with AWS developer tools

A long, long time ago, I wrote a blog post the captured my experiences setting up a continues delivery pipeline for a containerised application, using the AWS developer tools: AWS CodePipeline, AWS CodeBuild and AWS CodeCommit.

It has been almost two years since I wrote that post. Prompted by some recent customer conversations, now felt like the right time for a reboot.

## Safety first

As organisations stive to meet the needs of tehir customers, there is a constant tension between moving fast: reducing the time to value; and moving safely: not breaking stuff.w

The basic idea being that you have two environments running, your blue and your green. One represents the current release and the other represents the new release.

When the time comes to cutover to the new release, you can do some safe in the knowledge that you have a working environment (the current release) available to roll back to, just in case something goes wrong. A hot standby if you will!

Simple docker container with nginx and some js to refresh and serve random cat memes.

## From the bottom ...

Let's start by creating ourselves a repository for storing our project.

    aws codecommit create-repository --repository-name go-frontend

