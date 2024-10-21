from azure.storage.blob import *

# Replace with your values
sas_token = ""
account_name = ""
container_name = ""
 
# Construct the BlobServiceClient with the SAS token URL
blob_service_client = BlobServiceClient(
    f"https://{account_name}.blob.core.windows.net?{sas_token}"
)
 
# Access a container using the client
container_client = blob_service_client.get_container_client(container_name)
 
# List blobs in the container
print("Blobs in container:")
for blob in container_client.list_blobs():
    print(blob.name)