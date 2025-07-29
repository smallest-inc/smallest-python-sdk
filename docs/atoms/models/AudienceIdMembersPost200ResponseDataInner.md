# AudienceIdMembersPost200ResponseDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | [optional] 
**data** | [**AudienceIdMembersPost200ResponseDataInnerData**](AudienceIdMembersPost200ResponseDataInnerData.md) |  | [optional] 

## Example

```python
from atoms.models.audience_id_members_post200_response_data_inner import AudienceIdMembersPost200ResponseDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersPost200ResponseDataInner from a JSON string
audience_id_members_post200_response_data_inner_instance = AudienceIdMembersPost200ResponseDataInner.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersPost200ResponseDataInner.to_json())

# convert the object into a dict
audience_id_members_post200_response_data_inner_dict = audience_id_members_post200_response_data_inner_instance.to_dict()
# create an instance of AudienceIdMembersPost200ResponseDataInner from a dict
audience_id_members_post200_response_data_inner_from_dict = AudienceIdMembersPost200ResponseDataInner.from_dict(audience_id_members_post200_response_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


