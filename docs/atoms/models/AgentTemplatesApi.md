# atoms.AgentTemplatesApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**agent_from_template_post**](AgentTemplatesApi.md#agent_from_template_post) | **POST** /agent/from-template | Create agent from template
[**agent_template_get**](AgentTemplatesApi.md#agent_template_get) | **GET** /agent/template | Get agent templates


# **agent_from_template_post**
> AgentFromTemplatePost200Response agent_from_template_post(create_agent_from_template_request)

Create agent from template

We have created templates for some common use cases. You can use these templates to create an agent. For getting list of templates, you can use the /agent/template endpoint. It will give you the list of templates with their description and id. You can pass the id of the template in the request body to create an agent from the template.

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import atoms
from atoms.models.agent_from_template_post200_response import AgentFromTemplatePost200Response
from atoms.models.create_agent_from_template_request import CreateAgentFromTemplateRequest
from atoms.rest import ApiException
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
    api_instance = atoms.AgentTemplatesApi(api_client)
    create_agent_from_template_request = atoms.CreateAgentFromTemplateRequest() # CreateAgentFromTemplateRequest | 

    try:
        # Create agent from template
        api_response = api_instance.agent_from_template_post(create_agent_from_template_request)
        print("The response of AgentTemplatesApi->agent_from_template_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentTemplatesApi->agent_from_template_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_agent_from_template_request** | [**CreateAgentFromTemplateRequest**](CreateAgentFromTemplateRequest.md)|  | 

### Return type

[**AgentFromTemplatePost200Response**](AgentFromTemplatePost200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **agent_template_get**
> AgentTemplateGet200Response agent_template_get()

Get agent templates

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import atoms
from atoms.models.agent_template_get200_response import AgentTemplateGet200Response
from atoms.rest import ApiException
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
    api_instance = atoms.AgentTemplatesApi(api_client)

    try:
        # Get agent templates
        api_response = api_instance.agent_template_get()
        print("The response of AgentTemplatesApi->agent_template_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentTemplatesApi->agent_template_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**AgentTemplateGet200Response**](AgentTemplateGet200Response.md)

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
**400** | Invalid input |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

