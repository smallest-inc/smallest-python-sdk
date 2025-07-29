# KnowledgeBaseItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the knowledge base item | 
**item_type** | **str** | The type of the knowledge base item | 
**metadata** | **object** | Additional metadata for the item | [optional] 
**knowledge_base_id** | **str** | The ID of the knowledge base this item belongs to | 
**processing_status** | **str** | The processing status of the item | 
**file_name** | **str** | The name of the file (for file type items) | [optional] 
**content_type** | **str** | The MIME type of the content | [optional] 
**size** | **float** | The size of the file in bytes | [optional] 
**key** | **str** | The storage key for the file | [optional] 
**title** | **str** | The title of the item | [optional] 
**content** | **str** | The content of the item (for text type items) | [optional] 
**created_at** | **datetime** | The date and time when the item was created | 
**updated_at** | **datetime** | The date and time when the item was last updated | 

## Example

```python
from atoms.models.knowledge_base_item import KnowledgeBaseItem

# TODO update the JSON string below
json = "{}"
# create an instance of KnowledgeBaseItem from a JSON string
knowledge_base_item_instance = KnowledgeBaseItem.from_json(json)
# print the JSON string representation of the object
print(KnowledgeBaseItem.to_json())

# convert the object into a dict
knowledge_base_item_dict = knowledge_base_item_instance.to_dict()
# create an instance of KnowledgeBaseItem from a dict
knowledge_base_item_from_dict = KnowledgeBaseItem.from_dict(knowledge_base_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


