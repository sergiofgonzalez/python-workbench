# 03: Creating a chat (using chat completions) using Azure AI Foundry SDK

## How To

This project uses `uv`. To run the project type:

```bash
uv run main.py
```

The program will prompt the user for a question and will convey it to a model deployed on Azure AI Foundry.

The program requires setting:

+ `PROJECT_ENDPOINT`: Your Azure AI Foundry project endpoint.
+ `DEPLOYMENT_NAME`: The name of a deployment within your Azure AI Foundry project.

### General Prerequisites

1. Create an Azure AI Foundry project. Once created, click on the "Overview" page of the navigation pane, and in the "Endpoints and keys" panel, make sure that "Azure AI Foundry" is selected on the "Libraries" section. Make sure to copy the "Azure AI Foundry project endpoint".

2. Create a new Python project. Add the packages:
    + `azure-ai-projects` &mdash; Azure AI Foundry SDK (note the trailing 's')
    + `azure-identity` &mdash; Authentication library

3. Make sure you have installed Azure CLI following the instructions from https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest. You can check you have it installed by running:

    ```bash
    az --version
    ```

4. Make sure you have installed a browser. When running on WSL, make sure to check https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps for details.

5. Create an authenticated session using `az login`. If you have access to multiple subscriptions, you might need to use the `--tenant` option passing the corresponding `TENANT_ID`. Please note that the `TENANT_ID` is different from the subscription ID:

    ```
    [Tenant and subscription selection]

    No     Subscription name    Subscription ID                       Tenant
    -----  -------------------  ------------------------------------  ------------------------------------
    [1] *  Subscription name    2f49....-....-....-....-............  ebc7....-....-....-....-............
    ```

