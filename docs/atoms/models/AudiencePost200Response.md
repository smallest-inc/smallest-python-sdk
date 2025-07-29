# AudiencePost200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**AudiencePost200ResponseData**](AudiencePost200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.audience_post200_response import AudiencePost200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudiencePost200Response from a JSON string
audience_post200_response_instance = AudiencePost200Response.from_json(json)
# print the JSON string representation of the object
print(AudiencePost200Response.to_json())

# convert the object into a dict
audience_post200_response_dict = audience_post200_response_instance.to_dict()
# create an instance of AudiencePost200Response from a dict
audience_post200_response_from_dict = AudiencePost200Response.from_dict(audience_post200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


