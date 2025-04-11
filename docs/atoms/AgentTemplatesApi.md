# atoms.AgentTemplatesApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_agent_from_template**](AgentTemplatesApi.md#create_agent_from_template) | **POST** /agent/from-template | Create agent from template
[**get_agent_templates**](AgentTemplatesApi.md#get_agent_templates) | **GET** /agent/template | Get agent templates

# **create_agent_from_template**

Create a new agent using a predefined template.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    template_request = {
        "template_id": "your_template_id",
        "name": "My Template Agent"
    }
    
    response = atoms_client.create_agent_from_template(create_agent_from_template_request=template_request)
    print(f"Created agent with ID: {response}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**create_agent_from_template_request** | [**CreateAgentFromTemplateRequest**](./models/CreateAgentFromTemplateRequest.md) | Template configuration | 

### Return type

**str**

# **get_agent_templates**

Get a list of available agent templates.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    response = atoms_client.get_agent_templates()
    print(f"Available templates: {response}")

if __name__ == "__main__":
    main()
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**List[GetAgentTemplates200ResponseDataInner]**](./models/GetAgentTemplates200ResponseDataInner.md)

