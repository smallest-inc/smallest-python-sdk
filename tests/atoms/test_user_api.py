import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.user_get200_response import UserGet200Response

def test_get_current_user(atoms_client):
    response = atoms_client.get_current_user()
    assert isinstance(response, UserGet200Response)