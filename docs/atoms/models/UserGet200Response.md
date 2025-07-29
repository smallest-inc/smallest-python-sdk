# UserGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**UserGet200ResponseData**](UserGet200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.user_get200_response import UserGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of UserGet200Response from a JSON string
user_get200_response_instance = UserGet200Response.from_json(json)
# print the JSON string representation of the object
print(UserGet200Response.to_json())

# convert the object into a dict
user_get200_response_dict = user_get200_response_instance.to_dict()
# create an instance of UserGet200Response from a dict
user_get200_response_from_dict = UserGet200Response.from_dict(user_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


