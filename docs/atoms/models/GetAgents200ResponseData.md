# GetAgents200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agents** | [**List[AgentDTO]**](AgentDTO.md) |  | [optional] 
**total_count** | **int** | Total number of agents | [optional] 
**has_more** | **bool** | Whether there are more agents to fetch | [optional] 
**is_search_results** | **bool** | Whether the results are from a search query | [optional] 

## Example

```python
from smallestai.atoms.models.get_agents200_response_data import GetAgents200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetAgents200ResponseData from a JSON string
get_agents200_response_data_instance = GetAgents200ResponseData.from_json(json)
# print the JSON string representation of the object
print(GetAgents200ResponseData.to_json())

# convert the object into a dict
get_agents200_response_data_dict = get_agents200_response_data_instance.to_dict()
# create an instance of GetAgents200ResponseData from a dict
get_agents200_response_data_from_dict = GetAgents200ResponseData.from_dict(get_agents200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


