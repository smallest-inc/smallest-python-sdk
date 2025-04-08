# CreateCampaign200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**CreateCampaign200ResponseData**](CreateCampaign200ResponseData.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.create_campaign200_response import CreateCampaign200Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCampaign200Response from a JSON string
create_campaign200_response_instance = CreateCampaign200Response.from_json(json)
# print the JSON string representation of the object
print(CreateCampaign200Response.to_json())

# convert the object into a dict
create_campaign200_response_dict = create_campaign200_response_instance.to_dict()
# create an instance of CreateCampaign200Response from a dict
create_campaign200_response_from_dict = CreateCampaign200Response.from_dict(create_campaign200_response_dict)
```



