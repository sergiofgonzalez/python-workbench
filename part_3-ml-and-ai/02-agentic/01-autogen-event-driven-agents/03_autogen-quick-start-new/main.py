"""Agents' registration and run for AutoGen v0.4.0 Quick Start."""

import asyncio
import os
import tempfile

from autogen_core.application import SingleThreadedAgentRuntime
from autogen_core.components import DefaultTopicId
from autogen_core.components.models import AzureOpenAIChatCompletionClient
from autogen_ext.code_executor.docker_executor import (
    DockerCommandLineCodeExecutor,
)
from dotenv import load_dotenv

from agents import Assistant, Executor, Message

# read env vars from .env
load_dotenv()

work_dir = tempfile.mkdtemp()

# create a local embedded runtime: the orchestrator
runtime = SingleThreadedAgentRuntime()


async def run_with_docker() -> None:
    """Register the agents and run them."""
    try:
        async with DockerCommandLineCodeExecutor(work_dir=work_dir) as executor:
            # register the assistant and executor agents
            await Assistant.register(
                runtime,
                "assistant",
                lambda: Assistant(
                    AzureOpenAIChatCompletionClient(
                        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                        api_version="2023-05-15",
                        azure_deployment="chat_gpt4o",
                        model="gpt-4o",
                        temperature=0,
                        model_capabilities={
                            "chat": True,
                            "vision": True,
                            "json_output": True,
                            "function_calling": True,
                        },
                    ),
                ),
            )
            await Executor.register(
                runtime,
                "executor",
                lambda: Executor(executor),
            )

            # start the runtime and publish a message to the assistant.
            runtime.start()
            await runtime.publish_message(
                Message(
                    "Create a plot of NVIDIA vs TSLA stock returns YTD "
                    "from 2024-01-01.",
                ),
                DefaultTopicId(),
            )
            await runtime.stop_when_idle()
    except Exception as e:  # noqa: BLE001
        print(f"Exception in async flow: {e}")
        await runtime.stop_when_idle()


async def main() -> None:
    """Entry point of the application."""
    await run_with_docker()


if __name__ == "__main__":
    asyncio.run(main())
