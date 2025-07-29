# CreateAgentFromTemplateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_name** | **str** | Name of the agent | 
**agent_description** | **str** | Description of the agent | [optional] 
**template_id** | **str** | ID of the template to use. You can get the list of templates with their description and id from the /agent/template endpoint. | 

## Example

```python
from atoms.models.create_agent_from_template_request import CreateAgentFromTemplateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAgentFromTemplateRequest from a JSON string
create_agent_from_template_request_instance = CreateAgentFromTemplateRequest.from_json(json)
# print the JSON string representation of the object
print(CreateAgentFromTemplateRequest.to_json())

# convert the object into a dict
create_agent_from_template_request_dict = create_agent_from_template_request_instance.to_dict()
# create an instance of CreateAgentFromTemplateRequest from a dict
create_agent_from_template_request_from_dict = CreateAgentFromTemplateRequest.from_dict(create_agent_from_template_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


