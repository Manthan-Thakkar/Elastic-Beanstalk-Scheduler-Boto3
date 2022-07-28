import boto3
#variable for using Boto3Client
eb_client = boto3.client("elasticbeanstalk")
asg_client = boto3.client("autoscaling")
#Empty List Declaration
env_arn_list = []
tag_check = []
env_id_name_tags = []
environment_id = []
environment_name = []
asg_group_id = []
#Returns descriptions for existing environments.
env_arn = eb_client.describe_environments()
for get_arn in env_arn["Environments"]:
    env_arn_list.append(get_arn["EnvironmentArn"])                  #Saved Output in env_arn_list
#Return the tags applied to an AWS Elastic Beanstalk resource
for arn_tags in env_arn_list:
    env_tags = eb_client.list_tags_for_resource(ResourceArn = arn_tags)["ResourceTags"]
    tag_check.append(env_tags)
    for tag in env_tags:
        if tag["Key"] == "environment" and tag["Value"] == "dev":
            env_id_name_tags.append(list(env_tags))                                      #Saved Output in tag_check
for env_t in env_id_name_tags:    
    environment_id.append(next((item for item in env_t if item["Key"] == "elasticbeanstalk:environment-id"), None)["Value"])                        #Saved Output in environment_name
#Loop to get AutoScalingGroup of specific environments id and environments name
for asg_id in environment_id:
    response_asg = eb_client.describe_environment_resources(
        EnvironmentId=asg_id
        )
    asg_group_id.append(response_asg["EnvironmentResources"]["AutoScalingGroups"][0]["Name"])   #Saved Output in asg_group_id
#Sets ASG to Minimum Count to 0 or 1 
for asg_count in range(0,len(asg_group_id)):
    response = asg_client.update_auto_scaling_group(
        AutoScalingGroupName=asg_group_id[asg_count],
        MinSize=0,
        MaxSize=0
    )
    print(response)

# print(env_arn_list)
# print(tag_check)
# print(env_id_name_tags)
# print(environment_id)
# print(environment_name)
# print(asg_group_id)