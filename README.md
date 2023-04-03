# Apis Azure Synapse

# Information this project

This project aims to explain very simply how to create and configure a user application, to access the Azure Synapse APIs, and provides some example codes to obtain the access token, and how to perform some post and get.

## Create user application

The user application has the purpose of generating a token that will validate our access to the Synapse api.
Two ways to create the user application.

The simplest way is to run the following command in the Azure Cloud Shell in the Azure portal itself. Remembering that you need to make sure that the logged in user has sufficient permissions for the task.

```bash
az ad sp create-for-rbac
```

After executing the command, you will get the following output. Remember to save this information, it will be used later when we run the code that will access the api.
Follow the correspondence of the fields, later on we use other names

- appId = client id
- tenant = tenant id
- password = client secret

![Mobile 1](https://github.com/Lodbrockcraft/Apis_Azure_Synapses/blob/main/assets/ids_prompcomand.png)

The other way would be to create the user application directly in the azure portal.
- Sign-in to the Azure portal.
- Search for and Select Azure Active Directory.
- Select App registrations, then select New registration.
- Name the application, for example "example-app".
- Select a supported account type, which determines who can use the application.
- Under Redirect URI, select Web for the type of application you want to create. Enter the URI where the access token is sent to.
- Select Register.

![Mobile 1](https://github.com/Lodbrockcraft/Apis_Azure_Synapses/blob/main/assets/create-app.png)

When creating the main service you will need to save 3 information about it.
- client id
- tenant id
- client secret

![Mobile 1](https://github.com/Lodbrockcraft/Apis_Azure_Synapses/blob/main/assets/create-app-ids.png)

The client secret you need to generate in the Certificates & secrets part, clicking on new secret.
The client secret value will be the value field.

![Mobile 1](https://github.com/Lodbrockcraft/Apis_Azure_Synapses/blob/main/assets/create-app-secret.png)

Now that we know how to create the user.
We need to add this user to a security group. This group can be created in the using conventional way. This group is required to have service principal communication with the azure resource. You can even use this security group for other service principal that will be used in other Microsoft APIs.

After creating the group and including the user within it. You will need to go to the Azure Synapse resource within the portal, and include this group in the Access control (IAM) as the minimum contributor, so you are calling the api https://management.core.windows.net/.
This api gives you access to resource information and other purposes.

To access your synapse workspace information such as pipelines, triggers, notebooks, dataflow etc. You need to insert the group in the Access control inside the synapse workspace. Depending on what you want to do, you'll need to assign this group to the workspace admin role.
Example: apis that create or delete pipelines need an admin permission.

This configuration is required to access the api type https://dev.azuresynapse.net.

Esse grupo é necessário para que tenha uma comunicação do service principal com o recurso do azure.

# Liberys

- Request
- Adal
- Pandas

# Documentation used
https://blog.jongallant.com/2021/02/azure-rest-apis-postman-2021/
https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal
