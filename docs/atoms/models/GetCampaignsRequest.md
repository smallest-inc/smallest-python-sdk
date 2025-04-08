# GetCampaignsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **float** | The page number | [optional] [default to 1]
**limit** | **float** | The number of items per page | [optional] [default to 10]

## Example

```python
from smallestai.atoms.models.get_campaigns_request import GetCampaignsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetCampaignsRequest from a JSON string
get_campaigns_request_instance = GetCampaignsRequest.from_json(json)
# print the JSON string representation of the object
print(GetCampaignsRequest.to_json())

# convert the object into a dict
get_campaigns_request_dict = get_campaigns_request_instance.to_dict()
# create an instance of GetCampaignsRequest from a dict
get_campaigns_request_from_dict = GetCampaignsRequest.from_dict(get_campaigns_request_dict)
```



