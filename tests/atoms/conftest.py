import os
import time
import pytest
import requests
from dotenv import load_dotenv
from smallestai.atoms.atoms_client import AtomsClient
import uuid

# Global state to share across tests
GLOBAL_STATE = {}

def create_knowledge_bases(base_url, headers):
    """Create test knowledge bases"""
    # Create base knowledge base
    resp = requests.post(
        f"{base_url}/knowledgebase",
        headers=headers,
        json={
            "name": "Test Knowledge Base",
            "description": "Knowledge base for testing"
        }
    )
    resp.raise_for_status()
    base_knowledge_base_id = resp.json()["data"]
    time.sleep(0.2)

    # Add base knowledge base item
    resp = requests.post(
        f"{base_url}/knowledgebase/{base_knowledge_base_id}/items/upload-text",
        headers=headers,
        json={
            "title": "Test Knowledge Base Item",
            "content": "This is a test knowledge base item",
        }
    )
    resp.raise_for_status()
    time.sleep(0.2)

    # Add temporary knowledge base item for delete testing
    resp = requests.post(
        f"{base_url}/knowledgebase/{base_knowledge_base_id}/items/upload-text",
        headers=headers,
        json={
            "title": "Temporary Test Knowledge Base Item",
            "content": "This is a temporary test knowledge base item",
        }
    )
    resp.raise_for_status()
    time.sleep(0.2)

    # Get items to fetch their IDs
    resp = requests.get(
        f"{base_url}/knowledgebase/{base_knowledge_base_id}/items",
        headers=headers
    )
    resp.raise_for_status()
    items = resp.json()["data"]
    if len(items) < 1:
        raise Exception("Expected at least 1 knowledge base items")
    
    temp_item_id = items[0]["_id"]

    # Create temporary knowledge base for delete test
    resp = requests.post(
        f"{base_url}/knowledgebase",
        headers=headers,
        json={
            "name": "Temporary Knowledge Base",
            "description": "Temporary knowledge base for delete testing"
        }
    )
    resp.raise_for_status()
    time.sleep(0.2)
    
    return {
        "base": {
            "id": base_knowledge_base_id,
            "temp_item": {"id": temp_item_id}
        },
        "temp": {
            "id": resp.json()["data"]
        }
    }

def create_agents(base_url, headers, knowledge_base_id):
    """Create test agents"""
    # Create base agent
    resp = requests.post(
        f"{base_url}/agent",
        headers=headers,
        json={
            "name": "Test Agent",
            "description": "Base agent for testing",
            "language": {
                "enabled": "en",
                "switching": False
            },
            "synthesizer": {
                "voiceConfig": {
                    "model": "waves_lightning_large",
                    "voiceId": "nyah"
                },
                "speed": 1.2,
                "consistency": 0.5,
                "similarity": 0,
                "enhancement": 1
            },
            "slmModel": "atoms-slm-v1",
            "globalKnowledgeBaseId": knowledge_base_id
        }
    )
    resp.raise_for_status()
    base_agent_id = resp.json()["data"]
    time.sleep(0.2)

    # Create temporary agent for delete test
    resp = requests.post(
        f"{base_url}/agent",
        headers=headers,
        json={
            "name": "Temporary Test Agent",
            "description": "Temporary agent for delete testing",
            "language": {
                "enabled": "en",
                "switching": False
            },
            "synthesizer": {
                "voiceConfig": {
                    "model": "waves_lightning_large",
                    "voiceId": "nyah"
                },
                "speed": 1.2,
                "consistency": 0.5,
                "similarity": 0,
                "enhancement": 1
            },
            "slmModel": "atoms-slm-v1",
            "globalKnowledgeBaseId": knowledge_base_id
        }
    )
    resp.raise_for_status()
    temp_agent_id = resp.json()["data"]
    time.sleep(0.2)
    
    return {
        "base": {"id": base_agent_id},
        "temp": {"id": temp_agent_id}
    }

def create_audience(base_url, headers):
    """Create test audience"""
    # Open and upload the audience template CSV file
    csv_path = os.path.join(os.path.dirname(__file__), "audience_template.csv")
    with open(csv_path, "rb") as file:
        files = {
            "file": ("audience_template.csv", file, "text/csv")
        }
        data = {
            "phoneNumberColumnName": "phoneNumber",
            "identifierColumnName": "Name",
            "name": "test_audience"
        }
        try:
            resp = requests.post(
                f"{base_url}/audience",
                headers=headers,
                files=files,
                data=data
            )
            resp.raise_for_status()
            time.sleep(0.2)

            # Get the first audience ID from the list
            resp = requests.get(f"{base_url}/audience", headers=headers)
            resp.raise_for_status()
            time.sleep(0.2)
            audience_data = resp.json()
            audience_id = audience_data["data"][0]["_id"]
            
            return {"id": audience_id}
        except Exception:
            # Silently ignore any errors during audience creation
            print("Error creating audience")

def create_campaign(base_url, headers):
    """Create test campaigns"""
    # Create base campaign
    resp = requests.post(
        f"{base_url}/campaign",
        headers=headers,
        json={
            "name": f"Test {uuid.uuid4().hex[:8]}",
            "description": "Base campaign for testing",
            "agentId": GLOBAL_STATE["base_agent"]["id"],
            "audienceId": GLOBAL_STATE["audience"]["id"]
        }
    )
    resp.raise_for_status()
    base_campaign_id = resp.json()["data"]["_id"]
    time.sleep(0.2)

    resp = requests.post(
        f"{base_url}/campaign",
        headers=headers,
        json={
            "name": f"Temporary Test {uuid.uuid4().hex[:8]}",
            "description": "Temporary campaign for delete testing",
            "agentId": GLOBAL_STATE["base_agent"]["id"],
            "audienceId": GLOBAL_STATE["audience"]["id"]
        }
    )
    resp.raise_for_status()
    temp_campaign_id = resp.json()["data"]["_id"]
    time.sleep(0.2)
    
    return {
        "base": {"id": base_campaign_id},
        "temp": {"id": temp_campaign_id}
    }

def fetch_agent_template(base_url, headers):
    """Fetch agent templates and return first template ID"""
    resp = requests.get(
        f"{base_url}/agent/template",
        headers=headers
    )
    resp.raise_for_status()
    templates = resp.json()["data"]
    if not templates:
        raise Exception("No agent templates found")
    return {"id": templates[0]["id"]}

def start_call(base_url, headers):
    """Start a test outbound call"""
    resp = requests.post(
        f"{base_url}/conversation/outbound",
        headers=headers,
        json={
            "agentId": GLOBAL_STATE["base_agent"]["id"],
            "phoneNumber": "+919666666666"
        }
    )
    resp.raise_for_status()
    base_call_id = resp.json()["data"]["conversationId"]
    time.sleep(0.2)
    
    return {
        "base": {"id": base_call_id}
    }

def pytest_configure(config):
    """Global setup before any test collection"""
    load_dotenv()
    
    api_key = os.getenv("SMALLEST_API_KEY")
    base_url = "https://atoms-api.dev.smallest.ai/api/v1"
    # base_url = "http://localhost:4001/api/v1"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # Create resources
        knowledge_bases = create_knowledge_bases(base_url, headers)
        agents = create_agents(base_url, headers, knowledge_bases["base"]["id"])
        audience = create_audience(base_url, headers)
        ref_template = fetch_agent_template(base_url, headers)
        
        # Store in global state
        GLOBAL_STATE.update({
            "base_knowledge_base": knowledge_bases["base"],
            "temp_knowledge_base_item_id": knowledge_bases["base"]["temp_item"]["id"],
            "temp_knowledge_base": knowledge_bases["temp"],
            "base_agent": agents["base"],
            "temp_agent": agents["temp"],
            "audience": audience,
            "ref_template": ref_template
        })
        
        campaign = create_campaign(base_url, headers)
        GLOBAL_STATE.update({
            "base_campaign": campaign["base"],
            "temp_campaign": campaign["temp"]
        })

        call = start_call(base_url, headers)
        GLOBAL_STATE.update({
            "base_call": call["base"]
        })
        
    except Exception as e:
        raise Exception(f"Global test setup failed: {str(e)}")

@pytest.fixture
def atoms_client():
    """Fixture to provide AtomsClient instance"""
    return AtomsClient()

@pytest.fixture
def global_state():
    """Fixture to access global state"""
    return GLOBAL_STATE 