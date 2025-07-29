import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.organization_get200_response import OrganizationGet200Response

def test_get_organization(atoms_client):
    response = atoms_client.get_organization()
    assert isinstance(response, OrganizationGet200Response) 