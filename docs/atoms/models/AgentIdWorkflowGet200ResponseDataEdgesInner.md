# AgentIdWorkflowGet200ResponseDataEdgesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier for the edge | [optional] 
**source** | **str** | ID of the source node | [optional] 
**source_handle** | **str** | Source handle ID | [optional] 
**target** | **str** | ID of the target node | [optional] 
**target_handle** | **str** | Target handle ID | [optional] 
**type** | **str** | Type of the edge (e.g., smoothstep, direct) | [optional] 
**label** | **str** | Label for the edge | [optional] 
**description** | **str** | Description of the edge | [optional] 
**selected** | **bool** |  | [optional] 
**animated** | **bool** |  | [optional] 
**marker_end** | [**AgentIdWorkflowGet200ResponseDataEdgesInnerMarkerEnd**](AgentIdWorkflowGet200ResponseDataEdgesInnerMarkerEnd.md) |  | [optional] 
**data** | [**AgentIdWorkflowGet200ResponseDataEdgesInnerData**](AgentIdWorkflowGet200ResponseDataEdgesInnerData.md) |  | [optional] 

## Example

```python
from atoms.models.agent_id_workflow_get200_response_data_edges_inner import AgentIdWorkflowGet200ResponseDataEdgesInner

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdWorkflowGet200ResponseDataEdgesInner from a JSON string
agent_id_workflow_get200_response_data_edges_inner_instance = AgentIdWorkflowGet200ResponseDataEdgesInner.from_json(json)
# print the JSON string representation of the object
print(AgentIdWorkflowGet200ResponseDataEdgesInner.to_json())

# convert the object into a dict
agent_id_workflow_get200_response_data_edges_inner_dict = agent_id_workflow_get200_response_data_edges_inner_instance.to_dict()
# create an instance of AgentIdWorkflowGet200ResponseDataEdgesInner from a dict
agent_id_workflow_get200_response_data_edges_inner_from_dict = AgentIdWorkflowGet200ResponseDataEdgesInner.from_dict(agent_id_workflow_get200_response_data_edges_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


