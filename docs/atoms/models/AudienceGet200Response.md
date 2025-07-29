# AudienceGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**List[AudienceGet200ResponseDataInner]**](AudienceGet200ResponseDataInner.md) |  | [optional] 

## Example

```python
from atoms.models.audience_get200_response import AudienceGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceGet200Response from a JSON string
audience_get200_response_instance = AudienceGet200Response.from_json(json)
# print the JSON string representation of the object
print(AudienceGet200Response.to_json())

# convert the object into a dict
audience_get200_response_dict = audience_get200_response_instance.to_dict()
# create an instance of AudienceGet200Response from a dict
audience_get200_response_from_dict = AudienceGet200Response.from_dict(audience_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


