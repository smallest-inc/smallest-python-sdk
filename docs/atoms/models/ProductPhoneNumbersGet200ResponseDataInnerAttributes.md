# ProductPhoneNumbersGet200ResponseDataInnerAttributes

Additional attributes of the phone number

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider** | **str** | The telephony provider | [optional] 
**phone_number** | **str** | The actual phone number | [optional] 

## Example

```python
from atoms.models.product_phone_numbers_get200_response_data_inner_attributes import ProductPhoneNumbersGet200ResponseDataInnerAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of ProductPhoneNumbersGet200ResponseDataInnerAttributes from a JSON string
product_phone_numbers_get200_response_data_inner_attributes_instance = ProductPhoneNumbersGet200ResponseDataInnerAttributes.from_json(json)
# print the JSON string representation of the object
print(ProductPhoneNumbersGet200ResponseDataInnerAttributes.to_json())

# convert the object into a dict
product_phone_numbers_get200_response_data_inner_attributes_dict = product_phone_numbers_get200_response_data_inner_attributes_instance.to_dict()
# create an instance of ProductPhoneNumbersGet200ResponseDataInnerAttributes from a dict
product_phone_numbers_get200_response_data_inner_attributes_from_dict = ProductPhoneNumbersGet200ResponseDataInnerAttributes.from_dict(product_phone_numbers_get200_response_data_inner_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


