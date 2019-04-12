import os
import json

freelancerFile = './exercise/freelancer.json'
if not os.path.isfile(freelancerFile):
    print("File does not exists")
    
with open(freelancerFile) as f:
    data = json.load(f)
    
    # compute all skills duration

	# output result

