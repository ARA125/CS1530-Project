import uuid
class User:
  def __init__(self, uniqe_id, username, name, profile_info):
    self.id = unique_id
    self.name = name
    self.username = username
    self.profile_info = profile_info

class Event:
  def __init__(self, event_name, type, start_time, end_time):
    self.event_id = uuid.uuid4()
    self.event_name = event_name
    self.start_time = start_time
    self.end_time = end_time

  def change_time(self,n_start_time, n_end_time):
  	self.start_time = n_start_time
  	self.end_time = n_end_time

class Calendar: 
  def __init__(self):
    self.calendar_id = uuid.uuid4()
    self.events = []

class Group:
  def __init__(self, admin_name, admin_id):
    self.group_id = uuid.uuid4()
    self.group_name = "untitled"
    self.admin_id = admin_id
    self.admin_name = admin_name
    self.calendar = Calendar()

  def rename(self, new_name):
  	self.group_name = new_name

  def change_admin(self, new_admin_name, new_admin_id):
  	self.admin_id = new_admin_id
  	self.admin_name = new_admin_name