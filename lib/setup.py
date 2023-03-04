def setup_week():
    return {
        "SCHEDULE": {
            "MONDAY": {
                "PILLS": [[0, ["advil", "tylenol", "xanax"]]],
                "TRAINER": [[0, []]],
                "THERAPIST": [[0]]
            },
            "TUESDAY": {
                "PILLS": [[0, []]],
                "TRAINER": [[0, []]],
                "THERAPIST": [[0]]
            },
            "WEDNESDAY": {
                "PILLS": [[0, []]],
                "TRAINER": [[0, []]],
                "THERAPIST": [[0]]
            },
            "THURSDAY": {
                "PILLS": [[0, []]],
                "TRAINER": [[0, []]],
                "THERAPIST": [[0]]
            },
            "FRIDAY": {
                "PILLS": [[0, []]],
                "TRAINER": [[0, []]],
                "THERAPIST": [[0]]
            },
            "SATURDAY": {
                "PILLS": [["03:07", ["advil", "tylenol", "xanax"]], ["03:08", ["tylenol", "advil"]]],
                "TRAINER": [[0, []]],
                "THERAPIST": [[0]]
            },
            "SUNDAY": {
                "PILLS": [[0, []]],
                "TRAINER": [[0, []]],
                "THERAPIST": [[0]]
            }
        }
    }

def setup_day(day_of_week):
    '''
    day_of_week =  
         "MONDAY" : {
            "PILLS" : [[0, []]],
            "TRAINER": [[0, []]],
             "THERAPIST" : [[0]]
         } 
    '''
    t = day_of_week["PILLS"].copy()
    [x.insert(1, "pills") for x in t]
    return t