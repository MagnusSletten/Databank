#!/bin/bash
git checkout $BRANCH_NAME
git pull
cd /app/Databank/Scripts/tests/ &&
source /usr/local/gromacs/bin/GMXRC &&
pytest vs