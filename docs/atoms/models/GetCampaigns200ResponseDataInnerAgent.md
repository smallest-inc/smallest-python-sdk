# GetCampaigns200ResponseDataInnerAgent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the agent | [optional] 
**name** | **str** | The name of the agent | [optional] 

## Example

```python
from smallestai.atoms.models.get_campaigns200_response_data_inner_agent import GetCampaigns200ResponseDataInnerAgent

# TODO update the JSON string below
json = "{}"
# create an instance of GetCampaigns200ResponseDataInnerAgent from a JSON string
get_campaigns200_response_data_inner_agent_instance = GetCampaigns200ResponseDataInnerAgent.from_json(json)
# print the JSON string representation of the object
print(GetCampaigns200ResponseDataInnerAgent.to_json())

# convert the object into a dict
get_campaigns200_response_data_inner_agent_dict = get_campaigns200_response_data_inner_agent_instance.to_dict()
# create an instance of GetCampaigns200ResponseDataInnerAgent from a dict
get_campaigns200_response_data_inner_agent_from_dict = GetCampaigns200ResponseDataInnerAgent.from_dict(get_campaigns200_response_data_inner_agent_dict)
```



