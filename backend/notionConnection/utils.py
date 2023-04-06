import os
import requests
from dotenv import load_dotenv

class NotionClient:
    #Initializes
    def __init__(self, api_key = None, api_version="2021-08-16"):
        """
        Initializes client for notion connection. Requires api_key. If unspecified, 
        default to the one in the environment variable "NOTION_API_KEY"
        """
        self.api_key = api_key
        self.api_version = api_version
        
        if(self.api_key is None):
            load_dotenv()
            self.api_key = os.getenv("NOTION_API_KEY")

        self.headers = {
            "Notion-Version": self.api_version,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def getRequest(self, endpoint):
        '''
         Wrapper to do get request by  providing the endpoint.
        '''
        response = requests.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
    def getBlock(self, block_id):
        '''
            Get data(metadata) for a Block.
        '''
        endpoint = "https://api.notion.com/v1/blocks/" + block_id
        return self.getRequest(endpoint)
    
    def getBlockChildrenId(self, block_id):
        endpoint = f"https://api.notion.com/v1/blocks/{block_id}/children"
        return self.getRequest(endpoint)
    
    def getAllChildren(self, block_id):
        """
            Recursively retrieve all children of the specified block_id. 
            Adds the property 'childrenblock' which contains the children blocks. 
            Might parallelize retrieval of children since the children are all independent (I assume)
        """
        endpoint =  "https://api.notion.com/v1/blocks/" + block_id
        data = self.getRequest(endpoint)
        if(data['has_children']):
            childList = self.getBlockChildrenId(block_id)["results"]
            for childblock in childList:
                id = childblock["id"]
                childblock["childrenblock"] = self.getAllChildren(id)
            data["childrenblock"] = childList
        return data 


                

    