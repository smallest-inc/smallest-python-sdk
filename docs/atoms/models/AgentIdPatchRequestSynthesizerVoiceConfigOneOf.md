# AgentIdPatchRequestSynthesizerVoiceConfigOneOf


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** | We currently support 3 types of models for the synthesizer. Waves, Waves Lightning Large and Waves Lightning Large Voice Clone. You can clone your voice using waves platform and use the voiceId for this field and select the model as waves_lightning_large_voice_clone to use your cloned voice. | [optional] 
**voice_id** | **str** |  | [optional] 
**gender** | **str** | The gender of the synthesizer. When selecting gender, you have to select the model and voiceId which are required fields. | [optional] 

## Example

```python
from atoms.models.agent_id_patch_request_synthesizer_voice_config_one_of import AgentIdPatchRequestSynthesizerVoiceConfigOneOf

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdPatchRequestSynthesizerVoiceConfigOneOf from a JSON string
agent_id_patch_request_synthesizer_voice_config_one_of_instance = AgentIdPatchRequestSynthesizerVoiceConfigOneOf.from_json(json)
# print the JSON string representation of the object
print(AgentIdPatchRequestSynthesizerVoiceConfigOneOf.to_json())

# convert the object into a dict
agent_id_patch_request_synthesizer_voice_config_one_of_dict = agent_id_patch_request_synthesizer_voice_config_one_of_instance.to_dict()
# create an instance of AgentIdPatchRequestSynthesizerVoiceConfigOneOf from a dict
agent_id_patch_request_synthesizer_voice_config_one_of_from_dict = AgentIdPatchRequestSynthesizerVoiceConfigOneOf.from_dict(agent_id_patch_request_synthesizer_voice_config_one_of_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


