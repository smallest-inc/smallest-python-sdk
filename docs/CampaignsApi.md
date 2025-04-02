# atoms_client.CampaignsApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_campaign**](CampaignsApi.md#create_campaign) | **POST** /campaign | Create a campaign
[**delete_campaign**](CampaignsApi.md#delete_campaign) | **DELETE** /campaign | Delete a campaign
[**get_campaign_by_id**](CampaignsApi.md#get_campaign_by_id) | **GET** /campaign/{id} | Get a campaign
[**get_campaigns**](CampaignsApi.md#get_campaigns) | **GET** /campaign | Retrieve all campaigns
[**start_campaign**](CampaignsApi.md#start_campaign) | **POST** /campaign/{id}/start | Start a campaign
[**stop_campaign**](CampaignsApi.md#stop_campaign) | **POST** /campaign/{id}/stop | Stop a campaign


# **create_campaign**
> List[CreateCampaign200ResponseInner] create_campaign(create_campaign_request)

Create a campaign

Create a campaign

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import atoms_client
from smallestai.atoms_client.models.create_campaign200_response_inner import CreateCampaign200ResponseInner
from smallestai.atoms_client.models.create_campaign_request import CreateCampaignRequest
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
    api_instance = atoms_client.CampaignsApi(api_client)
    create_campaign_request = atoms_client.CreateCampaignRequest() # CreateCampaignRequest | 

    try:
        # Create a campaign
        api_response = api_instance.create_campaign(create_campaign_request)
        print("The response of CampaignsApi->create_campaign:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->create_campaign: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_campaign_request** | [**CreateCampaignRequest**](CreateCampaignRequest.md)|  | 

### Return type

[**List[CreateCampaign200ResponseInner]**](CreateCampaign200ResponseInner.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Campaign created successfully |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_campaign**
> DeleteAgent200Response delete_campaign(id)

Delete a campaign

Delete a campaign

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import atoms_client
from smallestai.atoms_client.models.delete_agent200_response import DeleteAgent200Response
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
    api_instance = atoms_client.CampaignsApi(api_client)
    id = 'id_example' # str | The ID of the campaign

    try:
        # Delete a campaign
        api_response = api_instance.delete_campaign(id)
        print("The response of CampaignsApi->delete_campaign:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->delete_campaign: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the campaign | 

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
**200** | Campaign deleted successfully |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_campaign_by_id**
> GetCampaignById200Response get_campaign_by_id(id)

Get a campaign

Get a campaign

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import atoms_client
from smallestai.atoms_client.models.get_campaign_by_id200_response import GetCampaignById200Response
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
    api_instance = atoms_client.CampaignsApi(api_client)
    id = 'id_example' # str | The ID of the campaign

    try:
        # Get a campaign
        api_response = api_instance.get_campaign_by_id(id)
        print("The response of CampaignsApi->get_campaign_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->get_campaign_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the campaign | 

### Return type

[**GetCampaignById200Response**](GetCampaignById200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of campaigns |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_campaigns**
> GetCampaigns200Response get_campaigns(get_campaigns_request)

Retrieve all campaigns

Get all campaigns

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import atoms_client
from smallestai.atoms_client.models.get_campaigns200_response import GetCampaigns200Response
from smallestai.atoms_client.models.get_campaigns_request import GetCampaignsRequest
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
    api_instance = atoms_client.CampaignsApi(api_client)
    get_campaigns_request = atoms_client.GetCampaignsRequest() # GetCampaignsRequest | 

    try:
        # Retrieve all campaigns
        api_response = api_instance.get_campaigns(get_campaigns_request)
        print("The response of CampaignsApi->get_campaigns:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->get_campaigns: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **get_campaigns_request** | [**GetCampaignsRequest**](GetCampaignsRequest.md)|  | 

### Return type

[**GetCampaigns200Response**](GetCampaigns200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of campaigns |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_campaign**
> DeleteAgent200Response start_campaign(id)

Start a campaign

Start a campaign

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import atoms_client
from smallestai.atoms_client.models.delete_agent200_response import DeleteAgent200Response
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
    api_instance = atoms_client.CampaignsApi(api_client)
    id = 'id_example' # str | The ID of the campaign

    try:
        # Start a campaign
        api_response = api_instance.start_campaign(id)
        print("The response of CampaignsApi->start_campaign:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->start_campaign: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the campaign | 

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
**200** | Campaign started successfully |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_campaign**
> DeleteAgent200Response stop_campaign(id)

Stop a campaign

Stop a campaign

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import atoms_client
from smallestai.atoms_client.models.delete_agent200_response import DeleteAgent200Response
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
    api_instance = atoms_client.CampaignsApi(api_client)
    id = 'id_example' # str | The ID of the campaign

    try:
        # Stop a campaign
        api_response = api_instance.stop_campaign(id)
        print("The response of CampaignsApi->stop_campaign:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CampaignsApi->stop_campaign: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The ID of the campaign | 

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
**200** | Campaign stopped successfully |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

