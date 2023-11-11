import json
import os
import subprocess
import time

import azurerm
from azure.cosmosdb.table.models import Entity
from azure.storage.queue import QueueServiceClient
from dotenv import load_dotenv

load_dotenv()

# Get Auth token to interact with Azure and Subscription ID
get_token = subprocess.run(
    ["az account get-access-token | jq -r .accessToken"],
    stdout=subprocess.PIPE,
    shell=True,
)
auth_token = get_token.stdout.decode("utf-8").rstrip()
subscription_id = azurerm.get_subscription_from_cli()

# Define variable to hold the RG name, Storage Account name and location
resource_group_name = os.environ["AZURE_RESOURCE_GROUP_NAME"]
storageaccount_name = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
location = os.environ["AZURE_LOCATION"]


# Create the resource group with the given name
response = azurerm.create_resource_group(
    auth_token, subscription_id, resource_group_name, location
)
if response.status_code == 200 or response.status_code == 201:
    print(f"Resource group: {resource_group_name} created successfully.")
else:
    print(
        (
            f"Error creating resource group {resource_group_name}: "
            f"status code={response.status_code}"
        )
    )

# Create storage account with the given name
response = azurerm.create_storage_account(
    auth_token,
    subscription_id,
    resource_group_name,
    storageaccount_name,
    location,
    storage_type="Standard_LRS",
)
if response.status_code == 202:
    print(f"Storage account: {storageaccount_name} created successfully.")
    print(
        (
            "Waiting for 15 seconds for the storage account to be ready "
            "before attempting to create a Queue"
        )
    )
    time.sleep(15)
else:
    print(
        (
            f"Error creating storage account {storageaccount_name}: "
            f"status code={response.status_code}"
        )
    )

# Use Azure Storage SDK to create a Queue
response = azurerm.get_storage_account_keys(
    auth_token, subscription_id, resource_group_name, storageaccount_name
)
storageaccount_keys = json.loads(response.text)
storageaccount_primarykey = storageaccount_keys["keys"][0]["value"]

# Initializing the Queue client
queue_service = QueueServiceClient(
    account_url=f"https://{storageaccount_name}.queue.core.windows.net/",
    credential={
        "account_name": storageaccount_name,
        "account_key": storageaccount_primarykey,
    },
)

# Creating the queue
queue = queue_service.create_queue("myqueue")
print(f"Storage Queue 'myqueue' successfully created.")

# Sending some messages
queue.send_message("Veggie pizza ordered")
queue.send_message("Pepperoni pizza ordered")
queue.send_message("Hawaiian pizza ordered")
queue.send_message("Pepperoni pizza ordered")
queue.send_message("Pepperoni pizza ordered")

# Giving some time to the system to reconcile
time.sleep(1)

# Getting the number of messages in the queue
num_messages = queue.get_queue_properties().approximate_message_count
print(f"There are {num_messages} message(s) in 'myqueue'")

# Retrieve messages
response = queue.receive_messages(messages_per_page=2)
for message in response:
    print(message.content)
    queue.delete_message(message)

# Getting the number of messages in the queue again
num_messages = queue.get_queue_properties().approximate_message_count
print(f"There are {num_messages} message(s) in 'myqueue'")


input(f"Press Enter to tear down the resource group {resource_group_name}")
queue.delete_queue()
response = azurerm.delete_resource_group(
    auth_token, subscription_id, resource_group_name
)
if response.status_code == 202:
    print(f"Resource group {resource_group_name} successfully deleted.")
else:
    print(
        (
            f"Could not delete {resource_group_name!r}: "
            "status={response.status_code}"
        )
    )
