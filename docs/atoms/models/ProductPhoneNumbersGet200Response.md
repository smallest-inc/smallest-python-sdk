# ProductPhoneNumbersGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**data** | [**List[ProductPhoneNumbersGet200ResponseDataInner]**](ProductPhoneNumbersGet200ResponseDataInner.md) |  | [optional] 

## Example

```python
from atoms.models.product_phone_numbers_get200_response import ProductPhoneNumbersGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ProductPhoneNumbersGet200Response from a JSON string
product_phone_numbers_get200_response_instance = ProductPhoneNumbersGet200Response.from_json(json)
# print the JSON string representation of the object
print(ProductPhoneNumbersGet200Response.to_json())

# convert the object into a dict
product_phone_numbers_get200_response_dict = product_phone_numbers_get200_response_instance.to_dict()
# create an instance of ProductPhoneNumbersGet200Response from a dict
product_phone_numbers_get200_response_from_dict = ProductPhoneNumbersGet200Response.from_dict(product_phone_numbers_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


