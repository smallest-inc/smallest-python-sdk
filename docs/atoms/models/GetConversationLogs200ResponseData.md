# GetConversationLogs200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the conversation | [optional] 
**call_id** | **str** | The ID of the conversation | [optional] 
**agent** | [**AgentDTO**](AgentDTO.md) |  | [optional] 
**status** | **str** | The status of the conversation | [optional] 
**duration** | **float** | The duration of the conversation in seconds | [optional] 
**recording_url** | **str** | The recording URL of the conversation | [optional] 
**var_from** | **str** | The phone number of the caller | [optional] 
**to** | **str** | The phone number of the callee | [optional] 
**transcript** | **List[str]** | The transcript of the conversation | [optional] 
**average_transcriber_latency** | **float** | The average time taken by the TTS to transcribe the conversation | [optional] 
**average_agent_latency** | **float** | The average time taken by the LLM to respond to the conversation | [optional] 
**average_synthesizer_latency** | **float** | The average time taken by the TTS to synthesize the conversation | [optional] 
**type** | **str** | The type of the conversation | [optional] 

## Example

```python
from smallestai.atoms.models.get_conversation_logs200_response_data import GetConversationLogs200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetConversationLogs200ResponseData from a JSON string
get_conversation_logs200_response_data_instance = GetConversationLogs200ResponseData.from_json(json)
# print the JSON string representation of the object
print(GetConversationLogs200ResponseData.to_json())

# convert the object into a dict
get_conversation_logs200_response_data_dict = get_conversation_logs200_response_data_instance.to_dict()
# create an instance of GetConversationLogs200ResponseData from a dict
get_conversation_logs200_response_data_from_dict = GetConversationLogs200ResponseData.from_dict(get_conversation_logs200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


