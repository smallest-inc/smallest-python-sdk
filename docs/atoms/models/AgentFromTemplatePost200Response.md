# AgentFromTemplatePost200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | **str** | The ID of the created agent | [optional] 

## Example

```python
from atoms.models.agent_from_template_post200_response import AgentFromTemplatePost200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AgentFromTemplatePost200Response from a JSON string
agent_from_template_post200_response_instance = AgentFromTemplatePost200Response.from_json(json)
# print the JSON string representation of the object
print(AgentFromTemplatePost200Response.to_json())

# convert the object into a dict
agent_from_template_post200_response_dict = agent_from_template_post200_response_instance.to_dict()
# create an instance of AgentFromTemplatePost200Response from a dict
agent_from_template_post200_response_from_dict = AgentFromTemplatePost200Response.from_dict(agent_from_template_post200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


