from requests import get
import json

class Version:
    def __init__(self,_json):
        self.raw_json = _json
        self.loaders = _json["loaders"]
        self.game_version = _json["game_versions"]
        self.name = _json["name"]
        self.version_number = _json["version_number"]
        self.type = _json["version_type"]
        self.changelog = _json["changelog"]
        self.files = _json["files"]

class Project:
    def __init__(self,_json,_web):
        self.url = _web
        self.raw_json = _json
        self.project_id = _json["id"]
        self.slug = _json["slug"]
        self.project_type = _json["project_type"]
        self.title = _json["title"]
        self.team_id = _json["team"]
        self.desc = _json["description"]
        self.body = _json["body"]
        self.uploaded = _json["published"]
        self.last_update = _json["updated"]
        self.approved = _json["approved"]
        self.downloads = _json["downloads"]
        self.followers = _json["followers"]
        self.categories = _json["categories"]
        self.loaders = _json["loaders"]
        self.versions = _json["versions"]
        self.client_side = _json["client_side"]
        self.server_side = _json["server_side"]
        self.game_versions = _json["game_version"]
        self.icon = _json["icon_url"]
    
    def update(self):
        _json = json.loads(get(f"https://api.modrinth.com/v2/project/{self.project_id}").text)
        self.raw_json = _json
        self.project_id = _json["id"]
        self.slug = _json["slug"]
        self.project_type = _json["project_type"]
        self.title = _json["title"]
        self.team_id = _json["team"]
        self.desc = _json["description"]
        self.body = _json["body"]
        self.uploaded = _json["published"]
        self.last_update = _json["updated"]
        self.approved = _json["approved"]
        self.downloads = _json["downloads"]
        self.followers = _json["followers"]
        self.categories = _json["categories"]
        self.loaders = _json["loaders"]
        self.versions = _json["icon_url"]
        self.client_side = _json["client_side"]
        self.server_side = _json["server_side"]
        self.game_versions = _json["game_version"]
        self.icon = _json["icon_url"]

class Search_Project:
    def __init__(self,_json,_web):
        self.url = _web
        self.raw_json = _json
        self.project_id = _json["project_id"]
        self.slug = _json["slug"]
        self.project_type = _json["project_type"]
        self.title = _json["title"]
        self.desc = _json["description"]
        self.downloads = _json["downloads"]
        self.categories = _json["categories"]
        self.versions = _json["icon_url"]
        self.client_side = _json["client_side"]
        self.server_side = _json["server_side"]
    
    def get_full(self):
        out = get(self.url + "/project/" + self.project_id)
        if out.status_code == 404:
            raise ConnectionError("404 Error: Project Not found")
        else:
            return Project(json.loads(out.text),self.url)
        

class Modrinth:
    def __init__(self,website="https://api.modrinth.com/v2"):
        self.url = website
    def search_projects(self,query,limit=10,offset=0):
        out = get(self.url + "/search",params={"query":query,"limit":limit,"offset":offset})
        jsonout = json.loads(out.text)
        returnlist = []
        for i in jsonout["hits"]:
            returnlist.append(Search_Project(i,self.url))
        return returnlist
    
    def get_project(self,idorsslug):
        out = get(self.url + "/project/" + idorsslug)
        if out.status_code == 404:
            raise ConnectionError("404 Error: Project Not found")
        else:
            return Project(json.loads(out.text),self.url)