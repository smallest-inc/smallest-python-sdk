# AgentDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the agent | [optional] 
**name** | **str** | The name of the agent | [optional] 
**description** | **str** | The description of the agent | [optional] 
**organization** | **str** | The organization ID of the agent | [optional] 
**workflow_id** | **str** | The workflow ID of the agent | [optional] 
**created_by** | **str** | The user ID of the user who created the agent | [optional] 
**global_knowledge_base_id** | **str** | The global knowledge base ID of the agent | [optional] 
**language** | [**AgentDTOLanguage**](AgentDTOLanguage.md) |  | [optional] 
**synthesizer** | [**AgentDTOSynthesizer**](AgentDTOSynthesizer.md) |  | [optional] 
**slm_model** | **str** | The LLM model to use for the agent. LLM model will be used to generate the response and take decisions based on the user&#39;s query. | [optional] 
**default_variables** | **object** | The default variables to use for the agent. These variables will be used if no variables are provided when initiating a conversation with the agent. | [optional] 
**created_at** | **datetime** | The date and time when the agent was created | [optional] 
**updated_at** | **datetime** | The date and time when the agent was last updated | [optional] 

## Example

```python
from smallestai.atoms_client.models.agent_dto import AgentDTO

# TODO update the JSON string below
json = "{}"
# create an instance of AgentDTO from a JSON string
agent_dto_instance = AgentDTO.from_json(json)
# print the JSON string representation of the object
print(AgentDTO.to_json())

# convert the object into a dict
agent_dto_dict = agent_dto_instance.to_dict()
# create an instance of AgentDTO from a dict
agent_dto_from_dict = AgentDTO.from_dict(agent_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


