# UpdateAgentRequestSynthesizerVoiceConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** | We currently support 3 types of models for the synthesizer. Waves, Waves Lightning Large and Waves Lightning Large Voice Clone. You can clone your voice using waves platform and use the voiceId for this field and select the model as waves_lightning_large_voice_clone to use your cloned voice. | [optional] 
**voice_id** | **str** | The voice ID to use | [optional] [default to 'nyah']
**gender** | **str** | The gender of the synthesizer. When selecting gender, you have to select the model and voiceId which are required fields. | [optional] 

## Example

```python
from smallestai.atoms.models.update_agent_request_synthesizer_voice_config import UpdateAgentRequestSynthesizerVoiceConfig

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAgentRequestSynthesizerVoiceConfig from a JSON string
update_agent_request_synthesizer_voice_config_instance = UpdateAgentRequestSynthesizerVoiceConfig.from_json(json)
# print the JSON string representation of the object
print(UpdateAgentRequestSynthesizerVoiceConfig.to_json())

# convert the object into a dict
update_agent_request_synthesizer_voice_config_dict = update_agent_request_synthesizer_voice_config_instance.to_dict()
# create an instance of UpdateAgentRequestSynthesizerVoiceConfig from a dict
update_agent_request_synthesizer_voice_config_from_dict = UpdateAgentRequestSynthesizerVoiceConfig.from_dict(update_agent_request_synthesizer_voice_config_dict)
```



