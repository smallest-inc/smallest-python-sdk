import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import atoms

# Configuration
API_KEY = os.environ.get("API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2N2U1MjFjOGZlZTk3MzY2NjcwMDM3MmQiLCJpYXQiOjE3NDMwNjk2NDB9.EPizbqQLuxrx4HirxyouldzoD6ggnYSS_h0H38m0F8M")
AGENT_ID = os.environ.get("AGENT_ID", "67e663bffaec7a78253c9e32")
PHONE_NUMBERS = os.environ.get("PHONE_NUMBERS", "1234567890,9876543210").split(",")
TARGET_PHONE_NUMBER = os.environ.get("TARGET_PHONE_NUMBER", "+919769384457")

# Setup API client
# configuration = Configuration(
#     host="http://localhost:4001/api/v1",
# )

# api_client = ApiClient()
print(os.environ.get("SMALLEST_API_KEY"))

# Initialize API instances
agents_api = atoms.AgentsApi()
knowledge_base_api = atoms.KnowledgeBaseApi()
calls_api = atoms.CallsApi()

def main():
    try:
        # Step 1: Fetch the agent by ID
        print(f"Fetching agent with ID: {AGENT_ID}")
        agent = agents_api.get_agent_by_id(id=AGENT_ID).data
        print(f"Agent name: {agent.name}")
        
        # Get the global knowledge base ID from the agent
        global_knowledge_base_id = agent.global_knowledge_base_id
        if not global_knowledge_base_id:
            print("Error: Agent does not have a global knowledge base ID")
            return
        
        print(f"Global knowledge base ID: {global_knowledge_base_id}")
        
        # Step 2: Add items to the knowledge base
        print("Adding items to the knowledge base...")
        
        # Example knowledge items
        knowledge_items = [
            {
                "title": "Product Information",
                "content": "Our flagship product is a smart home assistant that can control lights, temperature, and security systems."
            },
            {
                "title": "Pricing Details",
                "content": "Basic plan: $9.99/month. Premium plan: $19.99/month. Enterprise plan: Contact sales for custom pricing."
            },
            {
                "title": "Support Hours",
                "content": "Our customer support team is available Monday through Friday, 9 AM to 6 PM Eastern Time."
            }
        ]
        
        # Upload each knowledge item
        for item in knowledge_items:
            upload_request = {
                "title": item["title"],
                "content": item["content"]
            }
            
            response = knowledge_base_api.upload_text_to_knowledge_base(
                id=global_knowledge_base_id,
                upload_text_to_knowledge_base_request=upload_request
            )
            
            print(f"Added knowledge item: {item['title']}")
        
        # Step 3: Make an outbound call
        print(f"\nInitiating outbound call to {TARGET_PHONE_NUMBER}...")
        
        call_request = {
            "agent_id": AGENT_ID,
            "phone_number": TARGET_PHONE_NUMBER,
        }
        
        call_response = calls_api.start_outbound_call(
            start_outbound_call_request=call_request
        )
        
        print(f"Call initiated successfully!")
        print(f"Call ID: {call_response.id}")
        print(f"Status: {call_response.data.call_id}")
        
        print("\nScript execution completed successfully")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
