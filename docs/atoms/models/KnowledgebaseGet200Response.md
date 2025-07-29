# KnowledgebaseGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**List[KnowledgeBase]**](KnowledgeBase.md) |  | [optional] 

## Example

```python
from atoms.models.knowledgebase_get200_response import KnowledgebaseGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of KnowledgebaseGet200Response from a JSON string
knowledgebase_get200_response_instance = KnowledgebaseGet200Response.from_json(json)
# print the JSON string representation of the object
print(KnowledgebaseGet200Response.to_json())

# convert the object into a dict
knowledgebase_get200_response_dict = knowledgebase_get200_response_instance.to_dict()
# create an instance of KnowledgebaseGet200Response from a dict
knowledgebase_get200_response_from_dict = KnowledgebaseGet200Response.from_dict(knowledgebase_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


