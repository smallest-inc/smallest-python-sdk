# atoms.KnowledgeBaseApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_knowledge_base**](KnowledgeBaseApi.md#create_knowledge_base) | **POST** /knowledgebase | Create a knowledge base
[**delete_knowledge_base**](KnowledgeBaseApi.md#delete_knowledge_base) | **DELETE** /knowledgebase/{id} | Delete a knowledge base
[**delete_knowledge_base_item**](KnowledgeBaseApi.md#delete_knowledge_base_item) | **DELETE** /knowledgebase/{knowledgeBaseId}/items/{knowledgeBaseItemId} | Delete a knowledge base item
[**get_knowledge_base_by_id**](KnowledgeBaseApi.md#get_knowledge_base_by_id) | **GET** /knowledgebase/{id} | Get a knowledge base
[**get_knowledge_base_items**](KnowledgeBaseApi.md#get_knowledge_base_items) | **GET** /knowledgebase/{id}/items | Get all knowledge base items
[**get_knowledge_bases**](KnowledgeBaseApi.md#get_knowledge_bases) | **GET** /knowledgebase | Get all knowledge bases
[**upload_media_to_knowledge_base**](KnowledgeBaseApi.md#upload_media_to_knowledge_base) | **POST** /knowledgebase/{id}/items/upload-media | Upload media to a knowledge base
[**upload_text_to_knowledge_base**](KnowledgeBaseApi.md#upload_text_to_knowledge_base) | **POST** /knowledgebase/{id}/items/upload-text | Upload text to a knowledge base

# **create_knowledge_base**

Create a new knowledge base.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    kb_request = {
        "name": "My Knowledge Base",
        "description": "Knowledge base description"
    }
    
    response = atoms_client.create_knowledge_base(create_knowledge_base_request=kb_request)
    print(f"Created knowledge base with ID: {response.data}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**create_knowledge_base_request** | [**CreateKnowledgeBaseRequest**](./models/CreateKnowledgeBaseRequest.md) | Knowledge base configuration | 

### Return type

[**CreateKnowledgeBase201Response**](./models/CreateKnowledgeBase201Response.md)

# **delete_knowledge_base**

Delete an existing knowledge base.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    kb_id = "your_knowledge_base_id"
    response = atoms_client.delete_knowledge_base(id=kb_id)
    print("Knowledge base deleted successfully")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Knowledge base ID to delete | 

### Return type

[**DeleteAgent200Response**](./models/DeleteAgent200Response.md)

# **delete_knowledge_base_item**

Delete an item from a knowledge base.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    kb_id = "your_knowledge_base_id"
    item_id = "your_item_id"
    response = atoms_client.delete_knowledge_base_item(
        knowledge_base_id=kb_id,
        knowledge_base_item_id=item_id
    )
    print("Knowledge base item deleted successfully")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**knowledge_base_id** | **str** | Knowledge base ID | 
**knowledge_base_item_id** | **str** | Item ID to delete | 

### Return type

[**DeleteAgent200Response**](./models/DeleteAgent200Response.md)

# **get_knowledge_base_by_id**

Get details of a specific knowledge base.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    kb_id = "your_knowledge_base_id"
    response = atoms_client.get_knowledge_base_by_id(id=kb_id)
    print(f"Knowledge base details: {response.data}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Knowledge base ID to retrieve | 

### Return type

[**GetKnowledgeBaseById200Response**](./models/GetKnowledgeBaseById200Response.md)

# **get_knowledge_base_items**

Get all items in a knowledge base.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    kb_id = "your_knowledge_base_id"
    response = atoms_client.get_knowledge_base_items(id=kb_id)
    print(f"Knowledge base items: {response.data}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Knowledge base ID | 

### Return type

[**GetKnowledgeBaseItems200Response**](./models/GetKnowledgeBaseItems200Response.md)

# **get_knowledge_bases**

Get a list of all knowledge bases.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    response = atoms_client.get_knowledge_bases()
    print(f"Retrieved knowledge bases: {response.data}")

if __name__ == "__main__":
    main()
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**GetKnowledgeBases200Response**](./models/GetKnowledgeBases200Response.md)

# **upload_media_to_knowledge_base**

Upload media file to a knowledge base.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    kb_id = "your_knowledge_base_id"
    with open("media_file.mp4", "rb") as media_file:
        response = atoms_client.upload_media_to_knowledge_base(
            id=kb_id,
            media=media_file.read()
        )
    print("Media uploaded successfully")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Knowledge base ID | 
**media** | **bytearray** | Media file content | 

### Return type

[**DeleteAgent200Response**](./models/DeleteAgent200Response.md)

# **upload_text_to_knowledge_base**

Upload text content to a knowledge base.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    kb_id = "your_knowledge_base_id"
    text_request = {
        "title": "Your title here",
        "content": "Your text content here"
    }
    
    response = atoms_client.upload_text_to_knowledge_base(
        id=kb_id,
        upload_text_to_knowledge_base_request=text_request
    )
    print("Text uploaded successfully")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Knowledge base ID | 
**upload_text_to_knowledge_base_request** | [**UploadTextToKnowledgeBaseRequest**](./models/UploadTextToKnowledgeBaseRequest.md) | Text content and metadata | 

### Return type

[**DeleteAgent200Response**](./models/DeleteAgent200Response.md)

