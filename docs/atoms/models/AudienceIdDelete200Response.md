# AudienceIdDelete200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | **List[str]** |  | [optional] 

## Example

```python
from atoms.models.audience_id_delete200_response import AudienceIdDelete200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdDelete200Response from a JSON string
audience_id_delete200_response_instance = AudienceIdDelete200Response.from_json(json)
# print the JSON string representation of the object
print(AudienceIdDelete200Response.to_json())

# convert the object into a dict
audience_id_delete200_response_dict = audience_id_delete200_response_instance.to_dict()
# create an instance of AudienceIdDelete200Response from a dict
audience_id_delete200_response_from_dict = AudienceIdDelete200Response.from_dict(audience_id_delete200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


