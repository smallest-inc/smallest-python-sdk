# atoms.CallsApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**start_outbound_call**](CallsApi.md#start_outbound_call) | **POST** /conversation/outbound | Start an outbound call

# **start_outbound_call**

Initiates an outbound conversation with a specified agent and phone number.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    call_request = {
        "agent_id": "your_agent_id",
        "phone_number": "+1234567890"
    }
    
    response = atoms_client.start_outbound_call(start_outbound_call_request=call_request)
    print(f"Started call with conversation ID: {response.conversation_id}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**start_outbound_call_request** | [**StartOutboundCallRequest**](./models/StartOutboundCallRequest.md) | Call configuration | 

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

