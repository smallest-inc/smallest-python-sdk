# AudienceIdMembersSearchGet200ResponseDataSearchInfo

Information about the search performed

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**search_type** | **str** | The type of search performed | [optional] 
**search_term** | **str** | The search term(s) used | [optional] 
**search_fields** | **List[str]** | The specific fields searched (for field-specific searches) | [optional] 
**total_results** | **int** | The number of results returned | [optional] 

## Example

```python
from atoms.models.audience_id_members_search_get200_response_data_search_info import AudienceIdMembersSearchGet200ResponseDataSearchInfo

# TODO update the JSON string below
json = "{}"
# create an instance of AudienceIdMembersSearchGet200ResponseDataSearchInfo from a JSON string
audience_id_members_search_get200_response_data_search_info_instance = AudienceIdMembersSearchGet200ResponseDataSearchInfo.from_json(json)
# print the JSON string representation of the object
print(AudienceIdMembersSearchGet200ResponseDataSearchInfo.to_json())

# convert the object into a dict
audience_id_members_search_get200_response_data_search_info_dict = audience_id_members_search_get200_response_data_search_info_instance.to_dict()
# create an instance of AudienceIdMembersSearchGet200ResponseDataSearchInfo from a dict
audience_id_members_search_get200_response_data_search_info_from_dict = AudienceIdMembersSearchGet200ResponseDataSearchInfo.from_dict(audience_id_members_search_get200_response_data_search_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


