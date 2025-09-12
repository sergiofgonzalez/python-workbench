# 02: Listing the connections of Azure AI Foundry project

## How To

This project uses `uv`. To run the project type:

```bash
uv run main.py
```

The program will list the connections associated to the Azure AI Foundry project, and will try to identify an storage account to connect to it and download all the files found on a particular container.

You will need to have an environment variable or `.env` file with the `PROJECT_ENDPOINT`.

Additionally, you should create a storage account and define an env variable `STG_ACCOUNT_NAME` with its name and put a file into a container which you can identify with `CONTAINER_NAME`, so that the program can download it.

Then, configure this storage account as a connected resource.

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

