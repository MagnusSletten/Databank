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
    "sim2": "Simulations.2",
    "adddata": "Simulations.AddData",
    "nodata": None,
     "sim1": "Simulations.1",
}
@pytest.fixture(autouse=True, scope="module")
def header_module_scope(request):
    # pick sim from marker or cmdopt (your existing logic is fine)
    cmdopt = getattr(request.config.option, "cmdopt", "nodata")
    sim = {
        "sim1": "Simulations.1",
        "sim2": "Simulations.2",
        "adddata": "Simulations.AddData",
        "nodata": None,
    }.get(cmdopt, None)

    tests_dir = os.path.dirname(__file__)
    data_root = os.path.join(tests_dir, "Data")

    # 🔑 root + data must be set BEFORE import
    os.environ["NMLDB_ROOT_PATH"] = tests_dir
    os.environ["NMLDB_DATA_PATH"] = data_root
    if sim is not None:
        os.environ["NMLDB_SIMU_PATH"] = os.path.join(data_root, sim)
    else:
        os.environ.pop("NMLDB_SIMU_PATH", None)

    # clean re-import so DatabankLib picks up new env
    for name in list(sys.modules):
        if name == "DatabankLib" or name.startswith("DatabankLib."):
            del sys.modules[name]
    importlib.invalidate_caches()
    import DatabankLib  # noqa: F401

    print("DBG env -> ROOT:", os.getenv("NMLDB_ROOT_PATH"))
    print("DBG env -> DATA:", os.getenv("NMLDB_DATA_PATH"))
    print("DBG env -> SIMU:", os.getenv("NMLDB_SIMU_PATH"))
    yield


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
