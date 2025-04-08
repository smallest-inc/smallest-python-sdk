# UpdateAgentRequestLanguage

Language configuration for the agent. You can enable or disable language switching for the agent. This will be used to determine the language of the agent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **str** | The language of the agent. You can choose from the list of supported languages. | [optional] 
**switching** | **bool** | Whether to enable language switching for the agent. If enabled, the agent will be able to switch between languages based on the user&#39;s language. | [optional] [default to False]

## Example

```python
from smallestai.atoms.models.update_agent_request_language import UpdateAgentRequestLanguage

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAgentRequestLanguage from a JSON string
update_agent_request_language_instance = UpdateAgentRequestLanguage.from_json(json)
# print the JSON string representation of the object
print(UpdateAgentRequestLanguage.to_json())

# convert the object into a dict
update_agent_request_language_dict = update_agent_request_language_instance.to_dict()
# create an instance of UpdateAgentRequestLanguage from a dict
update_agent_request_language_from_dict = UpdateAgentRequestLanguage.from_dict(update_agent_request_language_dict)
```



