# KnowledgeBaseItemDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**item_type** | **str** |  | 
**metadata** | **object** |  | [optional] 
**knowledge_base_id** | **str** |  | 
**processing_status** | **str** |  | 
**content_type** | **str** |  | [optional] 
**size** | **float** |  | [optional] 
**key** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**content** | **str** |  | [optional] 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from smallestai.atoms.models.knowledge_base_item_dto import KnowledgeBaseItemDTO

# TODO update the JSON string below
json = "{}"
# create an instance of KnowledgeBaseItemDTO from a JSON string
knowledge_base_item_dto_instance = KnowledgeBaseItemDTO.from_json(json)
# print the JSON string representation of the object
print(KnowledgeBaseItemDTO.to_json())

# convert the object into a dict
knowledge_base_item_dto_dict = knowledge_base_item_dto_instance.to_dict()
# create an instance of KnowledgeBaseItemDTO from a dict
knowledge_base_item_dto_from_dict = KnowledgeBaseItemDTO.from_dict(knowledge_base_item_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


