import adal
from pypowerbi.dataset import Column, Table, Dataset
from pypowerbi.client import PowerBIClient
from Credentials import client_id, username, password

# The Report to Refresh
group_id = "<your dataset's group id>"
dataset_id = "<your dataset's report id>"

# create your powerbi api client
client = PowerBIClient.get_client_with_username_password(client_id=client_id, username=username, password=password)

notify_option = "MailOnFailure"
client.datasets.refresh_dataset(dataset_id, notify_option=notify_option, group_id=group_id)
