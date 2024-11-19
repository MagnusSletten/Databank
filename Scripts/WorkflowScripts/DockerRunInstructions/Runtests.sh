#!/bin/bash
git checkout $BRANCH_NAME
git pull
<<<<<<< HEAD
cd /app/Databank/Scripts/tests/ &&
source /usr/local/gromacs/bin/GMXRC &&
pytest vs
=======
cd Scripts/tests/ &&
source /usr/local/gromacs/bin/GMXRC &&
pytest -vs
>>>>>>> dev_pipeline_compose
