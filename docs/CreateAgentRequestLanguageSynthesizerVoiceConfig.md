# CreateAgentRequestLanguageSynthesizerVoiceConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** | We currently support 3 types of models for the synthesizer. Waves, Waves Lightning Large and Waves Lightning Large Voice Clone. You can clone your voice using waves platform and use the voiceId for this field and select the model as waves_lightning_large_voice_clone to use your cloned voice. | [optional] 
**voice_id** | **str** | The voice ID to use | [optional] [default to 'nyah']
**gender** | **str** | The gender of the synthesizer. When selecting gender, you have to select the model and voiceId which are required fields. | [optional] 

## Example

```python
from smallestai.atoms_client.models.create_agent_request_language_synthesizer_voice_config import CreateAgentRequestLanguageSynthesizerVoiceConfig

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAgentRequestLanguageSynthesizerVoiceConfig from a JSON string
create_agent_request_language_synthesizer_voice_config_instance = CreateAgentRequestLanguageSynthesizerVoiceConfig.from_json(json)
# print the JSON string representation of the object
print(CreateAgentRequestLanguageSynthesizerVoiceConfig.to_json())

# convert the object into a dict
create_agent_request_language_synthesizer_voice_config_dict = create_agent_request_language_synthesizer_voice_config_instance.to_dict()
# create an instance of CreateAgentRequestLanguageSynthesizerVoiceConfig from a dict
create_agent_request_language_synthesizer_voice_config_from_dict = CreateAgentRequestLanguageSynthesizerVoiceConfig.from_dict(create_agent_request_language_synthesizer_voice_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


