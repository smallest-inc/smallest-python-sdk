# AudiencePost200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the audience | [optional] 
**name** | **str** | The name of the audience | [optional] 
**description** | **str** | The description of the audience | [optional] 
**phone_number_column_name** | **str** | The name of the column in the CSV that contains phone numbers | [optional] 
**identifier_column_name** | **str** | The name of the column in the CSV that contains identifiers | [optional] 
**organization** | **str** | The organization ID | [optional] 
**created_by** | **str** | The user ID who created the audience | [optional] 
**created_at** | **datetime** | The date and time when the audience was created | [optional] 
**updated_at** | **datetime** | The date and time when the audience was last updated | [optional] 

## Example

```python
from atoms.models.audience_post200_response_data import AudiencePost200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of AudiencePost200ResponseData from a JSON string
audience_post200_response_data_instance = AudiencePost200ResponseData.from_json(json)
# print the JSON string representation of the object
print(AudiencePost200ResponseData.to_json())

# convert the object into a dict
audience_post200_response_data_dict = audience_post200_response_data_instance.to_dict()
# create an instance of AudiencePost200ResponseData from a dict
audience_post200_response_data_from_dict = AudiencePost200ResponseData.from_dict(audience_post200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


