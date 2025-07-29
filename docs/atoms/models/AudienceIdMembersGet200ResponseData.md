# AudienceIdMembersGet200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**members** | [**List[AudienceIdMembersGet200ResponseDataMembersInner]**](AudienceIdMembersGet200ResponseDataMembersInner.md) |  | [optional] 
**total_count** | **int** | Total number of members in the audience | [optional] 
**total_pages** | **int** | Total number of pages available | [optional] 
**has_more** | **bool** | Whether there are more pages available | [optional] 

## Example

```python
from atoms.models.audience_id_members_get200_response_data import AudienceIdMembersGet200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersGet200ResponseData from a JSON string
audience_id_members_get200_response_data_instance = AudienceIdMembersGet200ResponseData.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersGet200ResponseData.to_json())

# convert the object into a dict
audience_id_members_get200_response_data_dict = audience_id_members_get200_response_data_instance.to_dict()
# create an instance of AudienceIdMembersGet200ResponseData from a dict
audience_id_members_get200_response_data_from_dict = AudienceIdMembersGet200ResponseData.from_dict(audience_id_members_get200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


