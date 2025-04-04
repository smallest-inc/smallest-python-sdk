# GetAgentTemplates200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**List[GetAgentTemplates200ResponseDataInner]**](GetAgentTemplates200ResponseDataInner.md) |  | [optional] 

## Example

```python
from smallestai.atoms_client.models.get_agent_templates200_response import GetAgentTemplates200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetAgentTemplates200Response from a JSON string
get_agent_templates200_response_instance = GetAgentTemplates200Response.from_json(json)
# print the JSON string representation of the object
print(GetAgentTemplates200Response.to_json())

# convert the object into a dict
get_agent_templates200_response_dict = get_agent_templates200_response_instance.to_dict()
# create an instance of GetAgentTemplates200Response from a dict
get_agent_templates200_response_from_dict = GetAgentTemplates200Response.from_dict(get_agent_templates200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


