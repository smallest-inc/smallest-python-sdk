# GetAgentById200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**AgentDTO**](AgentDTO.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_agent_by_id200_response import GetAgentById200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetAgentById200Response from a JSON string
get_agent_by_id200_response_instance = GetAgentById200Response.from_json(json)
# print the JSON string representation of the object
print(GetAgentById200Response.to_json())

# convert the object into a dict
get_agent_by_id200_response_dict = get_agent_by_id200_response_instance.to_dict()
# create an instance of GetAgentById200Response from a dict
get_agent_by_id200_response_from_dict = GetAgentById200Response.from_dict(get_agent_by_id200_response_dict)
```



