from smallestai.atoms.models.get_organization200_response_data import GetOrganization200ResponseData

def test_get_organization(atoms_client):
    response = atoms_client.get_organization()
    assert isinstance(response, GetOrganization200ResponseData) 