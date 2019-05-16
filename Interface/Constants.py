from enum import Enum

class AccessType(Enum): 
	NONE = 0
	READ = 1
	WRITE = 2
	ADMIN = 3
