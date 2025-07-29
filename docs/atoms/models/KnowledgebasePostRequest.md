# KnowledgebasePostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 

## Example

```python
from atoms.models.knowledgebase_post_request import KnowledgebasePostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of KnowledgebasePostRequest from a JSON string
knowledgebase_post_request_instance = KnowledgebasePostRequest.from_json(json)
# print the JSON string representation of the object
print(KnowledgebasePostRequest.to_json())

# convert the object into a dict
knowledgebase_post_request_dict = knowledgebase_post_request_instance.to_dict()
# create an instance of KnowledgebasePostRequest from a dict
knowledgebase_post_request_from_dict = KnowledgebasePostRequest.from_dict(knowledgebase_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


