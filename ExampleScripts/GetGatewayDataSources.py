import adal
from pypowerbi.dataset import Column, Table, Dataset
from pypowerbi.client import PowerBIClient

from Credentials import client_id, username, password

# Dataset to get gateway info for
group_id = "<your dataset's group id>"
dataset_id = "<your dataset's report id>"

# create your powerbi api client
client = PowerBIClient.get_client_with_username_password(client_id=client_id, username=username, password=password)

# do_refresh(client, group_id, dataset_id)
notify_option = "MailOnFailure"
data_sources = client.datasets.get_dataset_gateway_datasources(dataset_id, group_id=group_id)
print(data_sources)
