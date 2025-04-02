# AgentDTOLanguage

The language configuration of the agent

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **str** | The language of the agent | [optional] 
**switching** | **bool** | Whether the agent can switch between languages | [optional] 
**supported** | **List[str]** | The supported languages of the agent | [optional] 

## Example

```python
from smallestai.atoms_client.models.agent_dto_language import AgentDTOLanguage

# TODO update the JSON string below
json = "{}"
# create an instance of AgentDTOLanguage from a JSON string
agent_dto_language_instance = AgentDTOLanguage.from_json(json)
# print the JSON string representation of the object
print(AgentDTOLanguage.to_json())

# convert the object into a dict
agent_dto_language_dict = agent_dto_language_instance.to_dict()
# create an instance of AgentDTOLanguage from a dict
agent_dto_language_from_dict = AgentDTOLanguage.from_dict(agent_dto_language_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


