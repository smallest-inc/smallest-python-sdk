# UpdateAgent200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | **str** | The ID of the updated agent | [optional] 

## Example

```python
from smallestai.atoms_client.models.update_agent200_response import UpdateAgent200Response

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAgent200Response from a JSON string
update_agent200_response_instance = UpdateAgent200Response.from_json(json)
# print the JSON string representation of the object
print(UpdateAgent200Response.to_json())

# convert the object into a dict
update_agent200_response_dict = update_agent200_response_instance.to_dict()
# create an instance of UpdateAgent200Response from a dict
update_agent200_response_from_dict = UpdateAgent200Response.from_dict(update_agent200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


