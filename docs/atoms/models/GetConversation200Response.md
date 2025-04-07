# GetConversation200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**GetConversation200ResponseData**](GetConversation200ResponseData.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_conversation200_response import GetConversation200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetConversation200Response from a JSON string
get_conversation200_response_instance = GetConversation200Response.from_json(json)
# print the JSON string representation of the object
print(GetConversation200Response.to_json())

# convert the object into a dict
get_conversation200_response_dict = get_conversation200_response_instance.to_dict()
# create an instance of GetConversation200Response from a dict
get_conversation200_response_from_dict = GetConversation200Response.from_dict(get_conversation200_response_dict)
```



