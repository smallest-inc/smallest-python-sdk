# UploadTextToKnowledgeBaseRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**content** | **str** |  | 

## Example

```python
from smallestai.atoms.models.upload_text_to_knowledge_base_request import UploadTextToKnowledgeBaseRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UploadTextToKnowledgeBaseRequest from a JSON string
upload_text_to_knowledge_base_request_instance = UploadTextToKnowledgeBaseRequest.from_json(json)
# print the JSON string representation of the object
print(UploadTextToKnowledgeBaseRequest.to_json())

# convert the object into a dict
upload_text_to_knowledge_base_request_dict = upload_text_to_knowledge_base_request_instance.to_dict()
# create an instance of UploadTextToKnowledgeBaseRequest from a dict
upload_text_to_knowledge_base_request_from_dict = UploadTextToKnowledgeBaseRequest.from_dict(upload_text_to_knowledge_base_request_dict)
```



