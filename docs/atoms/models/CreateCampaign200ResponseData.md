# CreateCampaign200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the campaign | [optional] 
**name** | **str** | The name of the campaign | [optional] 
**description** | **str** | The description of the campaign | [optional] 
**organization** | **str** | The ID of the organization | [optional] 
**agent_id** | **str** | The ID of the agent | [optional] 
**created_by** | **str** | The ID of the user who created the campaign | [optional] 
**audience_id** | **str** | The ID of the audience | [optional] 
**participants_count** | **int** | The number of participants in the campaign | [optional] 
**created_at** | **datetime** | The date and time when the campaign was created | [optional] 
**updated_at** | **datetime** | The date and time when the campaign was last updated | [optional] 

## Example

```python
from smallestai.atoms.models.create_campaign200_response_data import CreateCampaign200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCampaign200ResponseData from a JSON string
create_campaign200_response_data_instance = CreateCampaign200ResponseData.from_json(json)
# print the JSON string representation of the object
print(CreateCampaign200ResponseData.to_json())

# convert the object into a dict
create_campaign200_response_data_dict = create_campaign200_response_data_instance.to_dict()
# create an instance of CreateCampaign200ResponseData from a dict
create_campaign200_response_data_from_dict = CreateCampaign200ResponseData.from_dict(create_campaign200_response_data_dict)
```



