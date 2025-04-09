import os
import time
import pytest
import requests
from dotenv import load_dotenv
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.configuration import Configuration
import uuid

GLOBAL_STATE = {}

def create_knowledge_bases(base_url, headers):
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

    resp = requests.get(
        f"{base_url}/knowledgebase/{base_knowledge_base_id}/items",
        headers=headers
    )
    resp.raise_for_status()
    items = resp.json()["data"]
    if len(items) < 1:
        raise Exception("Expected at least 1 knowledge base items")
    
    temp_item_id = items[0]["_id"]

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
            "slmModel": "electron-v1",
            "globalKnowledgeBaseId": knowledge_base_id
        }
    )
    print(resp.json())
    resp.raise_for_status()
    base_agent_id = resp.json()["data"]
    time.sleep(0.2)

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
            "slmModel": "electron-v1",
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

            resp = requests.get(f"{base_url}/audience", headers=headers)
            resp.raise_for_status()
            time.sleep(0.2)
            audience_data = resp.json()
            audience_id = audience_data["data"][0]["_id"]
            
            return {"id": audience_id}
        except Exception:
            print("Error creating audience")

def create_campaign(base_url, headers):
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
    load_dotenv()
    
    api_key = os.getenv("SMALLEST_API_KEY")
    base_url = "https://atoms-api.dev.smallest.ai/api/v1"
    # base_url = "http://localhost:4001/api/v1"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        knowledge_bases = create_knowledge_bases(base_url, headers)
        agents = create_agents(base_url, headers, knowledge_bases["base"]["id"])
        audience = create_audience(base_url, headers)
        base_agent_template = fetch_agent_template(base_url, headers)
        
        # temps are created for deletion testing
        GLOBAL_STATE.update({
            "base_knowledge_base": knowledge_bases["base"],
            "temp_knowledge_base_item_id": knowledge_bases["base"]["temp_item"]["id"],
            "temp_knowledge_base": knowledge_bases["temp"],
            "base_agent": agents["base"],
            "temp_agent": agents["temp"],
            "audience": audience,
            "base_agent_template": base_agent_template
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
    config = Configuration(
        host="https://atoms-api.dev.smallest.ai/api/v1"
    )
    return AtomsClient(configuration=config)

@pytest.fixture
def global_state():
    return GLOBAL_STATE 