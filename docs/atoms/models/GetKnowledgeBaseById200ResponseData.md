# GetKnowledgeBaseById200ResponseData


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
**updated_at** | **datetime** |  | 

## Example

```python
from smallestai.atoms_client.models.get_knowledge_base_by_id200_response_data import GetKnowledgeBaseById200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetKnowledgeBaseById200ResponseData from a JSON string
get_knowledge_base_by_id200_response_data_instance = GetKnowledgeBaseById200ResponseData.from_json(json)
# print the JSON string representation of the object
print(GetKnowledgeBaseById200ResponseData.to_json())

# convert the object into a dict
get_knowledge_base_by_id200_response_data_dict = get_knowledge_base_by_id200_response_data_instance.to_dict()
# create an instance of GetKnowledgeBaseById200ResponseData from a dict
get_knowledge_base_by_id200_response_data_from_dict = GetKnowledgeBaseById200ResponseData.from_dict(get_knowledge_base_by_id200_response_data_dict)
```



