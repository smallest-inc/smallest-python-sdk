# UpdateAgentRequestSynthesizer

Synthesizer configuration for the agent. You can configure the synthesizer to use different voices and models. Currently we support 3 types of models for the synthesizer. Waves, Waves Lightning Large and Waves Lightning Large Voice Clone. You can clone your voice using waves platform https://waves.smallest.ai/voice-clone and use the voiceId for this field and select the model as waves_lightning_large_voice_clone to use your cloned voice. When updating the synthesizer configuration to voice clone model, you have to provide model and voiceId and gender all are required fields but when selecting the model as waves or waves and waves_lightning_large, you have to provide only model field and voiceId.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**voice_config** | [**UpdateAgentRequestSynthesizerVoiceConfig**](UpdateAgentRequestSynthesizerVoiceConfig.md) |  | [optional] 
**speed** | **float** |  | [optional] [default to 1.2]
**consistency** | **float** |  | [optional] [default to 0.5]
**similarity** | **float** |  | [optional] [default to 0]
**enhancement** | **float** |  | [optional] [default to 1]

## Example

```python
from smallestai.atoms_client.models.update_agent_request_synthesizer import UpdateAgentRequestSynthesizer

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAgentRequestSynthesizer from a JSON string
update_agent_request_synthesizer_instance = UpdateAgentRequestSynthesizer.from_json(json)
# print the JSON string representation of the object
print(UpdateAgentRequestSynthesizer.to_json())

# convert the object into a dict
update_agent_request_synthesizer_dict = update_agent_request_synthesizer_instance.to_dict()
# create an instance of UpdateAgentRequestSynthesizer from a dict
update_agent_request_synthesizer_from_dict = UpdateAgentRequestSynthesizer.from_dict(update_agent_request_synthesizer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


