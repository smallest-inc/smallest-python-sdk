# AudienceIdMembersDeleteRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**member_ids** | **List[str]** | Array of member IDs to delete | 

## Example

```python
from atoms.models.audience_id_members_delete_request import AudienceIdMembersDeleteRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersDeleteRequest from a JSON string
audience_id_members_delete_request_instance = AudienceIdMembersDeleteRequest.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersDeleteRequest.to_json())

# convert the object into a dict
audience_id_members_delete_request_dict = audience_id_members_delete_request_instance.to_dict()
# create an instance of AudienceIdMembersDeleteRequest from a dict
audience_id_members_delete_request_from_dict = AudienceIdMembersDeleteRequest.from_dict(audience_id_members_delete_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


