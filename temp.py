import requests

secret = "JjN8Q~p3oa5e3_tJUiyk2ibuI9gRXXvLNRM5scNs"
client_id = "64c08e53-c64c-4dd5-979e-dc1dd7808555"
tenant_id = "70e6cc59-a0d5-478a-b8b9-678cce2e3a63"

def get_token():
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": secret,
        "scope": "https://analysis.windows.net/powerbi/api/.default"
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get token: {response.status_code} {response.text}")

def get_workspaces():
    url = "https://api.powerbi.com/v1.0/myorg/admin/groups?$top=1000"
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        raise Exception(f"Failed to get workspaces: {response.status_code} {response.text}")
    
def get_artifacts(workspace_id: str):
    """Returns the list of items or artifacts in a Microsoft Fabric workspace."""
    base_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items"
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        raise Exception(f"Failed to get artifacts: {response.status_code} {response.text}")
    
def create_folder(display_name: str, workspace_id: str):
    """Creates a folder in the Microsoft Fabric workspace."""
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders"
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }
    data = {
        "displayName": display_name,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to create folder: {response.status_code} {response.text}") 

create_folder("Bronze","858abbe1-f958-443b-bdcd-5e0d3b1cd7c9")



