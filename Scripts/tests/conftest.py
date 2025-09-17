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


def pytest_collection_modifyitems(config, items):
    cmdopt = config.getoption("--cmdopt")
    run_only_sim = pytest.mark.skip(reason=f"Skipped by --cmdopt {cmdopt}")
    for item in items:
        if cmdopt not in item.keywords:
            item.add_marker(run_only_sim)


# Pytest GLOBAL FIXTURES
# -------------------------------------------------------------------

SIM_MAP = {
    "sim1": "Simulations.1",
    "sim2": "Simulations.2",
    "adddata": "Simulations.AddData",
    "nodata": None,
}

@pytest.fixture(autouse=True, scope="function")
def header_function_scope(request):
    # Find which marker is set on this test
    sim_key = None
    for key in SIM_MAP:
        if request.node.get_closest_marker(key):
            sim_key = key
            break

    # Fallback to cmdopt if no marker present
    if sim_key is None:
        cmdopt = getattr(request.config.option, "cmdopt", None)
        if cmdopt in SIM_MAP:
            sim_key = cmdopt
        else:
            sim_key = "nodata"

    # Set env
    data_root = os.path.join(os.path.dirname(__file__), "Data")
    os.environ["NMLDB_DATA_PATH"] = data_root
    sim_dir = SIM_MAP[sim_key]
    if sim_dir is not None:
        os.environ["NMLDB_SIMU_PATH"] = os.path.join(data_root, sim_dir)
    else:
        os.environ.pop("NMLDB_SIMU_PATH", None)

    # Force fresh import of DatabankLib
    for name in list(sys.modules):
        if name == "DatabankLib" or name.startswith("DatabankLib."):
            del sys.modules[name]
    importlib.invalidate_caches()
    import DatabankLib  # noqa: F401

    print(f"DBG: Using dataset {sim_key} -> {os.getenv('NMLDB_SIMU_PATH')}")

    yield

    print("DBG: Mocking completed")


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
