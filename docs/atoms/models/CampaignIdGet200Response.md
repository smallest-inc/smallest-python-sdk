# CampaignIdGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**CampaignIdGet200ResponseData**](CampaignIdGet200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.campaign_id_get200_response import CampaignIdGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of CampaignIdGet200Response from a JSON string
campaign_id_get200_response_instance = CampaignIdGet200Response.from_json(json)
# print the JSON string representation of the object
print(CampaignIdGet200Response.to_json())

# convert the object into a dict
campaign_id_get200_response_dict = campaign_id_get200_response_instance.to_dict()
# create an instance of CampaignIdGet200Response from a dict
campaign_id_get200_response_from_dict = CampaignIdGet200Response.from_dict(campaign_id_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


