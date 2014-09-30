# Snakewater PUP Identifier (PUP.PY)
# Copyright Alex Yancey & Meanberg Design 2014
# Version 1.0
# Developed in Ettlin AP CS Period 1

# Information = 0
# Nuance = 1
# Suspicion = 2
# Confirmed_Detection = 3
# Cause_for_Alarm = 4

pups = []

def add(readable_name, det_type, percentage, resolution = None, file_location = None, regkey = None):
	pups.append({readable_name, det_type, percentage, resolution, file_location, regkey})