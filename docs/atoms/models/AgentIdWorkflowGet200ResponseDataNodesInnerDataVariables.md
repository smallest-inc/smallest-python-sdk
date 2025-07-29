# AgentIdWorkflowGet200ResponseDataNodesInnerDataVariables

Variables configuration

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_enabled** | **bool** |  | [optional] 
**data** | [**List[AgentIdWorkflowGet200ResponseDataNodesInnerDataVariablesDataInner]**](AgentIdWorkflowGet200ResponseDataNodesInnerDataVariablesDataInner.md) |  | [optional] 

## Example

```python
from atoms.models.agent_id_workflow_get200_response_data_nodes_inner_data_variables import AgentIdWorkflowGet200ResponseDataNodesInnerDataVariables

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdWorkflowGet200ResponseDataNodesInnerDataVariables from a JSON string
agent_id_workflow_get200_response_data_nodes_inner_data_variables_instance = AgentIdWorkflowGet200ResponseDataNodesInnerDataVariables.from_json(json)
# print the JSON string representation of the object
print(AgentIdWorkflowGet200ResponseDataNodesInnerDataVariables.to_json())

# convert the object into a dict
agent_id_workflow_get200_response_data_nodes_inner_data_variables_dict = agent_id_workflow_get200_response_data_nodes_inner_data_variables_instance.to_dict()
# create an instance of AgentIdWorkflowGet200ResponseDataNodesInnerDataVariables from a dict
agent_id_workflow_get200_response_data_nodes_inner_data_variables_from_dict = AgentIdWorkflowGet200ResponseDataNodesInnerDataVariables.from_dict(agent_id_workflow_get200_response_data_nodes_inner_data_variables_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


