# AudienceIdMembersSearchGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**AudienceIdMembersSearchGet200ResponseData**](AudienceIdMembersSearchGet200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.audience_id_members_search_get200_response import AudienceIdMembersSearchGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersSearchGet200Response from a JSON string
audience_id_members_search_get200_response_instance = AudienceIdMembersSearchGet200Response.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersSearchGet200Response.to_json())

# convert the object into a dict
audience_id_members_search_get200_response_dict = audience_id_members_search_get200_response_instance.to_dict()
# create an instance of AudienceIdMembersSearchGet200Response from a dict
audience_id_members_search_get200_response_from_dict = AudienceIdMembersSearchGet200Response.from_dict(audience_id_members_search_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


