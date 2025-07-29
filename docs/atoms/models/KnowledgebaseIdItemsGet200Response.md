# KnowledgebaseIdItemsGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**List[KnowledgeBaseItem]**](KnowledgeBaseItem.md) |  | [optional] 

## Example

```python
from atoms.models.knowledgebase_id_items_get200_response import KnowledgebaseIdItemsGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of KnowledgebaseIdItemsGet200Response from a JSON string
knowledgebase_id_items_get200_response_instance = KnowledgebaseIdItemsGet200Response.from_json(json)
# print the JSON string representation of the object
print(KnowledgebaseIdItemsGet200Response.to_json())

# convert the object into a dict
knowledgebase_id_items_get200_response_dict = knowledgebase_id_items_get200_response_instance.to_dict()
# create an instance of KnowledgebaseIdItemsGet200Response from a dict
knowledgebase_id_items_get200_response_from_dict = KnowledgebaseIdItemsGet200Response.from_dict(knowledgebase_id_items_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


