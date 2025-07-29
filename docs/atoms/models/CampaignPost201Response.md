# CampaignPost201Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | **object** |  | [optional] 

## Example

```python
from atoms.models.campaign_post201_response import CampaignPost201Response

# TODO update the JSON string below
json = "{}"
# create an instance of CampaignPost201Response from a JSON string
campaign_post201_response_instance = CampaignPost201Response.from_json(json)
# print the JSON string representation of the object
print(CampaignPost201Response.to_json())

# convert the object into a dict
campaign_post201_response_dict = campaign_post201_response_instance.to_dict()
# create an instance of CampaignPost201Response from a dict
campaign_post201_response_from_dict = CampaignPost201Response.from_dict(campaign_post201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


