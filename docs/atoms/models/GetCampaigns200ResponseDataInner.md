# GetCampaigns200ResponseDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the campaign | 
**name** | **str** | The name of the campaign | 
**description** | **str** | The description of the campaign | [optional] 
**organization** | **str** | The ID of the organization | [optional] 
**agent** | [**GetCampaigns200ResponseDataInnerAgent**](GetCampaigns200ResponseDataInnerAgent.md) |  | [optional] 
**created_by** | **str** | The ID of the user who created the campaign | [optional] 
**audience** | [**GetCampaigns200ResponseDataInnerAudience**](GetCampaigns200ResponseDataInnerAudience.md) |  | [optional] 
**participants_count** | **int** | The number of participants in the campaign | [optional] 
**created_at** | **datetime** | The date and time when the campaign was created | [optional] 
**updated_at** | **datetime** | The date and time when the campaign was last updated | [optional] 
**is_campaign_in_progress** | **bool** | Whether the campaign is in progress | [optional] 
**is_campaign_completed** | **bool** | Whether the campaign is completed | [optional] 

## Example

```python
from smallestai.atoms.models.get_campaigns200_response_data_inner import GetCampaigns200ResponseDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetCampaigns200ResponseDataInner from a JSON string
get_campaigns200_response_data_inner_instance = GetCampaigns200ResponseDataInner.from_json(json)
# print the JSON string representation of the object
print(GetCampaigns200ResponseDataInner.to_json())

# convert the object into a dict
get_campaigns200_response_data_inner_dict = get_campaigns200_response_data_inner_instance.to_dict()
# create an instance of GetCampaigns200ResponseDataInner from a dict
get_campaigns200_response_data_inner_from_dict = GetCampaigns200ResponseDataInner.from_dict(get_campaigns200_response_data_inner_dict)
```



