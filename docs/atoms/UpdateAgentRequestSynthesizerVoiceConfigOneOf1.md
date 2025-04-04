# UpdateAgentRequestSynthesizerVoiceConfigOneOf1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** | We currently support 3 types of models for the synthesizer. Waves, Waves Lightning Large and Waves Lightning Large Voice Clone. You can clone your voice using waves platform and use the voiceId for this field and select the model as waves_lightning_large_voice_clone to use your cloned voice. | [optional] 
**voice_id** | **str** | The voice ID to use | [optional] [default to 'nyah']

## Example

```python
from smallestai.atoms_client.models.update_agent_request_synthesizer_voice_config_one_of1 import UpdateAgentRequestSynthesizerVoiceConfigOneOf1

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAgentRequestSynthesizerVoiceConfigOneOf1 from a JSON string
update_agent_request_synthesizer_voice_config_one_of1_instance = UpdateAgentRequestSynthesizerVoiceConfigOneOf1.from_json(json)
# print the JSON string representation of the object
print(UpdateAgentRequestSynthesizerVoiceConfigOneOf1.to_json())

# convert the object into a dict
update_agent_request_synthesizer_voice_config_one_of1_dict = update_agent_request_synthesizer_voice_config_one_of1_instance.to_dict()
# create an instance of UpdateAgentRequestSynthesizerVoiceConfigOneOf1 from a dict
update_agent_request_synthesizer_voice_config_one_of1_from_dict = UpdateAgentRequestSynthesizerVoiceConfigOneOf1.from_dict(update_agent_request_synthesizer_voice_config_one_of1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


