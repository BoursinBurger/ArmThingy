"""
Tests for SaveSlot
"""


def test_save_obj_types():
    """Test the SaveSlot class's ability to parse a dictionary into the correct types of objects."""
    from SaveSlot import SaveSlot
    from datetime import datetime, timedelta
    input_dict = {
        "currentVersion": 1,
        "dateModified": "2026-05-18T21:15:00.6431925-04:00",
        "timeSpent": "02:43:39.0861335",
        "completedMissions": [
            1,
            2,
            3,
        ],
        "missionsShownInWarRoom": [
            1,
            2,
            3,
        ],
        "missionStats": {
            "array": [
                {
                    "Key": 1,
                    "Value": {
                        "bestTime": 1.23456789,
                        "maxEnemiesDefeated": 1
                    }
                },
                {
                    "Key": 2,
                    "Value": {
                        "bestTime": 2.345678901,
                        "maxEnemiesDefeated": 2
                    }
                },
            ]
        },
        "seenCutscenes": [
            1,
            2,
            3,
        ],
        "seenDialogues": [
            "1234567890abcdef",
            "8badf00d",
            "deadbeef",
        ],
        "currency": 100,
        "numChallengeCoins": 50,
        "unlockedChallengeMissions": [
            1,
            2,
            3,
        ],
        "equipmentState": {
            "array": [
                {
                    "Key": 3,
                    "Value": 0
                },
                {
                    "Key": 4,
                    "Value": 4
                }
            ]
        },
        "rescuedOrphans": [],
        "permanentPickups": [
            1,
            2,
            3,
        ],
        "currentAnastasiaHelmetID": 1,
        "currentAnastasiaTorsoID": 2,
        "currentAnastasiaGloveID": 3,
        "currentKnausHelmetID": 4,
        "currentKnausTorsoID": 5,
        "currentKnausGloveID": 6,
        "unlockedEquipment": []
    }

    slot = SaveSlot(input_dict)

    assert slot.current_version == 1
    assert slot.date_modified == datetime.fromisoformat("2026-05-18T21:15:00.6431925-04:00")
    assert slot.time_spent == timedelta(hours=2, minutes=43, seconds=39, microseconds=861335)
    assert slot.completed_missions == ["1", "2", "3"]
    assert slot.missions_shown_in_war_room == ["1", "2", "3"]
    assert slot.mission_stats == {"1": {"bestTime": 1.23456789, "maxEnemiesDefeated": 1},
                                  "2": {"bestTime": 2.345678901, "maxEnemiesDefeated": 2}}
    assert slot.seen_cutscenes == ["1", "2", "3"]
    assert slot.seen_dialogues == ["1234567890abcdef", "8badf00d", "deadbeef"]
    assert slot.currency == 100
    assert slot.num_challenge_coins == 50
    assert slot.unlocked_challenge_missions == ["1", "2", "3"]
    assert slot.equipment_state == {"3": 0, "4": 4}
    assert slot.rescued_orphans == []
    assert slot.permanent_pickups == ["1", "2", "3"]
    assert slot.current_anastasia_helmet_id == "1"
    assert slot.current_anastasia_torso_id == "2"
    assert slot.current_anastasia_glove_id == "3"
    assert slot.current_knaus_helmet_id == "4"
    assert slot.current_knaus_torso_id == "5"
    assert slot.current_knaus_glove_id == "6"
    assert slot.unlocked_equipment == []
