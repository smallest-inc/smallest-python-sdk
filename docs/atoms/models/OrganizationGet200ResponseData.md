# OrganizationGet200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**members** | [**List[OrganizationGet200ResponseDataMembersInner]**](OrganizationGet200ResponseDataMembersInner.md) |  | [optional] 
**subscription** | [**OrganizationGet200ResponseDataSubscription**](OrganizationGet200ResponseDataSubscription.md) |  | [optional] 

## Example

```python
from atoms.models.organization_get200_response_data import OrganizationGet200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationGet200ResponseData from a JSON string
organization_get200_response_data_instance = OrganizationGet200ResponseData.from_json(json)
# print the JSON string representation of the object
print(OrganizationGet200ResponseData.to_json())

# convert the object into a dict
organization_get200_response_data_dict = organization_get200_response_data_instance.to_dict()
# create an instance of OrganizationGet200ResponseData from a dict
organization_get200_response_data_from_dict = OrganizationGet200ResponseData.from_dict(organization_get200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


