# atoms.OrganizationApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_organization**](OrganizationApi.md#get_organization) | **GET** /organization | Get organization details

# **get_organization**

Get details of the current organization.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    response = atoms_client.get_organization()
    print(f"Organization details: {response}")

if __name__ == "__main__":
    main()
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**GetOrganization200ResponseData**](./models/GetOrganization200ResponseData.md)

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

[[Back to API list]](../../README.md#documentation-for-api-endpoints)

