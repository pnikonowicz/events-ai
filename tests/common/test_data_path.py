import os

from common.paths import DataPath, Paths


def test_data_path_with_explicit_base_dir_resolves_under_working_data():
    assert DataPath("today", Paths.TEMP_LOCAL_DIR).dir() == os.path.join(
        Paths.TEMP_LOCAL_DIR,
        "today",
    )


def test_data_path_default_base_dir_resolves_under_data():
    assert DataPath("today").dir() == os.path.join(Paths.DATA_DIR, "today")
