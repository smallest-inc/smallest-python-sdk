# AgentDTOSynthesizerVoiceConfig

The voice configuration of the synthesizer

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | **str** | The model of the synthesizer | [optional] [default to 'waves_lightning_large']
**voice_id** | **str** | The voice ID of the synthesizer. | [optional] [default to 'nyah']
**gender** | **str** |  | [optional] [default to 'female']

## Example

```python
from smallestai.atoms.models.agent_dto_synthesizer_voice_config import AgentDTOSynthesizerVoiceConfig

# TODO update the JSON string below
json = "{}"
# create an instance of AgentDTOSynthesizerVoiceConfig from a JSON string
agent_dto_synthesizer_voice_config_instance = AgentDTOSynthesizerVoiceConfig.from_json(json)
# print the JSON string representation of the object
print(AgentDTOSynthesizerVoiceConfig.to_json())

# convert the object into a dict
agent_dto_synthesizer_voice_config_dict = agent_dto_synthesizer_voice_config_instance.to_dict()
# create an instance of AgentDTOSynthesizerVoiceConfig from a dict
agent_dto_synthesizer_voice_config_from_dict = AgentDTOSynthesizerVoiceConfig.from_dict(agent_dto_synthesizer_voice_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


