# AgentIdWorkflowGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**AgentIdWorkflowGet200ResponseData**](AgentIdWorkflowGet200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.agent_id_workflow_get200_response import AgentIdWorkflowGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdWorkflowGet200Response from a JSON string
agent_id_workflow_get200_response_instance = AgentIdWorkflowGet200Response.from_json(json)
# print the JSON string representation of the object
print(AgentIdWorkflowGet200Response.to_json())

# convert the object into a dict
agent_id_workflow_get200_response_dict = agent_id_workflow_get200_response_instance.to_dict()
# create an instance of AgentIdWorkflowGet200Response from a dict
agent_id_workflow_get200_response_from_dict = AgentIdWorkflowGet200Response.from_dict(agent_id_workflow_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


