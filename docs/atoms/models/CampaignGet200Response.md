# CampaignGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**CampaignGet200ResponseData**](CampaignGet200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.campaign_get200_response import CampaignGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of CampaignGet200Response from a JSON string
campaign_get200_response_instance = CampaignGet200Response.from_json(json)
# print the JSON string representation of the object
print(CampaignGet200Response.to_json())

# convert the object into a dict
campaign_get200_response_dict = campaign_get200_response_instance.to_dict()
# create an instance of CampaignGet200Response from a dict
campaign_get200_response_from_dict = CampaignGet200Response.from_dict(campaign_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


