# CampaignPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the campaign | 
**description** | **str** | The description of the campaign | [optional] 
**audience_id** | **str** | The ID of the audience | 
**agent_id** | **str** | The ID of the agent | 

## Example

```python
from atoms.models.campaign_post_request import CampaignPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CampaignPostRequest from a JSON string
campaign_post_request_instance = CampaignPostRequest.from_json(json)
# print the JSON string representation of the object
print(CampaignPostRequest.to_json())

# convert the object into a dict
campaign_post_request_dict = campaign_post_request_instance.to_dict()
# create an instance of CampaignPostRequest from a dict
campaign_post_request_from_dict = CampaignPostRequest.from_dict(campaign_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


