from dotenv import load_dotenv
from pathlib import Path
import os
import requests

dotenv_path = Path('backend/.env')
load_dotenv(dotenv_path)
token = os.getenv('token')
version = os.getenv('version')

def parse(data):
    if (data["object"] == "list"):
        return parse_list(data["results"])

def parse_list(data):
    list = []
    for i in data:
        if (i["type"] in ["heading_1", "heading_2", "heading_3"]):
            list.append(parse_heading(i))
        elif (i["type"] == "paragraph"):
            list.append(parse_paragraph(i))
        elif (i["type"] == "bulleted_list_item"):
            list.append(parse_bullet_list(i))
        elif (i["type"] == "table"):
            list.append(parse_table(i))
        elif (i["type"] == "image"):
            list.append(parse_image(i))
        elif (i["type"] == "text"):
            list.append(parse_text(i))
        elif (i["type"] == "quote"):
            list.append(parse_quote(i))
        elif (i["type"] == "numbered_list_item"):
            list.append(parse_numbered_list_item(i))
        elif (i["type"] == "file"):
            list.append(parse_file(i))
    return list

def parse_numbered_list_item(data):
    result = dict()
    list = []
    result["type"] = "numbered_list_item"
    for i in data["numbered_list_item"]["text"]:
        if (i["plain_text"] != ""):
            list.append(parse_text(i))
    result["type"] = "numbered_list_item"
    result["content"] = list
    return result

def parse_heading(data):
    result = dict()
    result["type"] = "heading"
    result["content"] = data[data["type"]]["text"][0]["plain_text"]
    return result

def parse_paragraph(data):
    list = []
    for i in data["paragraph"]["text"]:
        list.append(parse_text(i))

    result = dict()
    result["type"] = "paragraph"
    result["content"] = list
    return result

def parse_text(data):
    result = dict()
    result["type"] = "text"
    result["content"] = data["plain_text"]

    special_attribute = dict()
    for attribute in data["annotations"]:
        if (attribute != "color" and data["annotations"][attribute] == True):
            special_attribute[attribute] = True

        elif (attribute == "color" and data["annotations"][attribute] != "default"):
            special_attribute[attribute] = data["annotations"][attribute]
        
        if (data["text"]["link"]):
            special_attribute["link"] = data["text"]["link"]["url"]

    return result

def parse_quote(data):
    list = []
    for i in data["quote"]["text"]:
        list.append(parse_text(i))

    result = dict()
    result["type"] = "quote"
    result["content"] = list
    return result

def parse_bullet_list(data):
    result = dict()

    result["type"] = "bulleted_list_item"
    list = []
    for i in data["bulleted_list_item"]["text"]:
        bullet_item = parse_text(i)
        if data["has_children"]:
            url = 'https://api.notion.com/v1/blocks/' + data["id"] + '/children'
            headers = {'Notion-Version': version, 'Authorization': token}
            response = requests.get(url, headers=headers)
            responseData = response.json()
            bullet_item["children"] = parse(responseData)

        list.append(bullet_item)
    result["content"] = list
    return result

def parse_table(data):
    result = dict()
    url = 'https://api.notion.com/v1/blocks/' + data["id"] + '/children'
    headers = {'Notion-Version': version, 'Authorization': token}
    response = requests.get(url, headers=headers)
    table = response.json()
    #Assume that table does not have children inside the block
    list = []
    if "results" in table:
        for i in table["results"]:
            for cell in i["table_row"]["cells"]:
                list.extend(parse_list(cell))
        
    result["type"] = "table_row"
    result["content"] = list
    return result

def parse_image(data):
    result = dict()
    result["type"] = "image"
    imagetype = data[data["type"]]["type"]
    result["content"] = data[data["type"]][imagetype]["url"]
    return result

def parse_file(data):
    result = dict()
    result["type"] = "file"

    # can be external of file type
    type = data["file"]["type"]

    if (type == "external"):
        result["url"] = data["file"]["external"]["url"]
    else:
        result["url"] = data["file"]["file"]["url"]

    return result