# GetKnowledgeBaseById200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**GetKnowledgeBaseById200ResponseData**](GetKnowledgeBaseById200ResponseData.md) |  | [optional] 

## Example

```python
from smallestai.atoms_client.models.get_knowledge_base_by_id200_response import GetKnowledgeBaseById200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetKnowledgeBaseById200Response from a JSON string
get_knowledge_base_by_id200_response_instance = GetKnowledgeBaseById200Response.from_json(json)
# print the JSON string representation of the object
print(GetKnowledgeBaseById200Response.to_json())

# convert the object into a dict
get_knowledge_base_by_id200_response_dict = get_knowledge_base_by_id200_response_instance.to_dict()
# create an instance of GetKnowledgeBaseById200Response from a dict
get_knowledge_base_by_id200_response_from_dict = GetKnowledgeBaseById200Response.from_dict(get_knowledge_base_by_id200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


