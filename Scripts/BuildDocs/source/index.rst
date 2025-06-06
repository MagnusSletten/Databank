.. NMRlipids databank documentation master file, created by
   sphinx-quickstart on Mon Sep  4 12:07:48 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NMRlipids databank's documentation!
==============================================

NMRlipids databank is a community-driven catalogue containing atomistic MD simulations of biologically relevant lipid membranes emerging from the `NMRlipids open collaboration <http://nmrlipids.blogspot.com/>`_. 


NMRlipids databank is an overlay databank.
------------------------------------------
Each databank entry is a simulation described by the README.yaml file which contains all the essential information for the data upcycling and reuse. This includes the information about permanent location of each simulation file, but raw data is located in distributed locations outside the NMRlipids databank. The content of README.yaml files is described in `User input and content of README.yaml files <READMEcontent.html>`_. The README.yaml files are stored in the `NMRlipids databank git <https://github.com/NMRLipids/Databank/tree/main/Data/Simulations>`_ in subfolders named based on file hash identities. For details and information about overlay databank structure see the `NMRlipids databank manuscript <https://doi.org/10.26434/chemrxiv-2023-jrpwm>`_.

NMRlipids Databank-GUI
----------------------
`NMRlipids Databank-GUI <https://databank.nmrlipids.fi/>`_ provides easy access to the NMRlipids Databank content
through a graphical user interface (GUI). Simulations can be searched based on their molecular composition, force field,
temperature, membrane properties, and quality; the search results are ranked based on the simulation quality as evaluated
against experimental data when available. Membranes can be visualized, and properties between different simulations and
experiments compared.

NMRlipids Databank-API
----------------------
The NMRlipids Databank-API provides programmatic access to all simulation data in the NMRlipids Databank.
This enables wide range of novel data-driven applications from construction of machine learning models that predict membrane properties, to automatic analysis of virtually
any property across all simulations in the Databank. For examples of novel analyses enabled by the NMRlipids databank API see the `NMRlipids databank manuscript <https://doi.org/10.26434/chemrxiv-2023-jrpwm>`_.

Functions available for simulation analyses are described in :ref:`APIfunctions`.
A project `template <https://github.com/NMRLipids/databank-template>`_ designed to intialize projects that analyse data from NMRlipids databank contains
a `minimum example for looping over available simulations <https://github.com/NMRLipids/databank-template/blob/main/scripts/template.ipynb>`_.
For further examples, see codes that analyze the `area per lipid <https://github.com/NMRLipids/Databank/blob/main/Scripts/AnalyzeDatabank/calcAPL.py>`_,
`C-H bond order parameters <https://github.com/NMRLipids/Databank/blob/main/Scripts/AnalyzeDatabank/calcOrderParameters.py>`_,
`X-ray scattering form factors <https://github.com/NMRLipids/Databank/blob/main/Scripts/AnalyzeDatabank/calc_FormFactors.py>`_,
and `principal component equilibration <https://github.com/NMRLipids/Databank/blob/main/Scripts/AnalyzeDatabank/NMRPCA_timerelax.py>`_.
For these analyses, the universal molecule and atom names are connected to simulation specific names using README.yaml and mapping files
as described in :ref:`molecule_names`.


Adding simulations into the NMRlipids databank
------------------------------------

The NMRlipids Databank is open for additions of simulation data by anyone. For detailed instructions to add new data, to update databank analyses and run quality evaluations, see :ref:`addData`. Quick and minimal steps to add a new simulation are here:

#. Add trajectory and topology (tpr for Gromacs, pdb or corresponding to other programs) file into a `Zenodo <https://zenodo.org/>`_ repository.

#. Create an `info.yaml` file containing the essential information on your simulation by filling the `template <https://github.com/NMRLipids/Databank/blob/development/Scripts/BuildDatabank/info_files/info.yaml>`_. For instructions, see :ref:`readmecontent` and `examples <https://github.com/NMRLipids/Databank/tree/main/Scripts/BuildDatabank/info_files>`_. Mapping files are described in  :ref:`molecule_names` and are available from `here <https://github.com/NMRLipids/Databank/tree/main/Scripts/BuildDatabank/mapping_files>`_ .

#. Save the created `info.yaml` file into a new directory with the next free integer into `Scripts/BuildDatabank/info_files/ <https://github.com/NMRLipids/Databank/tree/main/Scripts/BuildDatabank/info_files>`_ folder in the NMRlipids databank git and make a pull request to the main branch.

Do not hesitate to ask assistance via `GitHub issues <https://github.com/NMRLipids/Databank/issues>`_.

Adding experimental data into the NMRlipids databank
---------------------------
Instrutions are available at :ref:`addingExpData`.

System requirements
-------------------

The code has been tested in Linux environment with python 3.7 or newer and recent `Gromacs <https://manual.gromacs.org/current/install-guide/index.html>`_ version installed.

Setup using conda as distribution:

.. code-block:: bash

    conda create --name databank python==3.7 MDAnalysis
    conda activate databank
    (databank) pip install -e .


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   listOfFiles
   READMEcontent
   addingData
   addingExpData
   moleculesAndMapping
   databankLibrary
   exampleAndTutorials
   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
