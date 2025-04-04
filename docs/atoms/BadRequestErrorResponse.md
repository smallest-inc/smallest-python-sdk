# BadRequestErrorResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**errors** | **List[str]** |  | [optional] 

## Example

```python
from smallestai.atoms.models.bad_request_error_response import BadRequestErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BadRequestErrorResponse from a JSON string
bad_request_error_response_instance = BadRequestErrorResponse.from_json(json)
# print the JSON string representation of the object
print(BadRequestErrorResponse.to_json())

# convert the object into a dict
bad_request_error_response_dict = bad_request_error_response_instance.to_dict()
# create an instance of BadRequestErrorResponse from a dict
bad_request_error_response_from_dict = BadRequestErrorResponse.from_dict(bad_request_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


