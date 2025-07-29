# UserGet200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the user | [optional] 
**first_name** | **str** | The first name of the user | [optional] 
**last_name** | **str** | The last name of the user | [optional] 
**user_email** | **str** | The email of the user | [optional] 
**auth_provider** | **str** | The authentication provider of the user | [optional] 
**is_email_verified** | **bool** | Whether the user&#39;s email is verified | [optional] 
**organization_id** | **str** |  | [optional] 

## Example

```python
from atoms.models.user_get200_response_data import UserGet200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of UserGet200ResponseData from a JSON string
user_get200_response_data_instance = UserGet200ResponseData.from_json(json)
# print the JSON string representation of the object
print(UserGet200ResponseData.to_json())

# convert the object into a dict
user_get200_response_data_dict = user_get200_response_data_instance.to_dict()
# create an instance of UserGet200ResponseData from a dict
user_get200_response_data_from_dict = UserGet200ResponseData.from_dict(user_get200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


