# AutoGen 0.4.0

## The use case

Two agents creating a plot of Tesla's and NVIDIA's stock returns using an *agentic* approach:
+ Two classes `Assistant` and `Executor`. The `Assistant` agent writes code and the `Executor` agent executes the code.
+ A `Message` data class which represents the messages that can be passed between the agents.

The agents's logic whether it is using `model_client` (`ChatCompletionClient`) or `code_executor` (`CodeExecutor`) is completely decoupled from how messages are delivered:
> the framework provides a communication infrastructure (the **Agent Runtime**), and their agents are responsible for their logic.

The Agent Runtime delivers messages and manages the agents' lifecycle (the creation of the agents is therefore handled by the Agent runtime).

The code in [01: AutoGen Quick Start](01_autogen-quick-start/) uses the `SingleThreadedAgentRuntime` implementation.

Once executed, you will see the interaction between the `Assistant` and the `Executor`. When running it, you will see how a Docker container is spun up and the interaction between the agents happen there. You will also be able to have a look at the result by running:

```bash
$ cd tmp

$ ls -lrt

$ 
```
