# CreateCampaign201Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**CreateCampaign201ResponseData**](CreateCampaign201ResponseData.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.create_campaign201_response import CreateCampaign201Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCampaign201Response from a JSON string
create_campaign201_response_instance = CreateCampaign201Response.from_json(json)
# print the JSON string representation of the object
print(CreateCampaign201Response.to_json())

# convert the object into a dict
create_campaign201_response_dict = create_campaign201_response_instance.to_dict()
# create an instance of CreateCampaign201Response from a dict
create_campaign201_response_from_dict = CreateCampaign201Response.from_dict(create_campaign201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


