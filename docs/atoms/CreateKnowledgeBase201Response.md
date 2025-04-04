# CreateKnowledgeBase201Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | **str** |  | [optional] 

## Example

```python
from smallestai.atoms.models.create_knowledge_base201_response import CreateKnowledgeBase201Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateKnowledgeBase201Response from a JSON string
create_knowledge_base201_response_instance = CreateKnowledgeBase201Response.from_json(json)
# print the JSON string representation of the object
print(CreateKnowledgeBase201Response.to_json())

# convert the object into a dict
create_knowledge_base201_response_dict = create_knowledge_base201_response_instance.to_dict()
# create an instance of CreateKnowledgeBase201Response from a dict
create_knowledge_base201_response_from_dict = CreateKnowledgeBase201Response.from_dict(create_knowledge_base201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


