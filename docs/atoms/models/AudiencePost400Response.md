# AudiencePost400Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**errors** | **List[str]** |  | [optional] 

## Example

```python
from atoms.models.audience_post400_response import AudiencePost400Response

# TODO update the JSON string below
json = "{}"
# create an instance of AudiencePost400Response from a JSON string
audience_post400_response_instance = AudiencePost400Response.from_json(json)
# print the JSON string representation of the object
print(AudiencePost400Response.to_json())

# convert the object into a dict
audience_post400_response_dict = audience_post400_response_instance.to_dict()
# create an instance of AudiencePost400Response from a dict
audience_post400_response_from_dict = AudiencePost400Response.from_dict(audience_post400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


