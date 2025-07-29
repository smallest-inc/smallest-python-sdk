# AgentIdWorkflowGet200ResponseDataNodesInnerData

Node-specific data and configuration

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** | Display label for the node | [optional] 
**action** | **str** | The action/prompt text for the node | [optional] 
**is_start_node** | **bool** | Whether this is the starting node | [optional] 
**static_text** | **bool** | Whether the text is static | [optional] 
**knowledge_base** | **str** | Knowledge base ID for the node | [optional] 
**use_global_knowledge_base** | **bool** | Whether to use global knowledge base | [optional] 
**is_disconnected** | **bool** | Whether the node is disconnected | [optional] 
**type** | **str** | Node type | [optional] 
**variables** | [**AgentIdWorkflowGet200ResponseDataNodesInnerDataVariables**](AgentIdWorkflowGet200ResponseDataNodesInnerDataVariables.md) |  | [optional] 
**has_error** | **bool** |  | [optional] 
**validation_errors** | **List[str]** |  | [optional] 
**http_request** | **object** | HTTP request configuration (for pre_call_api nodes) | [optional] 
**response_data** | **object** | Response data configuration (for pre_call_api nodes) | [optional] 

## Example

```python
from atoms.models.agent_id_workflow_get200_response_data_nodes_inner_data import AgentIdWorkflowGet200ResponseDataNodesInnerData

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdWorkflowGet200ResponseDataNodesInnerData from a JSON string
agent_id_workflow_get200_response_data_nodes_inner_data_instance = AgentIdWorkflowGet200ResponseDataNodesInnerData.from_json(json)
# print the JSON string representation of the object
print(AgentIdWorkflowGet200ResponseDataNodesInnerData.to_json())

# convert the object into a dict
agent_id_workflow_get200_response_data_nodes_inner_data_dict = agent_id_workflow_get200_response_data_nodes_inner_data_instance.to_dict()
# create an instance of AgentIdWorkflowGet200ResponseDataNodesInnerData from a dict
agent_id_workflow_get200_response_data_nodes_inner_data_from_dict = AgentIdWorkflowGet200ResponseDataNodesInnerData.from_dict(agent_id_workflow_get200_response_data_nodes_inner_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


