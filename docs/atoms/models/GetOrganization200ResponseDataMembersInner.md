# GetOrganization200ResponseDataMembersInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**user_email** | **str** |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_organization200_response_data_members_inner import GetOrganization200ResponseDataMembersInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganization200ResponseDataMembersInner from a JSON string
get_organization200_response_data_members_inner_instance = GetOrganization200ResponseDataMembersInner.from_json(json)
# print the JSON string representation of the object
print(GetOrganization200ResponseDataMembersInner.to_json())

# convert the object into a dict
get_organization200_response_data_members_inner_dict = get_organization200_response_data_members_inner_instance.to_dict()
# create an instance of GetOrganization200ResponseDataMembersInner from a dict
get_organization200_response_data_members_inner_from_dict = GetOrganization200ResponseDataMembersInner.from_dict(get_organization200_response_data_members_inner_dict)
```



