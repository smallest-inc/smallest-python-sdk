# KnowledgeBase


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the knowledge base | 
**name** | **str** | The name of the knowledge base | 
**description** | **str** | The description of the knowledge base | [optional] 
**organization** | **str** | The organization ID | 
**created_by** | **str** | The user ID who created the knowledge base | 
**created_at** | **datetime** | The date and time when the knowledge base was created | [optional] 
**updated_at** | **datetime** | The date and time when the knowledge base was last updated | [optional] 

## Example

```python
from atoms.models.knowledge_base import KnowledgeBase

# TODO update the JSON string below
json = "{}"
# create an instance of KnowledgeBase from a JSON string
knowledge_base_instance = KnowledgeBase.from_json(json)
# print the JSON string representation of the object
print(KnowledgeBase.to_json())

# convert the object into a dict
knowledge_base_dict = knowledge_base_instance.to_dict()
# create an instance of KnowledgeBase from a dict
knowledge_base_from_dict = KnowledgeBase.from_dict(knowledge_base_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


