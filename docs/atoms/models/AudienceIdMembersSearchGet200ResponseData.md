# AudienceIdMembersSearchGet200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**members** | [**List[AudienceIdMembersGet200ResponseDataMembersInner]**](AudienceIdMembersGet200ResponseDataMembersInner.md) |  | [optional] 
**search_info** | [**AudienceIdMembersSearchGet200ResponseDataSearchInfo**](AudienceIdMembersSearchGet200ResponseDataSearchInfo.md) |  | [optional] 

## Example

```python
from atoms.models.audience_id_members_search_get200_response_data import AudienceIdMembersSearchGet200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersSearchGet200ResponseData from a JSON string
audience_id_members_search_get200_response_data_instance = AudienceIdMembersSearchGet200ResponseData.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersSearchGet200ResponseData.to_json())

# convert the object into a dict
audience_id_members_search_get200_response_data_dict = audience_id_members_search_get200_response_data_instance.to_dict()
# create an instance of AudienceIdMembersSearchGet200ResponseData from a dict
audience_id_members_search_get200_response_data_from_dict = AudienceIdMembersSearchGet200ResponseData.from_dict(audience_id_members_search_get200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


