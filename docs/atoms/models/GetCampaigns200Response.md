# GetCampaigns200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**List[GetCampaigns200ResponseDataInner]**](GetCampaigns200ResponseDataInner.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_campaigns200_response import GetCampaigns200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetCampaigns200Response from a JSON string
get_campaigns200_response_instance = GetCampaigns200Response.from_json(json)
# print the JSON string representation of the object
print(GetCampaigns200Response.to_json())

# convert the object into a dict
get_campaigns200_response_dict = get_campaigns200_response_instance.to_dict()
# create an instance of GetCampaigns200Response from a dict
get_campaigns200_response_from_dict = GetCampaigns200Response.from_dict(get_campaigns200_response_dict)
```



