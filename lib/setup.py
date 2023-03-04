from speech import say
# FIXME: Get correct import statement
# from recognition import . . . 

DAYS_OF_THE_WEEK = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

def setup_week():
    config = {
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
    },
    "PILLS": []
    }
    say("Thank you for choosing BUZZ as your trusted personal helper.")
    say("We are going to start setup now.")
    for i in range(7):
        day = config["SCHEDULE"][DAYS_OF_THE_WEEK[i]]
        
        say("Do you take any medication on " + DAYS_OF_THE_WEEK[i] + "?")
        # voice recigntion yes or no
        if True:
            say("What medication do you take on " + DAYS_OF_THE_WEEK[i] + "?")
            # voice recigntion pills into list
            pills = ["advil", "tylenol", "xanax"]
            for pill in pills:
                say("What time do you take " + pill + "?")
                # voice recigntion time 
                time = "03:07"
                # TODO: Convert time to 24 hour format
                day["PILLS"].append([time, pill])
        
        say("Do you have a trainer on " + DAYS_OF_THE_WEEK[i] + "?")
        if True:
            say("What time does your trainer come on " + DAYS_OF_THE_WEEK[i] + "?")
            # voice recigntion time 
            time = "03:07"
            
            # TODO: Have GPT generate workouts
            workouts = [1, 4, 77]
            
            day["TRAINER"].append([time, workouts])
        
        

def setup_day(day_of_week):
    '''
    day_of_week =  
         "MONDAY" : {
            "PILLS" : [[0, []]],
            "TRAINER": [[0, []]],
             "THERAPIST" : [[0]]
         } 
    '''
    tempArray = day_of_week["PILLS"].copy()
    tempArray.append(day_of_week["TRAINER"].copy())
    tempArray.append(day_of_week["THERAPIST"].copy())

    [event.insert(1, "PILLS") for event in tempArray]
    return sorted(tempArray)

def modify_week(schedule, day_of_week):
    '''
    schedule = 
        "MONDAY": {
            "PILLS": [[0, ["advil", "tylenol", "xanax"]]],
            "TRAINER": [[0, []]],
            "THERAPIST": [[0]]
        },
        "TUESDAY": {
            "PILLS": [[0, []]],
            "TRAINER": [[0, []]],
            "THERAPIST": [[0]]
        }
        .
        .
        .
    '''