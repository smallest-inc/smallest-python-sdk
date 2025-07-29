# OrganizationGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**OrganizationGet200ResponseData**](OrganizationGet200ResponseData.md) |  | [optional] 

## Example

```python
from atoms.models.organization_get200_response import OrganizationGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationGet200Response from a JSON string
organization_get200_response_instance = OrganizationGet200Response.from_json(json)
# print the JSON string representation of the object
print(OrganizationGet200Response.to_json())

# convert the object into a dict
organization_get200_response_dict = organization_get200_response_instance.to_dict()
# create an instance of OrganizationGet200Response from a dict
organization_get200_response_from_dict = OrganizationGet200Response.from_dict(organization_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


