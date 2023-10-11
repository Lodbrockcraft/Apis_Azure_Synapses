# This script aims to extract a list of all resources that exist within a specific resource group.
# Documentation: https://learn.microsoft.com/en-us/rest/api/resources/resources/list-by-resource-group

# Import libarys
import requests
import adal
import pandas as pd

# Create Parameters
tenant_id = ''
client_id = ''
client_secret = ''

authority_url = f'https://login.microsoftonline.com/{tenant_id}'
resource_url = 'https://management.azure.com/'

resourceGroupName = ''
subscriptionId = ''

# Create Token
# creation of token for api validation.
# we use the adal library to generate the token.
context = adal.AuthenticationContext(authority=authority_url,
                                     validate_authority=True,
                                     api_version=None)

token = context.acquire_token_with_client_credentials(resource_url, client_id, client_secret)

access_token = token.get('accessToken')

# Api url definition
url_api = f'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/resources?api-version=2021-04-01'

# Get api
# making the api call.
# if print returns 200 the call is ok.
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(url_api, headers=headers)
print(response)

# Normalizing return in json for a pandas dataframe
js = response.json()
df = pd.json_normalize(data=js['value'])

# Save dataframe in csv file
df.to_csv(f'C:/temp/list_resource.csv', index=False)