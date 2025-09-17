import importlib
import os
import pytest
import logging
import os
import sys
import pytest

# Pytest HOOKS
# -------------------------------------------------------------------


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt",
        action="store",
        default="sim1",
        help="Two test groups: sim1|sim2|nodata",
    )



# Pytest GLOBAL FIXTURES
# -------------------------------------------------------------------
SIM_MAP = {
    "sim1": "Simulations.1",
    "sim2": "Simulations.2",
    "adddata": "Simulations.AddData",
    "nodata": None,
}

@pytest.fixture(autouse=True, scope="module")
def set_root_and_data():
    tests_dir = os.path.dirname(__file__)
    data_root = os.path.join(tests_dir, "Data")
    os.environ["NMLDB_ROOT_PATH"] = tests_dir
    os.environ["NMLDB_DATA_PATH"]  = data_root
    yield

@pytest.fixture(autouse=True, scope="function")
def set_dataset_per_test(request):
    # 1) Prefer explicit marker
    sim_key = next((k for k in SIM_MAP if request.node.get_closest_marker(k)), None)

    # 2) Fallback to --cmdopt (but don't assume sim1)
    if sim_key is None:
        cmdopt = getattr(request.config.option, "cmdopt", None)
        sim_key = cmdopt if cmdopt in SIM_MAP else "nodata"

    # 3) Apply env
    data_root = os.environ["NMLDB_DATA_PATH"]
    sim_dir = SIM_MAP[sim_key]
    if sim_dir is None:
        os.environ.pop("NMLDB_SIMU_PATH", None)
    else:
        os.environ["NMLDB_SIMU_PATH"] = os.path.join(data_root, sim_dir)

    # 4) Clean reimport so this test uses the right env
    for name in list(sys.modules):
        if name == "DatabankLib" or name.startswith("DatabankLib."):
            del sys.modules[name]
    importlib.invalidate_caches()
    import DatabankLib  # noqa: F401

    print(f"DBG dataset -> {sim_key} ({os.getenv('NMLDB_SIMU_PATH')})")


@pytest.fixture(scope="module")
def logger():
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    if not logger.handlers:  # Avoid adding multiple handlers during pytest runs
        logger.addHandler(handler)

    yield logger

    # TEARDOWN: clean up handlers after use
    for handler in logger.handlers:
        logger.removeHandler(handler)
