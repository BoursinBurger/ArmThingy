import re
import datetime
from ArmThingyFunctions import camel_case_to_snake_case


class SaveSlot:
    current_version: int
    date_modified: datetime.datetime
    time_spent: datetime.timedelta
    completed_missions: list[str]
    missions_shown_in_war_room: list[str]
    mission_stats: dict[str, dict[str, int]]
    seen_cutscenes: list[str]
    seen_dialogues: list[str]
    currency: int
    num_challenge_coins: int
    unlocked_challenge_missions: list[str]
    equipment_state: dict[str, int]
    rescued_orphans: list[str]
    permanent_pickups: list[str]
    current_anastasia_helmet_id: str
    current_anastasia_torso_id: str
    current_anastasia_glove_id: str
    current_knaus_helmet_id: str
    current_knaus_torso_id: str
    current_knaus_glove_id: str
    unlocked_equipment: list[str]

    def __init__(self, json_dict):
        """
        Serializes save slot dictionary into a SaveSlot object.
        :param json_dict: Dictionary containing save slot data
        """

        # Dictionary keys with integer values that need to be converted to strings
        int_to_string = ["currentAnastasiaHelmetID", "currentAnastasiaTorsoID", "currentAnastasiaGloveID",
                         "currentKnausHelmetID", "currentKnausTorsoID", "currentKnausGloveID"]

        # Dictionary keys with integer lists that need to be converted to string lists
        int_lists = ["completedMissions", "missionsShownInWarRoom", "seenCutscenes",
                     "unlockedChallengeMissions", "permanentPickups"]

        # Dictionary keys with array structure that need to be converted to a simpler dictionary
        arrays = ["missionStats", "equipmentState"]

        for key, value in json_dict.items():
            # Convert the key to snake_case so it can be set to its appropriate object attribute
            attr = camel_case_to_snake_case(key)

            # Select the method for importing the key value into the object depending on the key
            match key:
                # Parse ISO-format string into a DateTime
                case "dateModified":
                    setattr(self, attr, datetime.datetime.fromisoformat(value))

                # Parse "HH:MM:SS.mmmmmmm" string into a TimeDelta
                # (Once again, they use 7 digits of precision for milliseconds and Python only supports 6. Sorry.)
                case "timeSpent":
                    timedelta_expression = r"(?P<hrs>\d{2}):(?P<mins>\d{2}):(?P<secs>\d{2})\.(?P<ms>\d{7})"
                    match = re.search(timedelta_expression, value)
                    if match:
                        hrs = int(match.group('hrs'))
                        mins = int(match.group('mins'))
                        secs = int(match.group('secs'))
                        ms = int(match.group('ms'))
                        setattr(self, attr,
                                datetime.timedelta(hours=hrs, minutes=mins, seconds=secs, microseconds=ms))
                    else:
                        setattr(self, attr, None)

                # Convert int value to str
                case item if item in int_to_string:
                    setattr(self, attr, str(value))

                # Convert list of int values to list of str
                case item if item in int_lists:
                    setattr(self, attr, [str(v) for v in value])

                # Extract "array" from dict, then flatten list of dicts to one dict
                case item if item in arrays:
                    array_dict = {}
                    array = value.get("array")
                    for key_value_dict in array:
                        array_dict[str(key_value_dict["Key"])] = key_value_dict["Value"]
                    setattr(self, attr, array_dict)

                # Remaining attributes are stored as is
                case _:
                    setattr(self, attr, value)
