# UnauthorizedErrorReponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**errors** | **List[str]** |  | [optional] 

## Example

```python
from smallestai.atoms.models.unauthorized_error_reponse import UnauthorizedErrorReponse

# TODO update the JSON string below
json = "{}"
# create an instance of UnauthorizedErrorReponse from a JSON string
unauthorized_error_reponse_instance = UnauthorizedErrorReponse.from_json(json)
# print the JSON string representation of the object
print(UnauthorizedErrorReponse.to_json())

# convert the object into a dict
unauthorized_error_reponse_dict = unauthorized_error_reponse_instance.to_dict()
# create an instance of UnauthorizedErrorReponse from a dict
unauthorized_error_reponse_from_dict = UnauthorizedErrorReponse.from_dict(unauthorized_error_reponse_dict)
```



