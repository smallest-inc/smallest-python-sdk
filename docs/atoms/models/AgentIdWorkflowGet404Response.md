# AgentIdWorkflowGet404Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**errors** | **List[str]** |  | [optional] 

## Example

```python
from atoms.models.agent_id_workflow_get404_response import AgentIdWorkflowGet404Response

# TODO update the JSON string below
json = "{}"
# create an instance of AgentIdWorkflowGet404Response from a JSON string
agent_id_workflow_get404_response_instance = AgentIdWorkflowGet404Response.from_json(json)
# print the JSON string representation of the object
print(AgentIdWorkflowGet404Response.to_json())

# convert the object into a dict
agent_id_workflow_get404_response_dict = agent_id_workflow_get404_response_instance.to_dict()
# create an instance of AgentIdWorkflowGet404Response from a dict
agent_id_workflow_get404_response_from_dict = AgentIdWorkflowGet404Response.from_dict(agent_id_workflow_get404_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


