from pypowerbi.client import PowerBIClient
from pypowerbi.activity_logs import ActivityLogs
from datetime import datetime

import pandas as pd

from Credentials import client_id, username, password

# create your powerbi api client
client = PowerBIClient.get_client_with_username_password(client_id=client_id, username=username, password=password)

# When testing, only logs from December 15th, 2019 and later were available. This may change in the future though.
dt = datetime(2019, 12, 16)
logs = client.activity_logs.get_activity_logs(dt)
print(logs)

pandas_installed = True
try:
    import pandas as pd
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
except ImportError:
    pandas_installed = False

if pandas_installed:
    # If pandas is installed, we can do lots of neat analysis
    df = pd.DataFrame(logs)
    print(df.columns)
    print(df["UserId"].unique())
    #df.to_csv(r"d:\powerbi_activity.csv")


