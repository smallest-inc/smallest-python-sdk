# GetOrganization200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**GetOrganization200ResponseData**](GetOrganization200ResponseData.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_organization200_response import GetOrganization200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganization200Response from a JSON string
get_organization200_response_instance = GetOrganization200Response.from_json(json)
# print the JSON string representation of the object
print(GetOrganization200Response.to_json())

# convert the object into a dict
get_organization200_response_dict = get_organization200_response_instance.to_dict()
# create an instance of GetOrganization200Response from a dict
get_organization200_response_from_dict = GetOrganization200Response.from_dict(get_organization200_response_dict)
```



