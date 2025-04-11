# atoms.LogsApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_conversation_logs**](LogsApi.md#get_conversation_logs) | **GET** /conversation/{id} | Get conversation logs

# **get_conversation_logs**

Get conversation logs for a specific conversation ID.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    conversation_id = "your_conversation_id"
    response = atoms_client.get_conversation_logs(id=conversation_id)
    print(f"Conversation logs: {response}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | The conversation ID to retrieve logs for | 

### Return type

[**GetConversationLogs200ResponseData**](./models/GetConversationLogs200ResponseData.md)

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

[[Back to API list]](../../README.md#documentation-for-api-endpoints)

