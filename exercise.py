import os
import sys
import json
from datetime import datetime

def get_months(rang):
    """Get number of months between two datetimes."""
    (start, end) = rang
    return (end.year - start.year) * 12 + end.month - start.month

def in_between(x, start, end):
    """Checks if a datetime is between two datetimes."""
    return x > start and x < end

def process_data(data):
    """Calculates the number of months of experience for each skill and dumps it into a json file."""
    skill_ranges = {}
    result = {}
    computed_skills = []
    # if the dictionnary contains necessary keys to have the result
    if "freelance" in data and "id" in data["freelance"]:
        if "professionalExperiences" in data["freelance"]:
            # get professionalExperiences
            professionalExperiences = data["freelance"]["professionalExperiences"]
            # loop on professionalExperiences
            for experience in professionalExperiences:
                # parse strings to get start datetime and end datetime
                start_date_time = datetime.strptime(experience["startDate"], "%Y-%m-%dT%H:%M:%S%z")
                end_date_time = datetime.strptime(experience["endDate"], "%Y-%m-%dT%H:%M:%S%z")
                # here we create a new structure with every technology
                # {skill: (id:id, skill: skill), [(start_date_time1, end_date_time1), ..]}
                for skill in experience["skills"]:
                    key = (skill["id"], skill["name"])
                    if key in skill_ranges:
                        skill_ranges [key].append((start_date_time, end_date_time))
                    else:
                        skill_ranges [key] = [(start_date_time, end_date_time)]
            # for each skill we're going to transform the linked linked_segments
            # a segment is a date skill_ranges and two linked segmets are segments that overlap
            # we add fist segment to linked_segments and then we check if new segment ovelaps,
            # if so, we update the start and/or end of this segment and we add it to linked_segments
            # and we do that for all skills
            # finally, we calculate the number of months in all ranges in linked_segments
            for skill in skill_ranges:
                linked_segments = []
                for (start, end) in skill_ranges[skill]:
                    if linked_segments == []:
                        linked_segments.append((start, end))
                    else:
                        for (seg_start, seg_end) in linked_segments:
                            if in_between(start, seg_start, seg_end):
                                start = seg_end
                            if in_between(end, seg_start, seg_end):
                                end = seg_start
                        linked_segments.append((start, end))
                total_experience = 0
                for seg in linked_segments:
                    total_experience += get_months(seg)
                # we prepare the object to return
                (id, name) = skill
                computed_skills.append({"id" : id, "name": name, "durationInMonths" : total_experience})
        return { "freelance" : {"id" : data["freelance"]["id"], "computed_skills" : computed_skills}}
    return {}

def write_result(result, path):
    """write the result into a file"""
    with open(path, 'w') as fp:
        json.dump(result, fp ,indent=4)

def main():
    try:
        freelancerFile = './exercise/freelancer.json'
        result_file = "./result.json"
        if not os.path.isfile(freelancerFile):
            print("File does not exists")

        with open(freelancerFile) as f:
            data = json.load(f)
        result = process_data(data)
        if result != {}:
            write_result(result, result_file)
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
