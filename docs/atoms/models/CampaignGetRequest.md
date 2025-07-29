# CampaignGetRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **float** | The page number | [optional] [default to 1]
**limit** | **float** | The number of items per page | [optional] [default to 10]

## Example

```python
from atoms.models.campaign_get_request import CampaignGetRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CampaignGetRequest from a JSON string
campaign_get_request_instance = CampaignGetRequest.from_json(json)
# print the JSON string representation of the object
print(CampaignGetRequest.to_json())

# convert the object into a dict
campaign_get_request_dict = campaign_get_request_instance.to_dict()
# create an instance of CampaignGetRequest from a dict
campaign_get_request_from_dict = CampaignGetRequest.from_dict(campaign_get_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


