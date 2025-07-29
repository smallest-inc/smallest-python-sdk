# AgentIdPatchRequestLanguage

Language configuration for the agent. You can enable or disable language switching for the agent. This will be used to determine the language of the agent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **str** | The language of the agent. You can choose from the list of supported languages. | [optional] [default to 'en']
**switching** | [**AgentIdPatchRequestLanguageSwitching**](AgentIdPatchRequestLanguageSwitching.md) |  | [optional] 

## Example

```python
from atoms.models.agent_id_patch_request_language import AgentIdPatchRequestLanguage

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdPatchRequestLanguage from a JSON string
agent_id_patch_request_language_instance = AgentIdPatchRequestLanguage.from_json(json)
# print the JSON string representation of the object
print(AgentIdPatchRequestLanguage.to_json())

# convert the object into a dict
agent_id_patch_request_language_dict = agent_id_patch_request_language_instance.to_dict()
# create an instance of AgentIdPatchRequestLanguage from a dict
agent_id_patch_request_language_from_dict = AgentIdPatchRequestLanguage.from_dict(agent_id_patch_request_language_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


