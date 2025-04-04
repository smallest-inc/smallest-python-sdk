# GetOrganization200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**members** | [**List[GetOrganization200ResponseDataMembersInner]**](GetOrganization200ResponseDataMembersInner.md) |  | [optional] 
**subscription** | [**GetOrganization200ResponseDataSubscription**](GetOrganization200ResponseDataSubscription.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_organization200_response_data import GetOrganization200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganization200ResponseData from a JSON string
get_organization200_response_data_instance = GetOrganization200ResponseData.from_json(json)
# print the JSON string representation of the object
print(GetOrganization200ResponseData.to_json())

# convert the object into a dict
get_organization200_response_data_dict = get_organization200_response_data_instance.to_dict()
# create an instance of GetOrganization200ResponseData from a dict
get_organization200_response_data_from_dict = GetOrganization200ResponseData.from_dict(get_organization200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


