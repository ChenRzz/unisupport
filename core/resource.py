from repo.resourceRepo import ResourceRepository
from model.resource import ResourceType

class ResourceService:
    def __init__(self, resource_repo: ResourceRepository):
        self.resource_repo = resource_repo

    def get_all_majors(self):
        pass

    def get_major_resources(self, major_id: int):
        pass

