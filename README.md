# pypowerbi

Python library for PowerBI. Loosely modelled after the C# PowerBI library to keep things somehow consistent.

## Installation

```
pip install pypowerbi
```

## Examples

### Posting a dataset

```
import adal
from pypowerbi.dataset import Column, Table, Dataset
from pypowerbi.client import PowerBIClient

# you might need to change these, but i doubt it
authority_url = 'https://login.windows.net/common'
resource_url = 'https://analysis.windows.net/powerbi/api'
api_url = 'https://api.powerbi.com'

# change these to your credentials
client_id = '00000000-0000-0000-0000-000000000000'
username = 'someone@somecompany.com'
password = 'averygoodpassword'

# first you need to authenticate using adal
context = adal.AuthenticationContext(authority=authority_url,
                                     validate_authority=True,
                                     api_version=None)

# get your authentication token
token = context.acquire_token_with_username_password(resource=resource_url,
                                                     client_id=client_id,
                                                     username=username,
                                                     password=password)

# create your powerbi api client
client = PowerBIClient(api_url, token)

# create your columns
columns = []
columns.append(Column(name='id', data_type='Int64'))
columns.append(Column(name='name', data_type='string'))
columns.append(Column(name='is_interesting', data_type='boolean'))
columns.append(Column(name='cost_usd', data_type='double'))
columns.append(Column(name='purchase_date', data_type='datetime'))

# create your tables
tables = []
tables.append(Table(name='AnExampleTableName', columns=columns))

# create your dataset
dataset = Dataset(name='AnExampleDatasetName', tables=tables)

# post your dataset!
client.datasets.post_dataset(dataset)
```

### Authentication & Authorization

It uses `adal` library for authentication and authorization. If you need step by step way to do auth, please refer to [this example on Bitbucket](https://bitbucket.org/omnistream/powerbi-api-example/).
