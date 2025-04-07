# atoms.CallsApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**start_outbound_call**](CallsApi.md#start_outbound_call) | **POST** /conversation/outbound | Start an outbound call


# **start_outbound_call**
> StartOutboundCall200Response start_outbound_call(start_outbound_call_request)

Start an outbound call

Initiates an outbound conversation with a specified agent and phone number.

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.start_outbound_call200_response import StartOutboundCall200Response
from smallestai.atoms.models.start_outbound_call_request import StartOutboundCallRequest
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
    api_instance = atoms.CallsApi(api_client)
    start_outbound_call_request = atoms.StartOutboundCallRequest() # StartOutboundCallRequest | 

    try:
        # Start an outbound call
        api_response = api_instance.start_outbound_call(start_outbound_call_request)
        print("The response of CallsApi->start_outbound_call:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CallsApi->start_outbound_call: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_outbound_call_request** | [**StartOutboundCallRequest**](./models/StartOutboundCallRequest.md)|  | 

### Return type

[**StartOutboundCall200Response**](./models/StartOutboundCall200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully started the outbound conversation |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to API list]](../../README.md#documentation-for-api-endpoints)

