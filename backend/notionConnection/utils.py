import os
import requests
from dotenv import load_dotenv
import concurrent.futures
import urllib.request

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
            childBlocks = []
            for childblock in childList:
                id = childblock["id"]
                childBlocks.append(self.getAllChildren(id))
            data["childrenblock"] = childList
        return data 
    
    #Return the block with specified block_id and all of its children inside the 'childrenblock' property.
    def getAllChildrenAsync(self, block_id):
        endpoint =  "https://api.notion.com/v1/blocks/" + block_id
        data = self.getRequest(endpoint)
        if(data['has_children']):
            childList = self.getBlockChildrenId(block_id)["results"]
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                # Start the load operations and mark each future with its URL
                future_task = {executor.submit(self.getAllChildrenAsync, childList[i]["id"] ) : i for i in range(len(childList))}
                for future in concurrent.futures.as_completed(future_task):
                    childblock_id = future_task[future]
                    try:
                        #This should be thread safe since each thread access different ids. So no race conditions.
                        childList[childblock_id] = future.result()

                    except Exception as exc:
                        print('%r generated an exception: %s' % (childList[childblock_id]["id"], exc))
                    else:
                        print('%r page is %d bytes' % (childList[childblock_id]["id"], len(data)))
    
            data["childrenblock"] = childList
        return data 
    

    def getAllChildrenAsyncWrong(self, block_id):
        endpoint =  "https://api.notion.com/v1/blocks/" + block_id
        print("requesting", block_id)
        data = self.getRequest(endpoint)
        if(data['has_children']):
            childList = self.getBlockChildrenId(block_id)["results"]
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                # Start the load operations and mark each future with its URL
                future_task = {executor.submit(self.getAllChildrenAsyncWrong, childblock["id"] ) :childblock for childblock in childList}
                for future in concurrent.futures.as_completed(future_task):
                    childblock = future_task[future]
                    try:
                        childblock["childrenblock"] = future.result()

                    except Exception as exc:
                        print('%r generated an exception: %s' % (childblock["id"], exc))
                    else:
                        print('%r page is %d bytes' % (childblock["id"], len(data)))
    
            data["childrenblock"] = childList
        return data 
# We can use a with statement to ensure threads are cleaned up promptly




                

    