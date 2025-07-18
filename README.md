# my-agentcore
Day One

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv version
uv venv
source .venv/bin/activate
uv init
touch my_strands_agents.py
uv pip install strands-agents bedrock-agentcore
uv run my_strands_agents.py 
uv pip install strands-agents bedrock-agentcore==0.1.0
uv run my_strands_agents.py
uv pip install bedrock-agentcore bedrock-agentcore-starter-toolkit
uv pip install strands-agents strands-agents-tools
```

- RoleMyAgentCoreUsEast1
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AssumeRolePolicy",
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock-agentcore.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
            "StringEquals": {
                "aws:SourceAccount": "123456789012"
            },
            "ArnLike": {
                "aws:SourceArn": "arn:aws:bedrock-agentcore:us-east-1:123456789012:*"
            }
       }
    }
  ]
}
```

- MyAgentCoreUsEast1
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ECRImageAccess",
            "Effect": "Allow",
            "Action": [
                "ecr:BatchGetImage",
                "ecr:GetDownloadUrlForLayer"
            ],
            "Resource": [
                "arn:aws:ecr:us-east-1:123456789012:repository/my-agentcore"
            ]        
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:DescribeLogStreams",
                "logs:CreateLogGroup"
            ],
            "Resource": [
                "arn:aws:logs:us-east-1:123456789012:log-group:/aws/bedrock-agentcore/runtimes/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:DescribeLogGroups"
            ],
            "Resource": [
                "arn:aws:logs:us-east-1:123456789012:log-group:*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-east-1:123456789012:log-group:/aws/bedrock-agentcore/runtimes/*:log-stream:*"
            ]
        },
        {
            "Sid": "ECRTokenAccess",
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow", 
            "Action": [ 
                "xray:PutTraceSegments", 
                "xray:PutTelemetryRecords", 
                "xray:GetSamplingRules", 
                "xray:GetSamplingTargets"
                ],
             "Resource": [ "*" ] 
         },
         {
            "Effect": "Allow",
            "Resource": "*",
            "Action": "cloudwatch:PutMetricData",
            "Condition": {
                "StringEquals": {
                    "cloudwatch:namespace": "bedrock-agentcore"
                }
            }
        },
        {
            "Sid": "GetAgentAccessToken",
            "Effect": "Allow",
            "Action": [
                "bedrock-agentcore:GetWorkloadAccessToken",
                "bedrock-agentcore:GetWorkloadAccessTokenForJWT",
                "bedrock-agentcore:GetWorkloadAccessTokenForUserId"
            ],
            "Resource": [
              "arn:aws:bedrock-agentcore:us-east-1:123456789012:workload-identity-directory/default",
              "arn:aws:bedrock-agentcore:us-east-1:123456789012:workload-identity-directory/default/workload-identity/*"
            ]
        },
        {
            "Sid": "BedrockModelInvocation", 
             "Effect": "Allow", 
             "Action": [ 
                    "bedrock:InvokeModel", 
                    "bedrock:InvokeModelWithResponseStream"
                  ], 
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/*",
                "arn:aws:bedrock:us-east-1:123456789012:*"
            ]
        }
    ]
}
```


```bash
agentcore configure --entrypoint my_strands_agents.py -er arn:aws:iam::123456789012:role/RoleMyAgentCoreUsEast1
```

```bash
agentcore launch
```

https://qiita.com/har1101/items/73fa749e05c4cb38bb6e
https://aws.amazon.com/jp/blogs/aws/introducing-amazon-bedrock-agentcore-securely-deploy-and-operate-ai-agents-at-any-scale/
