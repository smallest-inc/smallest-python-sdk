# StartOutboundCall200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**call_id** | **str** | The ID of the initiated call | [optional] 

## Example

```python
from smallestai.atoms_client.models.start_outbound_call200_response_data import StartOutboundCall200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of StartOutboundCall200ResponseData from a JSON string
start_outbound_call200_response_data_instance = StartOutboundCall200ResponseData.from_json(json)
# print the JSON string representation of the object
print(StartOutboundCall200ResponseData.to_json())

# convert the object into a dict
start_outbound_call200_response_data_dict = start_outbound_call200_response_data_instance.to_dict()
# create an instance of StartOutboundCall200ResponseData from a dict
start_outbound_call200_response_data_from_dict = StartOutboundCall200ResponseData.from_dict(start_outbound_call200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


