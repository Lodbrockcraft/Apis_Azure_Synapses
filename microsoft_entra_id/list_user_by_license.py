import requests
import adal
import json
import pandas as pd
from pyspark.shell import sqlContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from delta.tables import *
from pyspark.sql import *

spark = SparkSession.builder.appName('Exemplo').getOrCreate()

tenant_id = ''
client_id = ''
client_secret = ''

authority_url = f'https://login.microsoftonline.com/{tenant_id}'
resource_url = 'https://graph.microsoft.com'

url = 'https://graph.microsoft.com/v1.0/users?$select=id,assignedLicenses&$top=999'

#===== Generate token for accessing api =====
def access_token_header():
    context = adal.AuthenticationContext(authority=authority_url,
                                        validate_authority=True,
                                        api_version=None)

    token = context.acquire_token_with_client_credentials(resource_url, client_id, client_secret)
    access_token = token.get('accessToken')
    header = {'Authorization': f'Bearer {access_token}'}
    return header

#===== Define schema structure =====
schema = StructType([
    StructField('id', StringType(), True),
    StructField('assignedLicenses', ArrayType(MapType(StringType(), StringType())), True)
])

#===== Call the API and create dataframe =====
# Due to the pagination of the api, it was necessary to create a loop to pull the url from the next page to call again and save the data in the dataframe.
# Lear more in https://learn.microsoft.com/pt-br/graph/paging?tabs=http

url_pag = url

df = spark.createDataFrame([], schema)

while url_pag != '':
    js = requests.get(url_pag, headers=access_token_header()).json()
    data = spark.createDataFrame(js['value'], schema)
    df = df.unionByName(data, allowMissingColumns=True)
    if '@odata.nextLink' in js:
        url_pag = js['@odata.nextLink']
    else:
        url_pag = ''

#===== Web scraping microsoft license descriptions =====
from bs4 import BeautifulSoup

response = requests.get('https://learn.microsoft.com/pt-br/entra/identity/users/licensing-service-plan-reference')
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("table")

df_html = pd.read_html(str(table))[0]
df_html = spark.createDataFrame(df_html.astype('str'))

#===== Extract skuId in assignedLicenses column =====

di = df.select(
    'id',
    explode('assignedLicenses').alias('assignedLicenses')
).select('id', 'assignedLicenses.skuId')

#===== Join dataframes =====

di = di.join(
    df_html, di.skuId == df_html['GUID'], 'left'
).select(
    di.id,
    di.skuId,
    df_html['Nome do produto'].alias('DescLicense')
)

#===== Check if any licenses are left without a description =====
# en-us Create a list with some user that had licenses without description. We do this to reduce the number of requests.

list_id = di.filter(di.DescLicense.isNull()).groupBy(
    di.skuId
).agg(
    max(di.id).alias('id')
).select(
    'id'
).collect()

list_id = [row.id for row in list_id]

print(list_id)

# en-us Creates a dataframe with the missing descriptions.

schema = StructType([
    StructField('skuId', StringType(), True),
    StructField('skuPartNumber', StringType(), True),
    StructField('id', StringType(), True),
    StructField('servicePlans', StringType(), True)
])

df_skuId_null = spark.createDataFrame([], schema)

for l in list_id:
    js = requests.get(f'https://graph.microsoft.com/v1.0/users/{l}/licenseDetails', headers=access_token_header()).json()
    data = spark.createDataFrame(js['value'], schema)
    df_skuId_null = df_skuId_null.unionByName(data, allowMissingColumns=True)

df_skuId_null = df_skuId_null.select(col('skuId').alias('idLicense'), 'skuPartNumber').distinct()

# en-us Perform a join and fill in the missing restrictions.

di = di.join(
    df_skuId_null, di.skuId == df_skuId_null.idLicense, 'left'
).select(
    di.id,
    di.skuId,
    di.DescLicense,
    df_skuId_null.skuPartNumber
).withColumn(
    'DescLicense', when(di.DescLicense.isNull(), df_skuId_null.skuPartNumber).otherwise(di.DescLicense)
).drop(df_skuId_null.skuPartNumber)

#===== Save dataframe in delta file =====
di.write.format("delta").save(path)