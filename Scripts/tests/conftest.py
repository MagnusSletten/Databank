import importlib
import os
import pytest
import logging
import os

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

@pytest.fixture(autouse=True, scope="module")
def header_module_scope(request):
    # 1) Prefer dataset markers on this test module
    sim_key = None
    for key in ("sim1", "sim2", "adddata", "nodata"):
        if request.node.get_closest_marker(key):
            sim_key = key
            break

    # 2) Fallback to --cmdopt (if provided and known)
    if sim_key is None:
        cmdopt = getattr(request.config.option, "cmdopt", None)
        if cmdopt in SIM_MAP:
            sim_key = cmdopt
        else:
            # default if nothing specified
            sim_key = "nodata"

    # 3) Set env before (re)import
    data_root = os.path.join(os.path.dirname(__file__), "Data")
    os.environ["NMLDB_DATA_PATH"] = data_root
    sim_dir = SIM_MAP[sim_key]
    if sim_dir is not None:
        os.environ["NMLDB_SIMU_PATH"] = os.path.join(data_root, sim_dir)
    else:
        os.environ.pop("NMLDB_SIMU_PATH", None)

    # 4) Clean re-import so module sees the fresh env
    for name in list(sys.modules):
        if name == "DatabankLib" or name.startswith("DatabankLib."):
            del sys.modules[name]
    importlib.invalidate_caches()
    import DatabankLib  # noqa: F401

    print("DBG env -> NMLDB_DATA_PATH:", os.getenv("NMLDB_DATA_PATH"))
    print("DBG env -> NMLDB_SIMU_PATH:", os.getenv("NMLDB_SIMU_PATH"))

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
