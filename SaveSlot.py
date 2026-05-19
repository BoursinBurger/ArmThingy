import re
import datetime


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

    @staticmethod
    def camel_case_to_snake_case(string: str) -> str:
        return ''.join(['_' + i.lower() if i.isupper() else i for i in string]).lstrip('_')

    def __init__(self, kwargs):

        int_to_string = ["currentAnastasiaHelmetId", "currentAnastasiaTorsoId", "currentAnastasiaGloveId",
                         "currentKnausHelmetId", "currentKnausTorsoId", "currentKnausGloveId"]

        int_lists = ["completedMissions", "missionsShownInWarRoom", "seenCutscenes",
                     "unlockedChallengeMissions", "permanentPickups"]

        arrays = ["missionStats", "equipmentState"]

        for key, value in kwargs.items():
            attr = self.camel_case_to_snake_case(key)
            if attr is not None:

                match key:
                    # Parse ISO-format string into DateTime
                    case "dateModified":
                        setattr(self, attr, datetime.datetime.fromisoformat(value))

                    # Parse "HH:MM:SS.mmmmmmm" into TimeDelta
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

                    # Convert int to str
                    case item if item in int_to_string:
                        setattr(self, attr, str(value))

                    # Convert list of int to list of str
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
