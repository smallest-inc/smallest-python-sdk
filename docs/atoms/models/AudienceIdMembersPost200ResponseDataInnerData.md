# AudienceIdMembersPost200ResponseDataInnerData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**added** | **int** | Number of members successfully added | [optional] 
**skipped** | **int** | Number of members skipped (e.g., duplicates) | [optional] 

## Example

```python
from atoms.models.audience_id_members_post200_response_data_inner_data import AudienceIdMembersPost200ResponseDataInnerData

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersPost200ResponseDataInnerData from a JSON string
audience_id_members_post200_response_data_inner_data_instance = AudienceIdMembersPost200ResponseDataInnerData.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersPost200ResponseDataInnerData.to_json())

# convert the object into a dict
audience_id_members_post200_response_data_inner_data_dict = audience_id_members_post200_response_data_inner_data_instance.to_dict()
# create an instance of AudienceIdMembersPost200ResponseDataInnerData from a dict
audience_id_members_post200_response_data_inner_data_from_dict = AudienceIdMembersPost200ResponseDataInnerData.from_dict(audience_id_members_post200_response_data_inner_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


