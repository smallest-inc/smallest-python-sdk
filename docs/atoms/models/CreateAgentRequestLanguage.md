# CreateAgentRequestLanguage

Language configuration for the agent. You can enable or disable language switching for the agent. This will be used to determine the language of the agent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **str** | The language of the agent. You can choose from the list of supported languages. | [optional] 
**switching** | **bool** | Whether to enable language switching for the agent. If enabled, the agent will be able to switch between languages based on the user&#39;s language. | [optional] [default to False]
**synthesizer** | [**CreateAgentRequestLanguageSynthesizer**](CreateAgentRequestLanguageSynthesizer.md) |  | [optional] 
**speed** | **float** |  | [optional] [default to 1.2]
**consistency** | **float** |  | [optional] [default to 0.5]
**similarity** | **float** |  | [optional] [default to 0]
**enhancement** | **float** |  | [optional] [default to 1]

## Example

```python
from smallestai.atoms.models.create_agent_request_language import CreateAgentRequestLanguage

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAgentRequestLanguage from a JSON string
create_agent_request_language_instance = CreateAgentRequestLanguage.from_json(json)
# print the JSON string representation of the object
print(CreateAgentRequestLanguage.to_json())

# convert the object into a dict
create_agent_request_language_dict = create_agent_request_language_instance.to_dict()
# create an instance of CreateAgentRequestLanguage from a dict
create_agent_request_language_from_dict = CreateAgentRequestLanguage.from_dict(create_agent_request_language_dict)
```



