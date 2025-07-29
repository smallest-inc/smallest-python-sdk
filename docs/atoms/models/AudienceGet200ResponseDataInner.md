# AudienceGet200ResponseDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the audience | [optional] 
**name** | **str** | The name of the audience | [optional] 
**description** | **str** | The description of the audience | [optional] 
**phone_number_column_name** | **str** | The name of the column in the CSV that contains phone numbers | [optional] 
**organization** | **str** | The organization ID | [optional] 
**created_by** | **str** | The user ID who created the audience | [optional] 
**created_at** | **datetime** | The date and time when the audience was created | [optional] 
**updated_at** | **datetime** | The date and time when the audience was last updated | [optional] 

## Example

```python
from atoms.models.audience_get200_response_data_inner import AudienceGet200ResponseDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceGet200ResponseDataInner from a JSON string
audience_get200_response_data_inner_instance = AudienceGet200ResponseDataInner.from_json(json)
# print the JSON string representation of the object
print(AudienceGet200ResponseDataInner.to_json())

# convert the object into a dict
audience_get200_response_data_inner_dict = audience_get200_response_data_inner_instance.to_dict()
# create an instance of AudienceGet200ResponseDataInner from a dict
audience_get200_response_data_inner_from_dict = AudienceGet200ResponseDataInner.from_dict(audience_get200_response_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


