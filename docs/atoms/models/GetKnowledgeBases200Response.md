# GetKnowledgeBases200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**List[KnowledgeBaseDTO]**](KnowledgeBaseDTO.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_knowledge_bases200_response import GetKnowledgeBases200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetKnowledgeBases200Response from a JSON string
get_knowledge_bases200_response_instance = GetKnowledgeBases200Response.from_json(json)
# print the JSON string representation of the object
print(GetKnowledgeBases200Response.to_json())

# convert the object into a dict
get_knowledge_bases200_response_dict = get_knowledge_bases200_response_instance.to_dict()
# create an instance of GetKnowledgeBases200Response from a dict
get_knowledge_bases200_response_from_dict = GetKnowledgeBases200Response.from_dict(get_knowledge_bases200_response_dict)
```



