# AudienceIdGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**AudienceGet200ResponseDataInner**](AudienceGet200ResponseDataInner.md) |  | [optional] 

## Example

```python
from atoms.models.audience_id_get200_response import AudienceIdGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdGet200Response from a JSON string
audience_id_get200_response_instance = AudienceIdGet200Response.from_json(json)
# print the JSON string representation of the object
print(AudienceIdGet200Response.to_json())

# convert the object into a dict
audience_id_get200_response_dict = audience_id_get200_response_instance.to_dict()
# create an instance of AudienceIdGet200Response from a dict
audience_id_get200_response_from_dict = AudienceIdGet200Response.from_dict(audience_id_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


