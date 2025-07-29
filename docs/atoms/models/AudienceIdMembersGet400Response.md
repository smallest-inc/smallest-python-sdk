# AudienceIdMembersGet400Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | [optional] 
**errors** | **List[str]** |  | [optional] 

## Example

```python
from atoms.models.audience_id_members_get400_response import AudienceIdMembersGet400Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersGet400Response from a JSON string
audience_id_members_get400_response_instance = AudienceIdMembersGet400Response.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersGet400Response.to_json())

# convert the object into a dict
audience_id_members_get400_response_dict = audience_id_members_get400_response_instance.to_dict()
# create an instance of AudienceIdMembersGet400Response from a dict
audience_id_members_get400_response_from_dict = AudienceIdMembersGet400Response.from_dict(audience_id_members_get400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


