# GetCampaignById200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**GetCampaignById200ResponseData**](GetCampaignById200ResponseData.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_campaign_by_id200_response import GetCampaignById200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetCampaignById200Response from a JSON string
get_campaign_by_id200_response_instance = GetCampaignById200Response.from_json(json)
# print the JSON string representation of the object
print(GetCampaignById200Response.to_json())

# convert the object into a dict
get_campaign_by_id200_response_dict = get_campaign_by_id200_response_instance.to_dict()
# create an instance of GetCampaignById200Response from a dict
get_campaign_by_id200_response_from_dict = GetCampaignById200Response.from_dict(get_campaign_by_id200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


