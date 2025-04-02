# atoms_client.LogsApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_conversation**](LogsApi.md#get_conversation) | **GET** /conversation/{id} | Get conversation logs


# **get_conversation**
> GetConversation200Response get_conversation(id)

Get conversation logs

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import atoms_client
from smallestai.atoms_client.models.get_conversation200_response import GetConversation200Response
from smallestai.atoms_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://atoms-api.smallest.ai/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = atoms_client.Configuration(
    host = "https://atoms-api.smallest.ai/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): BearerAuth
configuration = atoms_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with atoms_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = atoms_client.LogsApi(api_client)
    id = 'id_example' # str | The callId of the conversation. You can get the callId from the conversation logs.

    try:
        # Get conversation logs
        api_response = api_instance.get_conversation(id)
        print("The response of LogsApi->get_conversation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LogsApi->get_conversation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The callId of the conversation. You can get the callId from the conversation logs. | 

### Return type

[**GetConversation200Response**](GetConversation200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

