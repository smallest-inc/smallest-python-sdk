# UpdateAgentRequestSynthesizerVoiceConfigOneOf


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** | We currently support 3 types of models for the synthesizer. Waves, Waves Lightning Large and Waves Lightning Large Voice Clone. You can clone your voice using waves platform and use the voiceId for this field and select the model as waves_lightning_large_voice_clone to use your cloned voice. | [optional] 
**voice_id** | **str** |  | [optional] 
**gender** | **str** | The gender of the synthesizer. When selecting gender, you have to select the model and voiceId which are required fields. | [optional] 

## Example

```python
from smallestai.atoms.models.update_agent_request_synthesizer_voice_config_one_of import UpdateAgentRequestSynthesizerVoiceConfigOneOf

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAgentRequestSynthesizerVoiceConfigOneOf from a JSON string
update_agent_request_synthesizer_voice_config_one_of_instance = UpdateAgentRequestSynthesizerVoiceConfigOneOf.from_json(json)
# print the JSON string representation of the object
print(UpdateAgentRequestSynthesizerVoiceConfigOneOf.to_json())

# convert the object into a dict
update_agent_request_synthesizer_voice_config_one_of_dict = update_agent_request_synthesizer_voice_config_one_of_instance.to_dict()
# create an instance of UpdateAgentRequestSynthesizerVoiceConfigOneOf from a dict
update_agent_request_synthesizer_voice_config_one_of_from_dict = UpdateAgentRequestSynthesizerVoiceConfigOneOf.from_dict(update_agent_request_synthesizer_voice_config_one_of_dict)
```



