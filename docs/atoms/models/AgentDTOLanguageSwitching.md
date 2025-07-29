# AgentDTOLanguageSwitching

Language switching configuration for the agent

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_enabled** | **bool** | Whether language switching is enabled for the agent | [optional] 
**min_words_for_detection** | **float** | Minimum number of words required for language detection | [optional] 
**strong_signal_threshold** | **float** | Threshold for strong language signal detection | [optional] 
**weak_signal_threshold** | **float** | Threshold for weak language signal detection | [optional] 
**min_consecutive_for_weak_threshold_switch** | **float** | Minimum consecutive detections required for weak threshold language switch | [optional] 

## Example

```python
from atoms.models.agent_dto_language_switching import AgentDTOLanguageSwitching

# TODO update the JSON string below
json = "{}"
# create an instance of AgentDTOLanguageSwitching from a JSON string
agent_dto_language_switching_instance = AgentDTOLanguageSwitching.from_json(json)
# print the JSON string representation of the object
print(AgentDTOLanguageSwitching.to_json())

# convert the object into a dict
agent_dto_language_switching_dict = agent_dto_language_switching_instance.to_dict()
# create an instance of AgentDTOLanguageSwitching from a dict
agent_dto_language_switching_from_dict = AgentDTOLanguageSwitching.from_dict(agent_dto_language_switching_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


