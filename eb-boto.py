import boto3

#variable for using Boto3Client
eb_client = boto3.client("elasticbeanstalk")
asg_client = boto3.client("autoscaling")

#Empty List Declaration
env_arn_list = []
tag_check = []
list_env_tags = []
environment_id = []
environment_name = []
asg_group_id = []


#Returns descriptions for existing environments.
env_arn = eb_client.describe_environments()
for get_arn in env_arn["Environments"]:
    env_arn_list.append(get_arn["EnvironmentArn"])                  #Saved Output in env_arn_list


#Return the tags applied to an AWS Elastic Beanstalk resource
for arn_tags in env_arn_list:
    list_tags = eb_client.list_tags_for_resource(ResourceArn = arn_tags)["ResourceTags"]
    tag_check.append(list_tags)                                     #Saved Output in tag_check

#Loop to get list of tags which containes environment : dev
for x in tag_check:
    for y in range(0,len(tag_check)):
        if x[y]["Key"] == "environment" and x[y]["Value"] == "dev":
            for i in range(0,len(x)):
                list_env_tags.append(list(x[i].values()))                       #Saved Output in list_env_tags

#Loop to get list of environments id who has environment : dev
for get_env_id in list_env_tags:
    if get_env_id[0] == "elasticbeanstalk:environment-id":
        environment_id.append(get_env_id[1])                                #Saved Output in environment_id

#Loop to get list of environments name who has environment : dev
for get_env_name in list_env_tags:
    if get_env_name[0] == "elasticbeanstalk:environment-name":
        environment_name.append(get_env_name[1])                            #Saved Output in environment_name

#Loop to get AutoScalingGroup of specific environments id and environments name
for asg in range(0,len(environment_id)):
    response_asg = eb_client.describe_environment_resources(
        EnvironmentId=environment_id[asg],
        EnvironmentName=environment_name[asg]
        )
    asg_group_id.append(response_asg["EnvironmentResources"]["AutoScalingGroups"][0]["Name"])   #Saved Output in asg_group_id

#Sets ASG to Minimum Count to 0 or 1 
for asg_count in range(0,len(asg_group_id)):
    response = asg_client.update_auto_scaling_group(
        AutoScalingGroupName=asg_group_id[asg_count],
        MinSize=0
    )
    print(response)


# print(env_arn_list)
# print(tag_check)
# print(list_env_tags)
# print(environment_id)
# print(environment_name)
# print(asg_group_id)
