from typing import Any
from mcp.server.fastmcp import FastMCP
import requests

# Initialize FastMCP server
mcp = FastMCP("fabric-mcp")

#constants
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
    
@mcp.tool(name="list_workspaces")
def get_workspaces():
    """Returns the list of Microsoft Fabric workspaces."""
    base_url = "https://api.powerbi.com/v1.0/myorg/admin/groups"
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }

    all_results = []
    top = 5000
    skip = 0

    while True:
        url = f"{base_url}?$top={top}&$skip={skip}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to get workspaces: {response.status_code} {response.text}")

        data = response.json().get("value", [])
        if not data:
            break 

        all_results.extend(data)
        skip += top  

    return all_results

@mcp.tool(name="list_workspace_items")
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

@mcp.tool(name="create_folder")
def create_folder(display_name: str, workspace_id: str) -> Any:
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

@mcp.tool(name="delete_folder")
def delete_folder(folder_id: str, workspace_id: str):
    """Deletes a folder in the Microsoft Fabric workspace."""
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/folders/{folder_id}"
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        return {"message": "Folder deleted successfully"}   
    
@mcp.tool(name="create_item")
def create_item(display_name: str, workspace_id: str, folder_id: str,type:str) -> Any:
    """Creates an item in the Microsoft Fabric workspace."""
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items"
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }
    data = {
        "displayName": display_name,
        "type": type,  
        "folderId": folder_id
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to create item: {response.status_code} {response.text}")

@mcp.tool(name="delete_item")
def delete_item(item_id: str, workspace_id: str):
    """Deletes an item in the Microsoft Fabric workspace."""
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}"
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        return {"message": "Item deleted successfully"}
    else:
        raise Exception(f"Failed to delete item: {response.status_code} {response.text}")
    
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

