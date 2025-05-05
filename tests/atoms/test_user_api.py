from smallestai.atoms.models.get_current_user200_response_data import GetCurrentUser200ResponseData

def test_get_current_user(atoms_client):
    response = atoms_client.get_current_user()
    assert isinstance(response, GetCurrentUser200ResponseData) 