"""Agents' classes for AutoGen v0.4.0 Quick Start."""

from dataclasses import dataclass

from autogen_core.base import MessageContext
from autogen_core.components import (
    DefaultTopicId,
    RoutedAgent,
    default_subscription,
    message_handler,
)
from autogen_core.components.code_executor import (
    CodeExecutor,
    extract_markdown_code_blocks,
)
from autogen_core.components.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)


@dataclass
class Message:
    """Represent the messages that can be passed between agents."""

    content: str


@default_subscription
class Assistant(RoutedAgent):
    """An agent that writes code."""

    def __init__(self, model_client: ChatCompletionClient) -> None:
        """Initialize the Assistant agent."""
        super().__init__("An assistant agent.")
        self._model_client = model_client
        self._chat_history: list[LLMMessage] = [
            SystemMessage(
                content="""
                Write Python script in markdown block, and it will be executed.
                Always save figures to file in the current directory.
                Do not use plt.show().
                """,
            ),
        ]

    @message_handler
    async def handle_message(
        self,
        message: Message,
        ctx: MessageContext,  # noqa: ARG002
    ) -> None:
        """Handle the message."""
        self._chat_history.append(
            UserMessage(content=message.content, source="user"),
        )
        result = await self._model_client.create(self._chat_history)
        print(f"\n{'-' * 80}\nAssistant:\n{result.content}")
        self._chat_history.append(
            AssistantMessage(content=result.content, source="assistant"),
        )
        await self.publish_message(
            Message(content=result.content),
            DefaultTopicId(),
        )


@default_subscription
class Executor(RoutedAgent):
    """An agent that executes code."""

    def __init__(self, code_executor: CodeExecutor) -> None:
        """Initialize the Executor agent."""
        super().__init__("An executor agent.")
        self._code_executor = code_executor

    @message_handler
    async def handle_message(
        self,
        message: Message,
        ctx: MessageContext,
    ) -> None:
        """Handle the message."""
        code_blocks = extract_markdown_code_blocks(message.content)
        if code_blocks:
            result = await self._code_executor.execute_code_blocks(
                code_blocks,
                cancellation_token=ctx.cancellation_token,
            )
            print(f"\n{'-' * 80}\nExecutor:\n{result.output}")
            await self.publish_message(
                Message(content=result.output),
                DefaultTopicId(),
            )
