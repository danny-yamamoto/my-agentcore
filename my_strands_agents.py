from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()

agent = Agent()


@app.entrypoint
def invoke(payload):
    """Process user input and return a response"""

    user_message = payload.get("prompt", "Hello")

    return {"result": user_message}


if __name__ == "__main__":

    app.run()
