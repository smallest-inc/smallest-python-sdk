# StartOutboundCall200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**StartOutboundCall200ResponseData**](StartOutboundCall200ResponseData.md) |  | [optional] 

## Example

```python
from smallestai.atoms_client.models.start_outbound_call200_response import StartOutboundCall200Response

# TODO update the JSON string below
json = "{}"
# create an instance of StartOutboundCall200Response from a JSON string
start_outbound_call200_response_instance = StartOutboundCall200Response.from_json(json)
# print the JSON string representation of the object
print(StartOutboundCall200Response.to_json())

# convert the object into a dict
start_outbound_call200_response_dict = start_outbound_call200_response_instance.to_dict()
# create an instance of StartOutboundCall200Response from a dict
start_outbound_call200_response_from_dict = StartOutboundCall200Response.from_dict(start_outbound_call200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


