# GetAgentTemplates200ResponseDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the agent template | [optional] 
**name** | **str** | The name of the agent template | [optional] 
**description** | **str** | The description of the agent template | [optional] 
**avatar_url** | **str** | The avatar URL of the agent template | [optional] 
**reference_url** | **str** | The docs url of the agent template | [optional] 
**category** | **str** | The category of the agent template | [optional] 

## Example

```python
from smallestai.atoms_client.models.get_agent_templates200_response_data_inner import GetAgentTemplates200ResponseDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetAgentTemplates200ResponseDataInner from a JSON string
get_agent_templates200_response_data_inner_instance = GetAgentTemplates200ResponseDataInner.from_json(json)
# print the JSON string representation of the object
print(GetAgentTemplates200ResponseDataInner.to_json())

# convert the object into a dict
get_agent_templates200_response_data_inner_dict = get_agent_templates200_response_data_inner_instance.to_dict()
# create an instance of GetAgentTemplates200ResponseDataInner from a dict
get_agent_templates200_response_data_inner_from_dict = GetAgentTemplates200ResponseDataInner.from_dict(get_agent_templates200_response_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


