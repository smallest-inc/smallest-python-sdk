# AudienceIdMembersDelete200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**deleted_count** | **int** | Number of members successfully deleted | [optional] 

## Example

```python
from atoms.models.audience_id_members_delete200_response_data import AudienceIdMembersDelete200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersDelete200ResponseData from a JSON string
audience_id_members_delete200_response_data_instance = AudienceIdMembersDelete200ResponseData.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersDelete200ResponseData.to_json())

# convert the object into a dict
audience_id_members_delete200_response_data_dict = audience_id_members_delete200_response_data_instance.to_dict()
# create an instance of AudienceIdMembersDelete200ResponseData from a dict
audience_id_members_delete200_response_data_from_dict = AudienceIdMembersDelete200ResponseData.from_dict(audience_id_members_delete200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


