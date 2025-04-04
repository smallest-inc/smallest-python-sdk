# CreateKnowledgeBaseRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 

## Example

```python
from smallestai.atoms.models.create_knowledge_base_request import CreateKnowledgeBaseRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateKnowledgeBaseRequest from a JSON string
create_knowledge_base_request_instance = CreateKnowledgeBaseRequest.from_json(json)
# print the JSON string representation of the object
print(CreateKnowledgeBaseRequest.to_json())

# convert the object into a dict
create_knowledge_base_request_dict = create_knowledge_base_request_instance.to_dict()
# create an instance of CreateKnowledgeBaseRequest from a dict
create_knowledge_base_request_from_dict = CreateKnowledgeBaseRequest.from_dict(create_knowledge_base_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


