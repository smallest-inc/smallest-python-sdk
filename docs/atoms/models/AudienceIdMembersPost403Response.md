# AudienceIdMembersPost403Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**errors** | **List[str]** |  | [optional] 

## Example

```python
from atoms.models.audience_id_members_post403_response import AudienceIdMembersPost403Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersPost403Response from a JSON string
audience_id_members_post403_response_instance = AudienceIdMembersPost403Response.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersPost403Response.to_json())

# convert the object into a dict
audience_id_members_post403_response_dict = audience_id_members_post403_response_instance.to_dict()
# create an instance of AudienceIdMembersPost403Response from a dict
audience_id_members_post403_response_from_dict = AudienceIdMembersPost403Response.from_dict(audience_id_members_post403_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


