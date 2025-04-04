# atoms.UserApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_current_user**](UserApi.md#get_current_user) | **GET** /user | Get user details


# **get_current_user**
> GetCurrentUser200Response get_current_user()

Get user details

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.get_current_user200_response import GetCurrentUser200Response
from smallestai.atoms.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://atoms-api.smallest.ai/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = atoms.Configuration(
    host = "https://atoms-api.smallest.ai/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): BearerAuth
configuration = atoms.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with atoms.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = atoms.UserApi(api_client)

    try:
        # Get user details
        api_response = api_instance.get_current_user()
        print("The response of UserApi->get_current_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_current_user: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetCurrentUser200Response**](GetCurrentUser200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

