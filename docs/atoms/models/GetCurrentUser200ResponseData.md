# GetCurrentUser200ResponseData


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
from smallestai.atoms.models.get_current_user200_response_data import GetCurrentUser200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetCurrentUser200ResponseData from a JSON string
get_current_user200_response_data_instance = GetCurrentUser200ResponseData.from_json(json)
# print the JSON string representation of the object
print(GetCurrentUser200ResponseData.to_json())

# convert the object into a dict
get_current_user200_response_data_dict = get_current_user200_response_data_instance.to_dict()
# create an instance of GetCurrentUser200ResponseData from a dict
get_current_user200_response_data_from_dict = GetCurrentUser200ResponseData.from_dict(get_current_user200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


