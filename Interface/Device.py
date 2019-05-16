import json
from Interface.Utilities import Utilities
from Interface.Entity import Entity

class Device(Entity):

	def __init__(self, admin_id:str, user_id:str=None, data:dict=None):
		super(Device, self).__init__(data=data)
		self.admin_id = admin_id
		self.data["general"]["admin_id"] = admin_id
		
	def set_user(self, user_id):
		self.user_id = user_id
		self.data["general"]["user_id"] = user_id

	def set_admin(self, admin_id):
		self.admin_id = admin_id
		self.data["general"]["admin_id"] = admin_id
