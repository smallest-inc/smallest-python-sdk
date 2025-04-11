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

Create a new agent by providing the agent configuration.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    new_agent_request = {
        "name": "Test Agent",
        "description": "Test agent description",
        "language": {
            "enabled": "en",
            "switching": False
        },
        "synthesizer": {
            "voiceConfig": {
                "model": "waves_lightning_large",
                "voiceId": "nyah"
            },
            "speed": 1.2,
            "consistency": 0.5,
            "similarity": 0,
            "enhancement": 1
        },
        "slmModel": "electron-v1"
    }
    
    response = atoms_client.create_agent(create_agent_request=new_agent_request)
    print(f"Created agent with ID: {response}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**create_agent_request** | [**CreateAgentRequest**](./models/CreateAgentRequest.md) | Agent configuration | 

### Return type

**str**

# **delete_agent**

Delete an existing agent by ID.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    agent_id = "your_agent_id"
    response = atoms_client.delete_agent(id=agent_id)
    print(f"Agent deletion status: {response}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Agent ID to delete | 

### Return type

**bool**

# **get_agent_by_id**

Get details of a specific agent by ID.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    agent_id = "your_agent_id"
    response = atoms_client.get_agent_by_id(id=agent_id)
    print(f"Agent details: {response}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Agent ID to retrieve | 

### Return type

[**AgentDTO**](./models/AgentDTO.md)

# **get_agents**

Get a list of all agents.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    # Optional parameters for pagination and search
    response = atoms_client.get_agents(
        page=1,      # optional, default=1
        offset=5,    # optional, default=5
        search=None  # optional search term
    )
    print(f"Retrieved agents: {response}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**page** | **int** | Page number | [optional] [default to 1]
**offset** | **int** | Number of items per page | [optional] [default to 5]
**search** | **str** | Search term | [optional]

### Return type

[**GetAgents200ResponseData**](./models/GetAgents200ResponseData.md)

# **update_agent**

Update an existing agent's configuration.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    agent_id = "your_agent_id"
    update_request = {
        "name": "Updated Test Agent"
        # Add other fields to update as needed
    }
    
    response = atoms_client.update_agent(
        id=agent_id,
        update_agent_request=update_request
    )
    print(f"Agent update status: {response}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Agent ID to update | 
**update_agent_request** | [**UpdateAgentRequest**](./models/UpdateAgentRequest.md) | Updated agent configuration | 

### Return type

**bool**

