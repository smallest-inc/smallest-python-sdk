# GetKnowledgeBaseItems200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**List[KnowledgeBaseItemDTO]**](KnowledgeBaseItemDTO.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_knowledge_base_items200_response import GetKnowledgeBaseItems200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetKnowledgeBaseItems200Response from a JSON string
get_knowledge_base_items200_response_instance = GetKnowledgeBaseItems200Response.from_json(json)
# print the JSON string representation of the object
print(GetKnowledgeBaseItems200Response.to_json())

# convert the object into a dict
get_knowledge_base_items200_response_dict = get_knowledge_base_items200_response_instance.to_dict()
# create an instance of GetKnowledgeBaseItems200Response from a dict
get_knowledge_base_items200_response_from_dict = GetKnowledgeBaseItems200Response.from_dict(get_knowledge_base_items200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


