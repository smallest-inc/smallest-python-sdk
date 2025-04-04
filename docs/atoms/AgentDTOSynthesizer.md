# AgentDTOSynthesizer

The synthesizer (TTS) configuration of the agent

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**voice_config** | [**AgentDTOSynthesizerVoiceConfig**](AgentDTOSynthesizerVoiceConfig.md) |  | [optional] 
**speed** | **float** |  | [optional] [default to 1.2]
**consistency** | **float** | The consistency of the synthesizer | [optional] [default to 0.5]
**similarity** | **float** | The similarity of the synthesizer | [optional] [default to 0]
**enhancement** | **float** | The enhancement of the synthesizer | [optional] [default to 1]

## Example

```python
from smallestai.atoms.models.agent_dto_synthesizer import AgentDTOSynthesizer

# TODO update the JSON string below
json = "{}"
# create an instance of AgentDTOSynthesizer from a JSON string
agent_dto_synthesizer_instance = AgentDTOSynthesizer.from_json(json)
# print the JSON string representation of the object
print(AgentDTOSynthesizer.to_json())

# convert the object into a dict
agent_dto_synthesizer_dict = agent_dto_synthesizer_instance.to_dict()
# create an instance of AgentDTOSynthesizer from a dict
agent_dto_synthesizer_from_dict = AgentDTOSynthesizer.from_dict(agent_dto_synthesizer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


