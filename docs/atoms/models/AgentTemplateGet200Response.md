# AgentTemplateGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**List[AgentTemplateGet200ResponseDataInner]**](AgentTemplateGet200ResponseDataInner.md) |  | [optional] 

## Example

```python
from atoms.models.agent_template_get200_response import AgentTemplateGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AgentTemplateGet200Response from a JSON string
agent_template_get200_response_instance = AgentTemplateGet200Response.from_json(json)
# print the JSON string representation of the object
print(AgentTemplateGet200Response.to_json())

# convert the object into a dict
agent_template_get200_response_dict = agent_template_get200_response_instance.to_dict()
# create an instance of AgentTemplateGet200Response from a dict
agent_template_get200_response_from_dict = AgentTemplateGet200Response.from_dict(agent_template_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


