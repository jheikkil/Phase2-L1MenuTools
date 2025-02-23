import pytest


@pytest.fixture
def met_config():
    cfg_plot = {
        "sample": "TT",
        "default_version": "V22",
        "reference_object": {
            "object": "genMetTrue",
            "suffix": "",
            "label": "Gen MET"
        },
        "test_objects": {
            "trackerMET": {
                "suffix": "",
                "label": "Tracker MET"
            },
            "puppiMET": {
                "suffix": "Et",
                "label": "Puppi MET"
            },
        },
        "binning": {"min": 0, "max": 500, "step": 20},
        "trackerMETTruth": [17671, 8214, 6463, 5321, 4212, 3308, 2453, 1811,
                            1146, 759, 482, 307, 261, 154, 93, 73, 61, 32, 22,
                            18, 20, 14, 8, 7],
        "puppiMETTruth": [31222, 14025, 13874, 13621, 11387, 8429, 5670, 3644,
                          2133, 1306, 766, 460, 352, 222, 145, 98, 81, 45, 29,
                          21, 24, 15, 9, 7],
        "genMETTruth": [130238, 51518, 40197, 29181, 18620, 11269, 6729, 3975,
                        2255, 1353, 791, 470, 355, 225, 148, 98, 81, 45, 30,
                        21, 25, 15, 9, 7],
    }
    return cfg_plot
