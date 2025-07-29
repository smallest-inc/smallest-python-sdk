# AgentTemplateGet200ResponseDataInner


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
from atoms.models.agent_template_get200_response_data_inner import AgentTemplateGet200ResponseDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of AgentTemplateGet200ResponseDataInner from a JSON string
agent_template_get200_response_data_inner_instance = AgentTemplateGet200ResponseDataInner.from_json(json)
# print the JSON string representation of the object
print(AgentTemplateGet200ResponseDataInner.to_json())

# convert the object into a dict
agent_template_get200_response_data_inner_dict = agent_template_get200_response_data_inner_instance.to_dict()
# create an instance of AgentTemplateGet200ResponseDataInner from a dict
agent_template_get200_response_data_inner_from_dict = AgentTemplateGet200ResponseDataInner.from_dict(agent_template_get200_response_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


