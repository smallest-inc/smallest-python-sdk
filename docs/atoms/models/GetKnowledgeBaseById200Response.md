# GetKnowledgeBaseById200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**KnowledgeBaseDTO**](KnowledgeBaseDTO.md) |  | [optional] 

## Example

```python
from smallestai.atoms.models.get_knowledge_base_by_id200_response import GetKnowledgeBaseById200Response

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



