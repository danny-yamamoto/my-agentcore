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
        "arn:aws:ecr:us-east-1:123456789012:repository/my-agentcore"
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
        "arn:aws:logs:us-east-1:123456789012:log-group:/aws/bedrock-agentcore/runtimes/*",
        "arn:aws:logs:us-east-1:123456789012:log-group:*"
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
        "arn:aws:logs:us-east-1:123456789012:log-group:/aws/bedrock-agentcore/runtimes/*:log-stream:*"
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

</details>

## AgentCore のデプロイ

```bash
# 設定
agentcore configure --entrypoint my_strands_agents.py -er arn:aws:iam::123456789012:role/RoleMyAgentCoreUsEast1

# 起動
agentcore launch
```

## 参考リンク

- [Qiita記事](https://qiita.com/har1101/items/73fa749e05c4cb38bb6e)
- [AWS Blog: Introducing Amazon Bedrock AgentCore](https://aws.amazon.com/jp/blogs/aws/introducing-amazon-bedrock-agentcore-securely-deploy-and-operate-ai-agents-at-any-scale/)
