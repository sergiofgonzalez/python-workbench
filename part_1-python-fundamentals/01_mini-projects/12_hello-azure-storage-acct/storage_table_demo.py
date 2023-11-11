import json
import os
import subprocess
import time

import azurerm
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tableservice import TableService
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
            "before attempting to create a Table"
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

# Use Azure Storage SDK to create a Table
response = azurerm.get_storage_account_keys(
    auth_token, subscription_id, resource_group_name, storageaccount_name
)
storageaccount_keys = json.loads(response.text)
storageaccount_primarykey = storageaccount_keys["keys"][0]["value"]
table_service = TableService(
    account_name=storageaccount_name, account_key=storageaccount_primarykey
)
response = table_service.create_table("mytable")
if response == True:
    print("Table 'mytable' successfully created.")
else:
    print("Table 'mytable' couldn't be created.")

# Give the system some time reconcile new changes
time.sleep(1)


# Adding some data to our table
pizza = Entity()
pizza.PartitionKey = "pizzamenu"
pizza.RowKey = "001"
pizza.description = "Pepperoni"
pizza.cost = 18
table_service.insert_entity("mytable", pizza)
print("Created record for Pepperoni pizza.")

pizza = Entity()
pizza.PartitionKey = "pizzamenu"
pizza.RowKey = "002"
pizza.description = "Veggie"
pizza.cost = 15
table_service.insert_entity("mytable", pizza)
print("Created record for Veggie pizza.")

pizza = Entity()
pizza.PartitionKey = "pizzamenu"
pizza.RowKey = "003"
pizza.description = "Hawaiian"
pizza.cost = 12
table_service.insert_entity("mytable", pizza)
print("Created record for Hawaiian pizza.")

# Give the system some time to reconcile changes
time.sleep(1)

# Query the data now
pizzas = table_service.query_entities(
    "mytable", filter="PartitionKey eq 'pizzamenu'", select="description, cost"
)
for pizza in pizzas:
    print(f"Name: {pizza.description}, Cost: ${pizza.cost}")

input(f"Press Enter to tear down the resource group {resource_group_name}")
response = table_service.delete_table("mytable")
if response == True:
    print("Storage table mytable successfully deleted.")
else:
    print(f"Could not delete 'mytable': {response}")

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
