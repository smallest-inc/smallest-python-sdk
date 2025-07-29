# AudienceIdMembersSearchGet500Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**errors** | **List[str]** |  | [optional] 

## Example

```python
from atoms.models.audience_id_members_search_get500_response import AudienceIdMembersSearchGet500Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersSearchGet500Response from a JSON string
audience_id_members_search_get500_response_instance = AudienceIdMembersSearchGet500Response.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersSearchGet500Response.to_json())

# convert the object into a dict
audience_id_members_search_get500_response_dict = audience_id_members_search_get500_response_instance.to_dict()
# create an instance of AudienceIdMembersSearchGet500Response from a dict
audience_id_members_search_get500_response_from_dict = AudienceIdMembersSearchGet500Response.from_dict(audience_id_members_search_get500_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


