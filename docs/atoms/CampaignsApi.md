# atoms.CampaignsApi

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_campaign**](CampaignsApi.md#create_campaign) | **POST** /campaign | Create a campaign
[**delete_campaign**](CampaignsApi.md#delete_campaign) | **DELETE** /campaign/{id} | Delete a campaign
[**get_campaign_by_id**](CampaignsApi.md#get_campaign_by_id) | **GET** /campaign/{id} | Get a campaign
[**get_campaigns**](CampaignsApi.md#get_campaigns) | **GET** /campaign | Retrieve all campaigns
[**pause_campaign**](CampaignsApi.md#pause_campaign) | **POST** /campaign/{id}/pause | Pause a campaign
[**start_campaign**](CampaignsApi.md#start_campaign) | **POST** /campaign/{id}/start | Start a campaign

# **create_campaign**

Create a new campaign.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    campaign_request = {
        "name": "My Campaign",
        "description": "Campaign description",
        "agent_id": "your_agent_id",
        "schedule": {
            "start_time": "2024-03-20T10:00:00Z",
            "end_time": "2024-03-21T10:00:00Z"
        }
    }
    
    response = atoms_client.create_campaign(create_campaign_request=campaign_request)
    print(f"Created campaign with ID: {response.data}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**create_campaign_request** | [**CreateCampaignRequest**](./models/CreateCampaignRequest.md) | Campaign configuration | 

### Return type

[**CreateCampaign201Response**](./models/CreateCampaign201Response.md)

# **delete_campaign**

Delete an existing campaign.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    campaign_id = "your_campaign_id"
    response = atoms_client.delete_campaign(id=campaign_id)
    print("Campaign deleted successfully")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Campaign ID to delete | 

### Return type

[**DeleteAgent200Response**](./models/DeleteAgent200Response.md)

# **get_campaign_by_id**

Get details of a specific campaign.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    campaign_id = "your_campaign_id"
    response = atoms_client.get_campaign_by_id(id=campaign_id)
    print(f"Campaign details: {response.data}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Campaign ID to retrieve | 

### Return type

[**GetCampaignById200Response**](./models/GetCampaignById200Response.md)

# **get_campaigns**

Get a list of all campaigns.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    request = {
        "page": 1,
        "limit": 10
    }
    
    response = atoms_client.get_campaigns(get_campaigns_request=request)
    print(f"Retrieved campaigns: {response.data}")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**get_campaigns_request** | [**GetCampaignsRequest**](./models/GetCampaignsRequest.md) | Pagination parameters | 

### Return type

[**GetCampaigns200Response**](./models/GetCampaigns200Response.md)

# **pause_campaign**

Pause a running campaign.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    campaign_id = "your_campaign_id"
    response = atoms_client.pause_campaign(id=campaign_id)
    print("Campaign paused successfully")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Campaign ID to pause | 

### Return type

[**DeleteAgent200Response**](./models/DeleteAgent200Response.md)

# **start_campaign**

Start a paused or new campaign.

### Example

```python
from smallestai.atoms import AtomsClient

def main():
    atoms_client = AtomsClient()
    
    campaign_id = "your_campaign_id"
    response = atoms_client.start_campaign(id=campaign_id)
    print("Campaign started successfully")

if __name__ == "__main__":
    main()
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**id** | **str** | Campaign ID to start | 

### Return type

[**DeleteAgent200Response**](./models/DeleteAgent200Response.md)

