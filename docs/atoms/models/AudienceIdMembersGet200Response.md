# AudienceIdMembersGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**AudienceIdMembersGet200ResponseData**](AudienceIdMembersGet200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.audience_id_members_get200_response import AudienceIdMembersGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersGet200Response from a JSON string
audience_id_members_get200_response_instance = AudienceIdMembersGet200Response.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersGet200Response.to_json())

# convert the object into a dict
audience_id_members_get200_response_dict = audience_id_members_get200_response_instance.to_dict()
# create an instance of AudienceIdMembersGet200Response from a dict
audience_id_members_get200_response_from_dict = AudienceIdMembersGet200Response.from_dict(audience_id_members_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


