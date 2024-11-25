from DatabankLib.core import initialize_databank 

"""
Contains methods used for python scripts related to workflows. 
"""


#In order to get a consistent order of readme.yaml files we use sorting based on the ID.
def sorted_databank():
    systems = list(initialize_databank())
    systems.sort(key=lambda x: x['ID'])
    return systems

