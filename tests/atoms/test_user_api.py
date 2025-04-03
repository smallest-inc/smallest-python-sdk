from smallestai.atoms.models.get_current_user200_response import GetCurrentUser200Response

def test_get_current_user(atoms_client):
    response = atoms_client.user_api.get_current_user()
    assert isinstance(response, GetCurrentUser200Response) 