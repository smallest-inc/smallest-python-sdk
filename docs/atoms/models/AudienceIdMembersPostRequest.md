# AudienceIdMembersPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**members** | **List[object]** | Array of member objects with dynamic structure based on audience configuration | 

## Example

```python
from atoms.models.audience_id_members_post_request import AudienceIdMembersPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersPostRequest from a JSON string
audience_id_members_post_request_instance = AudienceIdMembersPostRequest.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersPostRequest.to_json())

# convert the object into a dict
audience_id_members_post_request_dict = audience_id_members_post_request_instance.to_dict()
# create an instance of AudienceIdMembersPostRequest from a dict
audience_id_members_post_request_from_dict = AudienceIdMembersPostRequest.from_dict(audience_id_members_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


