# InternalServerErrorResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**errors** | **List[str]** |  | [optional] 

## Example

```python
from smallestai.atoms.models.internal_server_error_response import InternalServerErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of InternalServerErrorResponse from a JSON string
internal_server_error_response_instance = InternalServerErrorResponse.from_json(json)
# print the JSON string representation of the object
print(InternalServerErrorResponse.to_json())

# convert the object into a dict
internal_server_error_response_dict = internal_server_error_response_instance.to_dict()
# create an instance of InternalServerErrorResponse from a dict
internal_server_error_response_from_dict = InternalServerErrorResponse.from_dict(internal_server_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


