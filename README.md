# my-agentcore

AWS Bedrock AgentCore と Strands Agents を使用した AI エージェントのサンプルです

## セットアップ

### 環境構築

```bash
# uv のインストール
curl -LsSf https://astral.sh/uv/install.sh | sh
uv version

# 仮想環境の作成と有効化
uv venv
source .venv/bin/activate

# プロジェクトの初期化
uv init
touch my_strands_agents.py

# 必要なパッケージのインストール
uv pip install strands-agents bedrock-agentcore
uv pip install bedrock-agentcore bedrock-agentcore-starter-toolkit
uv pip install strands-agents strands-agents-tools
```

### 実行

```bash
uv run my_strands_agents.py
```

## AWS IAM ロールとポリシー

### 信頼ポリシー（RoleMyAgentCoreUsEast1）

<details>

<summary>Role</summary>

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
          "aws:SourceAccount": "XXXXXXXXXXXX"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:*"
        }
      }
    }
  ]
}
```

</details>

### 権限ポリシー（MyAgentCoreUsEast1）

<details>

<summary>Policy</summary>

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
        "arn:aws:ecr:us-east-1:XXXXXXXXXXXX:repository/my-agentcore"
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
      "Sid": "CloudWatchLogs",
      "Effect": "Allow",
      "Action": [
        "logs:DescribeLogStreams",
        "logs:CreateLogGroup",
        "logs:DescribeLogGroups"
      ],
      "Resource": [
        "arn:aws:logs:us-east-1:XXXXXXXXXXXX:log-group:/aws/bedrock-agentcore/runtimes/*",
        "arn:aws:logs:us-east-1:XXXXXXXXXXXX:log-group:*"
      ]
    },
    {
      "Sid": "CloudWatchLogsWrite",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "arn:aws:logs:us-east-1:XXXXXXXXXXXX:log-group:/aws/bedrock-agentcore/runtimes/*:log-stream:*"
      ]
    },
    {
      "Sid": "XRayAccess",
      "Effect": "Allow",
      "Action": [
        "xray:PutTraceSegments",
        "xray:PutTelemetryRecords",
        "xray:GetSamplingRules",
        "xray:GetSamplingTargets"
      ],
      "Resource": ["*"]
    },
    {
      "Sid": "CloudWatchMetrics",
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
        "arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:workload-identity-directory/default",
        "arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:workload-identity-directory/default/workload-identity/*"
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
        "arn:aws:bedrock:us-east-1:XXXXXXXXXXXX:*"
      ]
    }
  ]
}
```

</details>

## AgentCore のデプロイ

```bash
# 設定
agentcore configure --entrypoint my_strands_agents.py -er arn:aws:iam::XXXXXXXXXXXX:role/RoleMyAgentCoreUsEast1

# 起動
agentcore launch
```

```bash
(my-agentcore) vscode ➜ /workspaces/my-agentcore (main) $ agentcore launch
Launching Bedrock AgentCore (cloud mode)...

Launching Bedrock AgentCore agent 'my_strands_agents' to cloud                                                                                                   
Build: #8 3.426 Successfully built my-agentcore                                                                                                                  
Build: #8 3.433 Successfully installed my-agentcore-0.1.0                                                                                                        
Build: #9 18.40 Successfully installed annotated-types-0.7.0 anyio-4.9.0 attrs-25.3.0 bedrock-agentcore-0.1.0 boto3-1.39.8 botocore-1.39.8 certifi-2025.7.14     
click-8.2.1 docstring-parser-0.16 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 httpx-sse-0.4.1 idna-3.10 importlib-metadata-8.7.0 jmespath-1.0.1 jsonschema-4.24.1     
jsonschema-specifications-2025.4.1 mcp-1.12.0 opentelemetry-api-1.35.0 opentelemetry-instrumentation-0.56b0 opentelemetry-instrumentation-threading-0.56b0       
opentelemetry-sdk-1.35.0 opentelemetry-semantic-conventions-0.56b0 packaging-25.0 pydantic-2.11.7 pydantic-core-2.33.2 pydantic-settings-2.10.1                  
python-dateutil-2.9.0.post0 python-dotenv-1.1.1 python-multipart-0.0.20 referencing-0.36.2 rpds-py-0.26.0 s3transfer-0.13.0 six-1.17.0 sniffio-1.3.1             
sse-starlette-2.4.1 starlette-0.47.1 strands-agents-1.0.0 typing-extensions-4.14.1 typing-inspection-0.4.1 urllib3-2.5.0 uvicorn-0.35.0 watchdog-6.0.0           
wrapt-1.17.2 zipp-3.23.0                                                                                                                                         
Build: #10 30.28 ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the  
following dependency conflicts.                                                                                                                                  
Docker image built: bedrock_agentcore-my_strands_agents:latest                                                                                                   
Uploading to ECR...                                                                                                                                              
Found credentials in environment variables.                                                                                                                      
Authenticating with registry...                                                                                                                                  
Registry authentication successful                                                                                                                               
Tagging image: bedrock_agentcore-my_strands_agents:latest -> XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/my-agentcore:latest                                    
Pushing image to registry...                                                                                                                                     
⠦ Launching Bedrock AgentCore...The push refers to repository [XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/my-agentcore]
0dee2ec6a212: Pushed 
7816074ca6ea: Pushed 
8baa95691bd4: Pushed 
17210edad838: Pushed 
ffa316416cfc: Pushed 
106f4e6fd4c4: Pushed 
ff3274401a0c: Pushed 
8b31ad78e00c: Pushed 
83ab85380878: Pushed 
58d7b7786e98: Pushed 
⠹ Launching Bedrock AgentCore...latest: digest: sha256:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX size: 2416
Image pushed successfully                                                                                                                                        
Image uploaded to ECR: XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/my-agentcore                                                                                 
Creating/updating agent...                                                                                                                                       
Creating agent 'my_strands_agents' with image URI: XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/my-agentcore:latest                                              
Successfully created agent 'my_strands_agents' with ID: my_strands_agents-XXXXXXXXXX, ARN:                                                                       
arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:runtime/my_strands_agents-XXXXXXXXXX                                                                            
Agent created/updated: arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:runtime/my_strands_agents-XXXXXXXXXX                                                     
Polling for endpoint to be ready...                                                                                                                              
Agent endpoint: arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:runtime/my_strands_agents-XXXXXXXXXX/runtime-endpoint/DEFAULT                                   
✓ Image pushed to ECR: XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/my-agentcore:latest
╭───────────────────────────────────────────────────────────────── Bedrock AgentCore Deployed ──────────────────────────────────────────────────────────────────╮
│ Deployment Successful!                                                                                                                                        │
│                                                                                                                                                               │
│ Agent Name: my_strands_agents                                                                                                                                 │
│ Agent ARN: arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:runtime/my_strands_agents-XXXXXXXXXX                                                              │
│ ECR URI: XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/my-agentcore                                                                                            │
│                                                                                                                                                               │
│ You can now check the status of your Bedrock AgentCore endpoint with:                                                                                         │
│ agentcore status                                                                                                                                              │
│                                                                                                                                                               │
│ You can now invoke your Bedrock AgentCore endpoint with:                                                                                                      │
│ agentcore invoke '{"prompt": "Hello"}'                                                                                                                        │
│                                                                                                                                                               │
│ 📋 Agent logs available at:                                                                                                                                   │
│    /aws/bedrock-agentcore/runtimes/my_strands_agents-XXXXXXXXXX-DEFAULT                                                                                       │
│    /aws/bedrock-agentcore/runtimes/my_strands_agents-XXXXXXXXXX-DEFAULT/runtime-logs                                                                          │
│                                                                                                                                                               │
│ 💡 Tail logs with:                                                                                                                                            │
│    aws logs tail /aws/bedrock-agentcore/runtimes/my_strands_agents-XXXXXXXXXX-DEFAULT --follow                                                                │
│    aws logs tail /aws/bedrock-agentcore/runtimes/my_strands_agents-XXXXXXXXXX-DEFAULT --since 1h                                                              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
(my-agentcore) vscode ➜ /workspaces/my-agentcore (main) $
```

```bash
(my-agentcore) vscode ➜ /workspaces/my-agentcore (main) $ agentcore status
Found credentials in environment variables.                                                                                                                      
Getting Status for my_strands_agents
╭─────────────────────────────────────────────────────────────── Bedrock AgentCore Agent Status ────────────────────────────────────────────────────────────────╮
│ Status of the current Agent:                                                                                                                                  │
│                                                                                                                                                               │
│ Agent Name: my_strands_agents                                                                                                                                 │
│ Agent ID: my_strands_agents-XXXXXXXXXX                                                                                                                        │
│ Agent Arn: arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:runtime/my_strands_agents-XXXXXXXXXX                                                              │
│ Created at: 2025-07-18 00:56:09.226029+00:00                                                                                                                  │
│ Last Updated at: 2025-07-18 00:56:15.394104+00:00                                                                                                             │
│ Configuration details:                                                                                                                                        │
│ - region: us-east-1                                                                                                                                           │
│ - account: XXXXXXXXXXXX                                                                                                                                       │
│ - execution role: arn:aws:iam::XXXXXXXXXXXX:role/RoleMyAgentCoreUsEast1                                                                                       │
│ - ecr repository: XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/my-agentcore                                                                                   │
│                                                                                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────────────────────────────── Bedrock AgentCore Endpoint Status ──────────────────────────────────────────────────────────────╮
│ Status of the current Endpoint:                                                                                                                               │
│                                                                                                                                                               │
│ Endpoint Id: DEFAULT                                                                                                                                          │
│ Endpoint Name: DEFAULT                                                                                                                                        │
│ Endpoint Arn: arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:runtime/my_strands_agents-XXXXXXXXXX/runtime-endpoint/DEFAULT                                  │
│ Agent Arn: arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXXXXX:runtime/my_strands_agents-XXXXXXXXXX                                                              │
│ STATUS: READY                                                                                                                                                 │
│ Last Updated at: 2025-07-18 00:56:15.394121+00:00                                                                                                             │
│                                                                                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

📋 Agent logs available at:
   /aws/bedrock-agentcore/runtimes/my_strands_agents-XXXXXXXXXX-DEFAULT
   /aws/bedrock-agentcore/runtimes/my_strands_agents-XXXXXXXXXX-DEFAULT/runtime-logs

💡 Tail logs with:
   aws logs tail /aws/bedrock-agentcore/runtimes/my_strands_agents-XXXXXXXXXX-DEFAULT --follow
   aws logs tail /aws/bedrock-agentcore/runtimes/my_strands_agents-XXXXXXXXXX-DEFAULT --since 1h
(my-agentcore) vscode ➜ /workspaces/my-agentcore (main) $ 
```

```bash
(my-agentcore) vscode ➜ /workspaces/my-agentcore (main) $ agentcore invoke '{"prompt": "Hello"}'
Payload:
{
  "prompt": "Hello"
}
Invoking BedrockAgentCore agent 'my_strands_agents' via cloud endpoint                                                                                           
Found credentials in environment variables.                                                                                                                      
Session ID: ********-****-****-****-************

Response:
{
  "ResponseMetadata": {
    "RequestId": "********-****-****-****-************",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "date": "Fri, 18 Jul 2025 00:57:24 GMT",
      "content-type": "application/json",
      "transfer-encoding": "chunked",
      "connection": "keep-alive",
      "x-amzn-requestid": "********-****-****-****-************",
      "baggage": "Self=1-********-************************,session.id=********-****-****-****-************",
      "x-amzn-bedrock-agentcore-runtime-session-id": "********-****-****-****-************",
      "x-amzn-trace-id": "Root=1-********-************************;Self=1-********-************************"
    },
    "RetryAttempts": 0
  },
  "runtimeSessionId": "********-****-****-****-************",
  "traceId": "Root=1-********-************************;Self=1-********-************************",
  "baggage": "Self=1-********-************************,session.id=********-****-****-****-************",
  "contentType": "application/json",
  "statusCode": 200,
  "response": [
    "b'{\"result\":\"Hello\"}'"
  ]
}
(my-agentcore) vscode ➜ /workspaces/my-agentcore (main) $
```

## 参考リンク

- [Qiita記事](https://qiita.com/har1101/items/73fa749e05c4cb38bb6e)
- [AWS Blog: Introducing Amazon Bedrock AgentCore](https://aws.amazon.com/jp/blogs/aws/introducing-amazon-bedrock-agentcore-securely-deploy-and-operate-ai-agents-at-any-scale/)
