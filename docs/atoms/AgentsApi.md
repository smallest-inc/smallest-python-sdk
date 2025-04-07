# atoms.AgentsApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_agent**](AgentsApi.md#create_agent) | **POST** /agent | Create a new agent
[**delete_agent**](AgentsApi.md#delete_agent) | **DELETE** /agent/{id} | Delete an agent
[**get_agent_by_id**](AgentsApi.md#get_agent_by_id) | **GET** /agent/{id} | Get agent by ID
[**get_agents**](AgentsApi.md#get_agents) | **GET** /agent | Get all agents
[**update_agent**](AgentsApi.md#update_agent) | **PATCH** /agent/{id} | Update an agent


# **create_agent**
> CreateAgentFromTemplate200Response create_agent(create_agent_request)

Create a new agent

You can create a new agent by passing the name of the agent in the request body.

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.create_agent_from_template200_response import CreateAgentFromTemplate200Response
from smallestai.atoms.models.create_agent_request import CreateAgentRequest
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
    api_instance = atoms.AgentsApi(api_client)
    create_agent_request = atoms.CreateAgentRequest() # CreateAgentRequest | 

    try:
        # Create a new agent
        api_response = api_instance.create_agent(create_agent_request)
        print("The response of AgentsApi->create_agent:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentsApi->create_agent: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_agent_request** | [**CreateAgentRequest**](./models/CreateAgentRequest.md)|  | 

### Return type

[**CreateAgentFromTemplate200Response**](./models/CreateAgentFromTemplate200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Agent created successfully |  -  |
**400** | Invalid input |  -  |
**401** | Unauthorized access |  -  |
**500** | Internal server error |  -  |

[[Back to API list]](../../README.md#documentation-for-api-endpoints)

# **delete_agent**
> DeleteAgent200Response delete_agent(id)

Delete an agent

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
    api_instance = atoms.AgentsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Delete an agent
        api_response = api_instance.delete_agent(id)
        print("The response of AgentsApi->delete_agent:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentsApi->delete_agent: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**DeleteAgent200Response**](./models/DeleteAgent200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Agent deleted successfully |  -  |
**400** | Invalid input |  -  |
**401** | Access token is missing or invalid |  -  |
**403** | Forbidden access |  -  |

[[Back to API list]](../../README.md#documentation-for-api-endpoints)

# **get_agent_by_id**
> GetAgentById200Response get_agent_by_id(id)

Get agent by ID

Agents are the main entities in the system. Agents are used to create conversations. You can create workflow for an agent and configure it for different use cases. You can also create custom workflows for an agent.

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.get_agent_by_id200_response import GetAgentById200Response
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
    api_instance = atoms.AgentsApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get agent by ID
        api_response = api_instance.get_agent_by_id(id)
        print("The response of AgentsApi->get_agent_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentsApi->get_agent_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**GetAgentById200Response**](./models/GetAgentById200Response.md)

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

# **get_agents**
> GetAgents200Response get_agents(page=page, offset=offset, search=search)

Get all agents

Agents are the main entities in the system. Agents are used to create conversations. You can create workflow for an agent and configure it for different use cases. You can also create custom workflows for an agent. This API will give you the list of agents created by organization you are a part of.

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.get_agents200_response import GetAgents200Response
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
    api_instance = atoms.AgentsApi(api_client)
    page = 1 # int |  (optional) (default to 1)
    offset = 5 # int |  (optional) (default to 5)
    search = 'search_example' # str |  (optional)

    try:
        # Get all agents
        api_response = api_instance.get_agents(page=page, offset=offset, search=search)
        print("The response of AgentsApi->get_agents:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentsApi->get_agents: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**|  | [optional] [default to 1]
 **offset** | **int**|  | [optional] [default to 5]
 **search** | **str**|  | [optional] 

### Return type

[**GetAgents200Response**](./models/GetAgents200Response.md)

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

# **update_agent**
> UpdateAgent200Response update_agent(id, update_agent_request)

Update an agent

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import smallestai.atoms
from smallestai.atoms.models.update_agent200_response import UpdateAgent200Response
from smallestai.atoms.models.update_agent_request import UpdateAgentRequest
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
    api_instance = atoms.AgentsApi(api_client)
    id = 'id_example' # str | 
    update_agent_request = atoms.UpdateAgentRequest() # UpdateAgentRequest | 

    try:
        # Update an agent
        api_response = api_instance.update_agent(id, update_agent_request)
        print("The response of AgentsApi->update_agent:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentsApi->update_agent: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **update_agent_request** | [**UpdateAgentRequest**](./models/UpdateAgentRequest.md)|  | 

### Return type

[**UpdateAgent200Response**](./models/UpdateAgent200Response.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Agent updated successfully |  -  |
**400** | Invalid input |  -  |
**401** | Access token is missing or invalid |  -  |
**500** | Internal server error |  -  |

[[Back to API list]](../../README.md#documentation-for-api-endpoints)

