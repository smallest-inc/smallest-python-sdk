# AgentIdPatchRequestLanguageSwitching

Language switching configuration for the agent. If enabled, the agent will be able to switch between languages based on the user's language.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_enabled** | **bool** | Whether to enable language switching for the agent | [optional] [default to False]
**min_words_for_detection** | **float** | Minimum number of words required for language detection | [optional] [default to 2]
**strong_signal_threshold** | **float** | Threshold for strong language signal detection (0.1 to 0.9) | [optional] [default to 0.7]
**weak_signal_threshold** | **float** | Threshold for weak language signal detection (0.1 to 0.9) | [optional] [default to 0.3]
**min_consecutive_for_weak_threshold_switch** | **float** | Minimum consecutive detections required for weak threshold language switch | [optional] [default to 2]

## Example

```python
from atoms.models.agent_id_patch_request_language_switching import AgentIdPatchRequestLanguageSwitching

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdPatchRequestLanguageSwitching from a JSON string
agent_id_patch_request_language_switching_instance = AgentIdPatchRequestLanguageSwitching.from_json(json)
# print the JSON string representation of the object
print(AgentIdPatchRequestLanguageSwitching.to_json())

# convert the object into a dict
agent_id_patch_request_language_switching_dict = agent_id_patch_request_language_switching_instance.to_dict()
# create an instance of AgentIdPatchRequestLanguageSwitching from a dict
agent_id_patch_request_language_switching_from_dict = AgentIdPatchRequestLanguageSwitching.from_dict(agent_id_patch_request_language_switching_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


