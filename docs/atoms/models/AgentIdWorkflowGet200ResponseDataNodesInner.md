# AgentIdWorkflowGet200ResponseDataNodesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier for the node | [optional] 
**type** | **str** | Type of the node (e.g., default_node, end_call, pre_call_api) | [optional] 
**position** | [**AgentIdWorkflowGet200ResponseDataNodesInnerPosition**](AgentIdWorkflowGet200ResponseDataNodesInnerPosition.md) |  | [optional] 
**position_absolute** | [**AgentIdWorkflowGet200ResponseDataNodesInnerPosition**](AgentIdWorkflowGet200ResponseDataNodesInnerPosition.md) |  | [optional] 
**data** | [**AgentIdWorkflowGet200ResponseDataNodesInnerData**](AgentIdWorkflowGet200ResponseDataNodesInnerData.md) |  | [optional] 
**width** | **float** |  | [optional] 
**height** | **float** |  | [optional] 
**selected** | **bool** |  | [optional] 
**dragging** | **bool** |  | [optional] 

## Example

```python
from atoms.models.agent_id_workflow_get200_response_data_nodes_inner import AgentIdWorkflowGet200ResponseDataNodesInner

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdWorkflowGet200ResponseDataNodesInner from a JSON string
agent_id_workflow_get200_response_data_nodes_inner_instance = AgentIdWorkflowGet200ResponseDataNodesInner.from_json(json)
# print the JSON string representation of the object
print(AgentIdWorkflowGet200ResponseDataNodesInner.to_json())

# convert the object into a dict
agent_id_workflow_get200_response_data_nodes_inner_dict = agent_id_workflow_get200_response_data_nodes_inner_instance.to_dict()
# create an instance of AgentIdWorkflowGet200ResponseDataNodesInner from a dict
agent_id_workflow_get200_response_data_nodes_inner_from_dict = AgentIdWorkflowGet200ResponseDataNodesInner.from_dict(agent_id_workflow_get200_response_data_nodes_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


