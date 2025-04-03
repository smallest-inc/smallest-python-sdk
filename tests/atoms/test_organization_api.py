from smallestai.atoms.models.get_organization200_response import GetOrganization200Response

def test_get_organization(atoms_client):
    response = atoms_client.organization_api.get_organization()
    assert isinstance(response, GetOrganization200Response) 