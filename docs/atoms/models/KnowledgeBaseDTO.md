# KnowledgeBaseDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the knowledge base | 
**name** | **str** | The name of the knowledge base | 
**description** | **str** | Description of the knowledge base | [optional] 
**organization** | **str** | The organization ID this knowledge base belongs to | 

## Example

```python
from smallestai.atoms.models.knowledge_base_dto import KnowledgeBaseDTO

# TODO update the JSON string below
json = "{}"
# create an instance of KnowledgeBaseDTO from a JSON string
knowledge_base_dto_instance = KnowledgeBaseDTO.from_json(json)
# print the JSON string representation of the object
print(KnowledgeBaseDTO.to_json())

# convert the object into a dict
knowledge_base_dto_dict = knowledge_base_dto_instance.to_dict()
# create an instance of KnowledgeBaseDTO from a dict
knowledge_base_dto_from_dict = KnowledgeBaseDTO.from_dict(knowledge_base_dto_dict)
```



