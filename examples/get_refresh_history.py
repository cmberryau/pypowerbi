import adal
from pypowerbi.dataset import Column, Table, Dataset
from pypowerbi.client import PowerBIClient

from Credentials import client_id, username, password

# Dataset to get refresh history for
group_id = "<your dataset's group id>"
dataset_id = "<your dataset's report id>"

# create your powerbi api client
client = PowerBIClient.get_client_with_username_password(client_id=client_id, username=username, password=password)

# Get the entire refresh history
history = client.datasets.get_dataset_refresh_history(dataset_id, group_id=group_id)
print(history)

# Get the most recent refresh
history = client.datasets.get_dataset_refresh_history(dataset_id, group_id=group_id, top=1)
print(history)