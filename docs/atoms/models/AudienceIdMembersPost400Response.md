# AudienceIdMembersPost400Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**errors** | **List[str]** |  | [optional] 

## Example

```python
from atoms.models.audience_id_members_post400_response import AudienceIdMembersPost400Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersPost400Response from a JSON string
audience_id_members_post400_response_instance = AudienceIdMembersPost400Response.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersPost400Response.to_json())

# convert the object into a dict
audience_id_members_post400_response_dict = audience_id_members_post400_response_instance.to_dict()
# create an instance of AudienceIdMembersPost400Response from a dict
audience_id_members_post400_response_from_dict = AudienceIdMembersPost400Response.from_dict(audience_id_members_post400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


