import json
from Interface.Utilities import Utilities
from Interface.Entity import Entity

class Organization(Entity):

	def __init__(self, tier:int, admin_id:str, data:dict):
		super(Organization, self).__init__(tier, data)
		self.data["general"]["admin_id"] = admin_id

