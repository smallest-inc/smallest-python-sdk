# CreateCampaignRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the campaign | 
**description** | **str** | The description of the campaign | [optional] 
**audience_id** | **str** | The ID of the audience | 
**agent_id** | **str** | The ID of the agent | 

## Example

```python
from smallestai.atoms.models.create_campaign_request import CreateCampaignRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCampaignRequest from a JSON string
create_campaign_request_instance = CreateCampaignRequest.from_json(json)
# print the JSON string representation of the object
print(CreateCampaignRequest.to_json())

# convert the object into a dict
create_campaign_request_dict = create_campaign_request_instance.to_dict()
# create an instance of CreateCampaignRequest from a dict
create_campaign_request_from_dict = CreateCampaignRequest.from_dict(create_campaign_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


