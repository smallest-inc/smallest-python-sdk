# CreateAgentRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**language** | [**CreateAgentRequestLanguage**](CreateAgentRequestLanguage.md) |  | [optional] 
**global_knowledge_base_id** | **str** | The global knowledge base ID of the agent. You can create a global knowledge base by using the /knowledgebase endpoint and assign it to the agent. The agent will use this knowledge base for its responses. | [optional] 
**slm_model** | **str** | The LLM model to use for the agent. LLM model will be used to generate the response and take decisions based on the user&#39;s query. | [optional] [default to 'atoms-slm-v1']
**default_variables** | **object** | The default variables to use for the agent. These variables will be used if no variables are provided when initiating a conversation with the agent. | [optional] 
**telephony_product_id** | **str** | The telephony product ID of the agent. This is the product ID of the telephony product that will be used to make the outbound call. You can buy telephone number and assign it to the agent. | [optional] 

## Example

```python
from smallestai.atoms.models.create_agent_request import CreateAgentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAgentRequest from a JSON string
create_agent_request_instance = CreateAgentRequest.from_json(json)
# print the JSON string representation of the object
print(CreateAgentRequest.to_json())

# convert the object into a dict
create_agent_request_dict = create_agent_request_instance.to_dict()
# create an instance of CreateAgentRequest from a dict
create_agent_request_from_dict = CreateAgentRequest.from_dict(create_agent_request_dict)
```



