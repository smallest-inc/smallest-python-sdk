# ProductPhoneNumbersGet200ResponseDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique identifier for the phone number | [optional] 
**is_active** | **bool** | Whether the phone number is active | [optional] 
**attributes** | [**ProductPhoneNumbersGet200ResponseDataInnerAttributes**](ProductPhoneNumbersGet200ResponseDataInnerAttributes.md) |  | [optional] 
**created_at** | **datetime** | The date and time when the phone number was created | [optional] 
**updated_at** | **datetime** | The date and time when the phone number was last updated | [optional] 

## Example

```python
from atoms.models.product_phone_numbers_get200_response_data_inner import ProductPhoneNumbersGet200ResponseDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of ProductPhoneNumbersGet200ResponseDataInner from a JSON string
product_phone_numbers_get200_response_data_inner_instance = ProductPhoneNumbersGet200ResponseDataInner.from_json(json)
# print the JSON string representation of the object
print(ProductPhoneNumbersGet200ResponseDataInner.to_json())

# convert the object into a dict
product_phone_numbers_get200_response_data_inner_dict = product_phone_numbers_get200_response_data_inner_instance.to_dict()
# create an instance of ProductPhoneNumbersGet200ResponseDataInner from a dict
product_phone_numbers_get200_response_data_inner_from_dict = ProductPhoneNumbersGet200ResponseDataInner.from_dict(product_phone_numbers_get200_response_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


