
All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AgentTemplatesApi* | [**create_agent_from_template**](./AgentTemplatesApi.md#create_agent_from_template) | **POST** /agent/from-template | Create agent from template
*AgentTemplatesApi* | [**get_agent_templates**](./AgentTemplatesApi.md#get_agent_templates) | **GET** /agent/template | Get agent templates
*AgentsApi* | [**create_agent**](./AgentsApi.md#create_agent) | **POST** /agent | Create a new agent
*AgentsApi* | [**delete_agent**](./AgentsApi.md#delete_agent) | **DELETE** /agent/{id} | Delete an agent
*AgentsApi* | [**get_agent_by_id**](./AgentsApi.md#get_agent_by_id) | **GET** /agent/{id} | Get agent by ID
*AgentsApi* | [**get_agents**](./AgentsApi.md#get_agents) | **GET** /agent | Get all agents
*AgentsApi* | [**update_agent**](./AgentsApi.md#update_agent) | **PATCH** /agent/{id} | Update an agent
*CallsApi* | [**start_outbound_call**](./CallsApi.md#start_outbound_call) | **POST** /conversation/outbound | Start an outbound call
*CampaignsApi* | [**create_campaign**](./CampaignsApi.md#create_campaign) | **POST** /campaign | Create a campaign
*CampaignsApi* | [**delete_campaign**](./CampaignsApi.md#delete_campaign) | **DELETE** /campaign/{id} | Delete a campaign
*CampaignsApi* | [**get_campaign_by_id**](./CampaignsApi.md#get_campaign_by_id) | **GET** /campaign/{id} | Get a campaign
*CampaignsApi* | [**get_campaigns**](./CampaignsApi.md#get_campaigns) | **GET** /campaign | Retrieve all campaigns
*CampaignsApi* | [**pause_campaign**](./CampaignsApi.md#pause_campaign) | **POST** /campaign/{id}/pause | Pause a campaign
*CampaignsApi* | [**start_campaign**](./CampaignsApi.md#start_campaign) | **POST** /campaign/{id}/start | Start a campaign
*KnowledgeBaseApi* | [**create_knowledge_base**](./KnowledgeBaseApi.md#create_knowledge_base) | **POST** /knowledgebase | Create a knowledge base
*KnowledgeBaseApi* | [**delete_knowledge_base**](./KnowledgeBaseApi.md#delete_knowledge_base) | **DELETE** /knowledgebase/{id} | Delete a knowledge base
*KnowledgeBaseApi* | [**delete_knowledge_base_item**](./KnowledgeBaseApi.md#delete_knowledge_base_item) | **DELETE** /knowledgebase/{knowledgeBaseId}/items/{knowledgeBaseItemId} | Delete a knowledge base item
*KnowledgeBaseApi* | [**get_knowledge_base_by_id**](./KnowledgeBaseApi.md#get_knowledge_base_by_id) | **GET** /knowledgebase/{id} | Get a knowledge base
*KnowledgeBaseApi* | [**get_knowledge_base_items**](./KnowledgeBaseApi.md#get_knowledge_base_items) | **GET** /knowledgebase/{id}/items | Get all knowledge base items
*KnowledgeBaseApi* | [**get_knowledge_bases**](./KnowledgeBaseApi.md#get_knowledge_bases) | **GET** /knowledgebase | Get all knowledge bases
*KnowledgeBaseApi* | [**upload_media_to_knowledge_base**](./KnowledgeBaseApi.md#upload_media_to_knowledge_base) | **POST** /knowledgebase/{id}/items/upload-media | Upload a media to a knowledge base
*KnowledgeBaseApi* | [**upload_text_to_knowledge_base**](./KnowledgeBaseApi.md#upload_text_to_knowledge_base) | **POST** /knowledgebase/{id}/items/upload-text | Upload a text to a knowledge base
*LogsApi* | [**get_conversation_logs**](./LogsApi.md#get_conversation_logs) | **GET** /conversation/{id} | Get conversation logs
*OrganizationApi* | [**get_organization**](./OrganizationApi.md#get_organization) | **GET** /organization | Get organization details
*UserApi* | [**get_current_user**](./UserApi.md#get_current_user) | **GET** /user | Get user details