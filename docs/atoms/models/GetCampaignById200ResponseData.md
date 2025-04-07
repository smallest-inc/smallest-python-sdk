# GetCampaignById200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the campaign | [optional] 
**name** | **str** | The name of the campaign | [optional] 
**description** | **str** | The description of the campaign | [optional] 
**organization** | **str** | The ID of the organization | [optional] 
**agent** | [**GetCampaigns200ResponseDataInnerAgent**](GetCampaigns200ResponseDataInnerAgent.md) |  | [optional] 
**created_by** | **str** | The ID of the user who created the campaign | [optional] 
**audience** | [**GetCampaigns200ResponseDataInnerAudience**](GetCampaigns200ResponseDataInnerAudience.md) |  | [optional] 
**participants_count** | **int** | The number of participants in the campaign | [optional] 
**created_at** | **datetime** | The date and time when the campaign was created | [optional] 
**updated_at** | **datetime** | The date and time when the campaign was last updated | [optional] 

## Example

```python
from smallestai.atoms.models.get_campaign_by_id200_response_data import GetCampaignById200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetCampaignById200ResponseData from a JSON string
get_campaign_by_id200_response_data_instance = GetCampaignById200ResponseData.from_json(json)
# print the JSON string representation of the object
print(GetCampaignById200ResponseData.to_json())

# convert the object into a dict
get_campaign_by_id200_response_data_dict = get_campaign_by_id200_response_data_instance.to_dict()
# create an instance of GetCampaignById200ResponseData from a dict
get_campaign_by_id200_response_data_from_dict = GetCampaignById200ResponseData.from_dict(get_campaign_by_id200_response_data_dict)
```



