# CreateAgentFromTemplate200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | **str** | The ID of the created agent | [optional] 

## Example

```python
from smallestai.atoms_client.models.create_agent_from_template200_response import CreateAgentFromTemplate200Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAgentFromTemplate200Response from a JSON string
create_agent_from_template200_response_instance = CreateAgentFromTemplate200Response.from_json(json)
# print the JSON string representation of the object
print(CreateAgentFromTemplate200Response.to_json())

# convert the object into a dict
create_agent_from_template200_response_dict = create_agent_from_template200_response_instance.to_dict()
# create an instance of CreateAgentFromTemplate200Response from a dict
create_agent_from_template200_response_from_dict = CreateAgentFromTemplate200Response.from_dict(create_agent_from_template200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


