import requests
import adal
import json
import pandas as pd

tenant_id = ''
client_id = ''
client_secret = ''

authority_url = f'https://login.microsoftonline.com/{tenant_id}'
resource_url = 'https://graph.microsoft.com'

url_api = 'https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses,companyName,country,userPrincipalName, department,displayName,employeeId,givenName,jobTitle,mail,createdDateTime,onPremisesDomainName,onPremisesSamAccountName,officeLocation,postalCode,city,state,streetAddress,telephoneNumber,surname,usageLocation,alternateEmailAddress,userType,memberOf,licenseDetails&$top=999'

#===== Generate token for accessing api =====
def access_token_header():
    context = adal.AuthenticationContext(authority=authority_url,
                                        validate_authority=True,
                                        api_version=None)

    token = context.acquire_token_with_client_credentials(resource_url, client_id, client_secret)
    access_token = token.get('accessToken')
    header = {'Authorization': f'Bearer {access_token}'}
    return header


#===== Call the API and create dataframe =====
# Due to the pagination of the api, it was necessary to create a loop to pull the url from the next page to call again and save the data in the dataframe.
# Lear more in https://learn.microsoft.com/pt-br/graph/paging?tabs=http

url_pag = url_api

df = pd.DataFrame()

while url_pag != '':
    js = requests.get(url_pag, headers=access_token_header()).json()
    data = pd.json_normalize(js['value'])
    df = pd.concat([df,data])
    if '@odata.nextLink' in js:
        url_pag = js['@odata.nextLink']
    else:
        url_pag = ''

# Save dataframe in csv file
df.to_csv(f'C:/temp/list_resource.csv', index=False)