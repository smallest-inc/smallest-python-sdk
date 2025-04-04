# atoms.KnowledgeBaseApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_knowledge_base**](KnowledgeBaseApi.md#create_knowledge_base) | **POST** /knowledgebase | Create a knowledge base
[**delete_knowledge_base**](KnowledgeBaseApi.md#delete_knowledge_base) | **DELETE** /knowledgebase/{id} | Delete a knowledge base
[**delete_knowledge_base_item**](KnowledgeBaseApi.md#delete_knowledge_base_item) | **DELETE** /knowledgebase/{knowledgeBaseId}/items/{knowledgeBaseItemId} | Delete a knowledge base item
[**get_knowledge_base_by_id**](KnowledgeBaseApi.md#get_knowledge_base_by_id) | **GET** /knowledgebase/{id} | Get a knowledge base
[**get_knowledge_base_items**](KnowledgeBaseApi.md#get_knowledge_base_items) | **GET** /knowledgebase/{id}/items | Get all knowledge base items
[**get_knowledge_bases**](KnowledgeBaseApi.md#get_knowledge_bases) | **GET** /knowledgebase | Get all knowledge bases
[**upload_media_to_knowledge_base**](KnowledgeBaseApi.md#upload_media_to_knowledge_base) | **POST** /knowledgebase/{id}/items/upload-media | Upload a media to a knowledge base
[**upload_text_to_knowledge_base**](KnowledgeBaseApi.md#upload_text_to_knowledge_base) | **POST** /knowledgebase/{id}/items/upload-text | Upload a text to a knowledge base


# **create_knowledge_base**
> CreateKnowledgeBase201Response create_knowledge_base(create_knowledge_base_request)

Create a knowledge base

Create a knowledge base

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.create_knowledge_base201_response import CreateKnowledgeBase201Response
from smallestai.atoms.models.create_knowledge_base_request import CreateKnowledgeBaseRequest
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
    api_instance = atoms.KnowledgeBaseApi(api_client)
    create_knowledge_base_request = atoms.CreateKnowledgeBaseRequest() # CreateKnowledgeBaseRequest | 

    try:
        # Create a knowledge base
        api_response = api_instance.create_knowledge_base(create_knowledge_base_request)
        print("The response of KnowledgeBaseApi->create_knowledge_base:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KnowledgeBaseApi->create_knowledge_base: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_knowledge_base_request** | [**CreateKnowledgeBaseRequest**](CreateKnowledgeBaseRequest.md)|  | 

### Return type

[**CreateKnowledgeBase201Response**](CreateKnowledgeBase201Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Knowledge base created successfully |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_knowledge_base**
> DeleteAgent200Response delete_knowledge_base(id)

Delete a knowledge base

Delete a knowledge base

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.delete_agent200_response import DeleteAgent200Response
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
    api_instance = atoms.KnowledgeBaseApi(api_client)
    id = 'id_example' # str | The ID of the knowledge base

    try:
        # Delete a knowledge base
        api_response = api_instance.delete_knowledge_base(id)
        print("The response of KnowledgeBaseApi->delete_knowledge_base:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KnowledgeBaseApi->delete_knowledge_base: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the knowledge base | 

### Return type

[**DeleteAgent200Response**](DeleteAgent200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Knowledge base deleted successfully |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_knowledge_base_item**
> DeleteAgent200Response delete_knowledge_base_item(knowledge_base_id, knowledge_base_item_id)

Delete a knowledge base item

Delete a knowledge base item

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.delete_agent200_response import DeleteAgent200Response
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
    api_instance = atoms.KnowledgeBaseApi(api_client)
    knowledge_base_id = 'knowledge_base_id_example' # str | The ID of the knowledge base
    knowledge_base_item_id = 'knowledge_base_item_id_example' # str | The ID of the knowledge base item

    try:
        # Delete a knowledge base item
        api_response = api_instance.delete_knowledge_base_item(knowledge_base_id, knowledge_base_item_id)
        print("The response of KnowledgeBaseApi->delete_knowledge_base_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KnowledgeBaseApi->delete_knowledge_base_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **knowledge_base_id** | **str**| The ID of the knowledge base | 
 **knowledge_base_item_id** | **str**| The ID of the knowledge base item | 

### Return type

[**DeleteAgent200Response**](DeleteAgent200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Knowledge base item deleted successfully |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_knowledge_base_by_id**
> GetKnowledgeBaseById200Response get_knowledge_base_by_id(id)

Get a knowledge base

Get a knowledge base

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.get_knowledge_base_by_id200_response import GetKnowledgeBaseById200Response
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
    api_instance = atoms.KnowledgeBaseApi(api_client)
    id = 'id_example' # str | The ID of the knowledge base

    try:
        # Get a knowledge base
        api_response = api_instance.get_knowledge_base_by_id(id)
        print("The response of KnowledgeBaseApi->get_knowledge_base_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KnowledgeBaseApi->get_knowledge_base_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the knowledge base | 

### Return type

[**GetKnowledgeBaseById200Response**](GetKnowledgeBaseById200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A knowledge base |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_knowledge_base_items**
> GetKnowledgeBaseItems200Response get_knowledge_base_items(id)

Get all knowledge base items

Get all knowledge base items

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.get_knowledge_base_items200_response import GetKnowledgeBaseItems200Response
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
    api_instance = atoms.KnowledgeBaseApi(api_client)
    id = 'id_example' # str | The ID of the knowledge base

    try:
        # Get all knowledge base items
        api_response = api_instance.get_knowledge_base_items(id)
        print("The response of KnowledgeBaseApi->get_knowledge_base_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KnowledgeBaseApi->get_knowledge_base_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the knowledge base | 

### Return type

[**GetKnowledgeBaseItems200Response**](GetKnowledgeBaseItems200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of knowledge base items |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_knowledge_bases**
> GetKnowledgeBases200Response get_knowledge_bases()

Get all knowledge bases

Get all knowledge bases

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.get_knowledge_bases200_response import GetKnowledgeBases200Response
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
    api_instance = atoms.KnowledgeBaseApi(api_client)

    try:
        # Get all knowledge bases
        api_response = api_instance.get_knowledge_bases()
        print("The response of KnowledgeBaseApi->get_knowledge_bases:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KnowledgeBaseApi->get_knowledge_bases: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetKnowledgeBases200Response**](GetKnowledgeBases200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of knowledge bases |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_media_to_knowledge_base**
> DeleteAgent200Response upload_media_to_knowledge_base(id, media)

Upload a media to a knowledge base

Upload a media to a knowledge base

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.delete_agent200_response import DeleteAgent200Response
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
    api_instance = atoms.KnowledgeBaseApi(api_client)
    id = 'id_example' # str | The ID of the knowledge base
    media = None # bytearray | 

    try:
        # Upload a media to a knowledge base
        api_response = api_instance.upload_media_to_knowledge_base(id, media)
        print("The response of KnowledgeBaseApi->upload_media_to_knowledge_base:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KnowledgeBaseApi->upload_media_to_knowledge_base: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the knowledge base | 
 **media** | **bytearray**|  | 

### Return type

[**DeleteAgent200Response**](DeleteAgent200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Knowledge base item created successfully |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_text_to_knowledge_base**
> DeleteAgent200Response upload_text_to_knowledge_base(id, upload_text_to_knowledge_base_request)

Upload a text to a knowledge base

Upload a text to a knowledge base

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.delete_agent200_response import DeleteAgent200Response
from smallestai.atoms.models.upload_text_to_knowledge_base_request import UploadTextToKnowledgeBaseRequest
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
    api_instance = atoms.KnowledgeBaseApi(api_client)
    id = 'id_example' # str | The ID of the knowledge base
    upload_text_to_knowledge_base_request = atoms.UploadTextToKnowledgeBaseRequest() # UploadTextToKnowledgeBaseRequest | 

    try:
        # Upload a text to a knowledge base
        api_response = api_instance.upload_text_to_knowledge_base(id, upload_text_to_knowledge_base_request)
        print("The response of KnowledgeBaseApi->upload_text_to_knowledge_base:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KnowledgeBaseApi->upload_text_to_knowledge_base: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the knowledge base | 
 **upload_text_to_knowledge_base_request** | [**UploadTextToKnowledgeBaseRequest**](UploadTextToKnowledgeBaseRequest.md)|  | 

### Return type

[**DeleteAgent200Response**](DeleteAgent200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Knowledge base item created successfully |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

