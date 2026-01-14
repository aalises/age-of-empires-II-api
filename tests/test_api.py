import pytest
from api.models.factory import get_model

def getEntries(filename):
    with open(filename) as f:
        return sum(1 for line in f) - 1  # Discard header

def test_create_instances(client):
        instance_civ = get_model("civilizations", ("ExampleCiv", "Age of Kings", "Archers",
                                                   "Sample Unit", "Sample Tech", "BonusTeam",
                                                   "CivBonus"))

        instance_unit = get_model("units", ("SampleUnit", "description", "expansion", "age",
                                            "created_in", "{'cost': 'null'}", 34, 0.4, 0.3, 0.94, 3, 1000,
                                            "1-8", 10, "3/4", None, None, None, None, None))

        instance_strct = get_model("structures", ("AmazingStructure", "expansion", "age",
                                   "{'cost':'null'}", 30, 1000, 5, "3/4", "1-8", None, None, None))

        instance_tech = get_model("technologies", ("GroundbreakingTech", "expansion", "age", "develops_in",
                                  "{'cost': 'null'}", 30, "Someone", "description"))

        assert instance_civ is not None and repr(instance_civ) == "<Civilization: ExampleCiv>"
        assert instance_unit is not None and repr(instance_unit) == "<Unit: SampleUnit>"
        assert instance_strct is not None and repr(instance_strct) == "<Structure: AmazingStructure>"
        assert instance_tech is not None and repr(instance_tech) == "<Technology: GroundbreakingTech>"

def test_all_data_returned(client):
    """Check that all the data is parsed correctly from the database"""

    data_all_civ = client.get('/api/v1/civilizations').get_json()["civilizations"]
    data_all_unit = client.get('/api/v1/units').get_json()["units"]
    data_all_strct = client.get('/api/v1/structures').get_json()["structures"]
    data_all_tech = client.get('/api/v1/technologies').get_json()["technologies"]

    assert len(data_all_civ) == getEntries("data/civilizations.csv")
    assert len(data_all_unit) == getEntries("data/units.csv")
    assert len(data_all_strct) == getEntries("data/structures.csv")
    assert len(data_all_tech) == getEntries("data/technologies.csv")

def test_civilizations(client):
    data_id = client.get('/api/v1/civilization/4').get_json()
    data_name = client.get('/api/v1/civilization/byzantines').get_json()
    data_name2 = client.get('/api/v1/civilization/Teutons').get_json()

    assert data_id["name"] == "Celts"
    assert data_name["army_type"] == "Defensive"
    assert data_name2["team_bonus"] == "Units are more resistant to conversion"


def test_units(client):
    data_id = client.get('/api/v1/unit/34').get_json()
    data_name = client.get('/api/v1/unit/archer').get_json()
    data_name2 = client.get('/api/v1/unit/teutonic_knight').get_json()

    assert data_id["name"] == "Elite Longboat"
    assert data_name["description"] == "Quick and light. Weak at close range; excels at battle from distance"
    assert data_name2["armor"] == "5/2"

def test_structures(client):
    data_id = client.get('/api/v1/structure/4').get_json()
    data_name = client.get('/api/v1/structure/castle').get_json()
    data_name2 = client.get('/api/v1/structure/bombard-tower').get_json()

    assert data_id["name"] == "Fish Trap"
    assert data_name["hit_points"] == 4800
    assert data_name2["range"] == "1-8"

def test_technologies(client):
    data_id = client.get('/api/v1/technology/34').get_json()
    data_name = client.get('/api/v1/technology/heated_shot').get_json()
    data_name2 = client.get('/api/v1/technology/herbal-medicine').get_json()

    assert data_id["name"] == "Spies"
    assert data_name["expansion"] == "Age of Kings"
    assert data_name2["description"] == "Garrisoned Units 4x healing speed"

def test_resources_not_found(client):
    """ Test the error messages when not found """

    civ_not_found = client.get('/api/v1/civilization/34').get_json()["message"]
    unit_not_found = client.get('/api/v1/unit/space_destroyer').get_json()["message"]
    tech_not_found = client.get('/api/v1/technology/speed_lasagna_cooking').get_json()["message"]
    strct_not_found = client.get('/api/v1/structure/statue_of_liberty').get_json()["message"]

    assert civ_not_found == 'Civilization not found'
    assert unit_not_found == 'Unit not found'
    assert tech_not_found == 'Technology not found'
    assert strct_not_found == 'Structure not found'
