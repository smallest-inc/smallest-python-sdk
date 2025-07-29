# AudienceIdMembersGet200ResponseDataMembersInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the audience member | [optional] 
**data** | **object** | Dynamic data from CSV, structure depends on uploaded file | [optional] 

## Example

```python
from atoms.models.audience_id_members_get200_response_data_members_inner import AudienceIdMembersGet200ResponseDataMembersInner

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersGet200ResponseDataMembersInner from a JSON string
audience_id_members_get200_response_data_members_inner_instance = AudienceIdMembersGet200ResponseDataMembersInner.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersGet200ResponseDataMembersInner.to_json())

# convert the object into a dict
audience_id_members_get200_response_data_members_inner_dict = audience_id_members_get200_response_data_members_inner_instance.to_dict()
# create an instance of AudienceIdMembersGet200ResponseDataMembersInner from a dict
audience_id_members_get200_response_data_members_inner_from_dict = AudienceIdMembersGet200ResponseDataMembersInner.from_dict(audience_id_members_get200_response_data_members_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


