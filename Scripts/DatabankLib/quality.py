"""
Module `quality` accumulate functions required for major QualityEvaluation script.
TODO: apply comments style
TODO: add tests
TODO: remove code duplication and commented code
"""

from . import *
from .databank_defs import *
from .core import *
from .databankLibrary import loadMappingFile

import re
import decimal as dc
import numpy as np
import scipy.stats
import scipy.signal
import json

lipid_numbers_list = lipids_dict.keys() # should contain all lipid names

class Simulation:
    def __init__(self, readme, OPdata, FFdata, indexingPath):
        self.readme = readme.copy()
        self.OPdata = OPdata #dictionary where key is the lipid type and value is order parameter file
        self.FFdata = FFdata
        self.indexingPath = indexingPath    
        
    def getLipids(self, molecules=lipid_numbers_list):
        lipids = []
        
        for key in self.readme['COMPOSITION'].keys():
            if key in molecules:
                lipids.append(key)
        return lipids
        
    def molarFraction(self, molecule,molecules=lipid_numbers_list): #only for lipids
        sum_lipids = 0
        number = sum(self.readme['COMPOSITION'][molecule]['COUNT']) 
        
        for key in self.readme['COMPOSITION'].keys():
            if key in molecules:
                sum_lipids += sum(self.readme['COMPOSITION'][key]['COUNT'])

        return number / sum_lipids
        
class Experiment:
    pass

################################

#Quality evaluation of simulated data
#Order parameters

def prob_S_in_g(OP_exp: float, exp_error: float, 
                OP_sim: float, op_sim_sd: float) -> float:
    """Main quality function computing the quality value from experimental and 
    simulation OP data.

    Args:
        OP_exp (float): Experimental OP value
        exp_error (float): Experimental error
        OP_sim (float): Simulated OP value
        op_sim_sd (float): Standard deviation from simulation

    Returns:
        float: single-OP quality value or NaN
    """
    # normal distribution N(s, OP_sim, op_sim_sd)
    a = OP_exp - exp_error
    b = OP_exp + exp_error
    
    A = (OP_sim-a)/op_sim_sd
    B = (OP_sim-b)/op_sim_sd
    P_S = scipy.stats.t.sf(B, df=1, loc=0, scale=1) - scipy.stats.t.sf(A, df=1, loc=0, scale=1)
    
    if np.isnan(P_S) :
        return P_S

    #this is an attempt to deal with precision, max set manually to 70
    dc.getcontext().prec = 70
    precise_log = -dc.Decimal(P_S).log10()

    return float(P_S)
    
# quality of molecule fragments
def getFragments(mapping_file):
    mapping_dict = loadMappingFile(mapping_file)
        
    fragments = {} 
    
    for key_m, value in mapping_dict.items():
        key_f = value['FRAGMENT']
        fragments.setdefault(key_f,[]).append(key_m)
                
    # merge glycerol backbone fragment into headgroup fragment  
    if 'glycerol backbone' in fragments.keys() and 'headgroup' in fragments.keys():
        fragments['headgroup'] += fragments['glycerol backbone']
        fragments.pop('glycerol backbone')
            
    return fragments
    
    
def filterCH(fragment_key, fragments):
    re_CH = re.compile(r'M_([GC0-9]*[A-Z0-9]*C[0-9]*H[0-9]*)*([GC0-9]*H[0-9]*)*_M')
    filtered = list(filter(re_CH.match, fragments[fragment_key]))
    return filtered
    
    
def checkForCH(fragment_key, fragments):
    filtered = filterCH(fragment_key, fragments)
    return bool(filtered)
    
def evaluated_percentage(fragments, exp_op_data):
    #C-H bonds only???

    frag_percentage = dict.fromkeys(fragments,0)
    
    for fragment_key in fragments.keys(): #go through fragments
        count_value = 0
        fragment_size = 0
        for key, value in exp_op_data.items():
             if key.split(' ')[0] in fragments[fragment_key]: #check if atom belongs to the fragment
                 fragment_size += 1
                 if not np.isnan(value[0][0]):
                     count_value += 1
        if fragment_size != 0:
            frag_percentage[fragment_key] = count_value / fragment_size
        else:
            frag_percentage[fragment_key] = 0
        
    print('experiment data availability percentage')
    print(frag_percentage)
    
    return frag_percentage


def fragmentQuality(fragments, exp_op_data, sim_op_data):
    p_F = evaluated_percentage(fragments, exp_op_data) # depends on the experiment file what fragments are in this dictionary
    exp_error = 0.02

    fragment_quality = dict.fromkeys(fragments.keys()) # empty dictionary with fragment names as keys
    
    for fragment_key in fragments.keys():
        E_sum = 0
        AV_sum = 0
        try:
            pF = p_F[fragment_key]
        except KeyError: 
            fragment_quality[fragment_key] = np.nan
            continue
        else:
            if p_F[fragment_key] != 0:
                for key_exp, value_exp in exp_op_data.items():
                    if (key_exp.split()[0] in fragments[fragment_key]) and not np.isnan(value_exp[0][0]):
                        OP_exp = value_exp[0][0]
                        try:
                            OP_sim = sim_op_data[key_exp][0]
                        except:
                            continue
                        else:

                            op_sim_STEM=sim_op_data[key_exp][2]
                    
                            #change here if you want to use shitness(TM) scale for fragments. Warning big numbers will dominate
                            # TODO: remove commented
                            # if OP_exp != float("NaN"):
                            QE = prob_S_in_g(OP_exp, exp_error, OP_sim, op_sim_STEM)
                            # print(OP_exp, OP_sim ,QE)
                            # print(QE, 10**(-QE))
                            
                            # print('prob_S')
                            # print(QE)
                            #  if QE >0: 
                            #   if QE == float("NaN"):
                            #    E_sum = E_sum
                            #    if QE == float("inf"): #'Infinity' or QE == 'inf':
                            #         E_sum += 300
                            #         AV_sum += 1
                            #    else:
                            #        print(QE)
                            #        E_sum += prob_S_in_g(OP_exp, exp_error, OP_sim, op_sim_STEM)
                            #        AV_sum += 1
                            E_sum += QE
                            AV_sum += 1
                if AV_sum > 0:
                    E_F = (E_sum / AV_sum)*p_F[fragment_key]
                    fragment_quality[fragment_key] = E_F
                else:
                    fragment_quality[fragment_key] = np.nan
            else:
                fragment_quality[fragment_key] = np.nan
    
    print('fragment quality ', fragment_quality)
    return fragment_quality
        
def fragmentQualityAvg(lipid,fragment_qual_dict,fragments): # handles one lipid at a time
    sums_dict = {}
    
    for doi in fragment_qual_dict.keys():
        for key_fragment in fragment_qual_dict[doi].keys():
            f_value = fragment_qual_dict[doi][key_fragment]
            sums_dict.setdefault(key_fragment,[]).append(f_value)
    
    avg_total_quality = {}
    
    for key_fragment in sums_dict:
        #remove nan values 
        to_be_summed = [x for x in sums_dict[key_fragment] if not np.isnan(x)]
        if to_be_summed:
            avg_value = sum(to_be_summed) / len(to_be_summed)
        else:
            avg_value = np.nan
        avg_total_quality.setdefault(key_fragment,avg_value)
    
    # if average fragment quality exists for all fragments that contain CH bonds then calculate total quality over all fragment quality averages
    if [ x for x in avg_total_quality.keys() if (checkForCH(x, fragments) and not np.isnan(avg_total_quality[x])) or (not checkForCH(x, fragments)) ]:
        list_values = [x for x in avg_total_quality.values() if not np.isnan(x)]
        avg_total_quality['total'] = sum(list_values) / len(list_values)    
    else:
        avg_total_quality['total'] = np.nan

    print("fragment avg")
    print(avg_total_quality)    
    
    return avg_total_quality


def systemQuality(system_fragment_qualities, simulation): # fragments is different for each lipid ---> need to make individual dictionaries
    system_dict = {}
    lipid_dict = {}
    w_nan = []

    for lipid in system_fragment_qualities.keys():
        fragments = getFragments(simulation.readme['COMPOSITION'][lipid]['MAPPING'])
        lipid_dict = dict.fromkeys(system_fragment_qualities[lipid].keys(),0) # copy keys to new dictionary
        
        w = simulation.molarFraction(lipid)

        for key, value in system_fragment_qualities[lipid].items():
            if not np.isnan(value):
                lipid_dict[key] += w*value
            else:
                w_nan.append(1-w) # save 1 - w of a lipid into a list if the fragment quality is nan
   
        system_dict[lipid] = lipid_dict
        
    system_quality = {}
    
    headgroup = 0
    tails = 0
    total = 0
    
    for lipid_key in system_dict:
        for key, value in system_dict[lipid_key].items():
            if key == 'total':
                total += value
            elif key == 'headgroup':
                headgroup += value
            elif key == 'sn-1' or key == 'sn-2':
                tails += value/2
            else:
                tails += value 
    
    if np.prod(w_nan) > 0:       
        system_quality['headgroup'] = headgroup * np.prod(w_nan) # multiply all elements of w_nan and divide the sum by the product
        system_quality['tails'] = tails * np.prod(w_nan) 
        system_quality['total'] = total * np.prod(w_nan)
    else:
        system_quality['headgroup'] = headgroup
        system_quality['tails'] = tails
        system_quality['total'] = total
        
    print("system_quality")    
    print(system_quality)
     
    return system_quality

#        if lipid != 'CHOL':    # SHOULD BE CHANGED TO WORK ALSO WITH OTHER LIPIDS WITHOUT HEAD AND TAILS THAN CHOLESTEROL
#            for key, value in system_fragment_qualities[lipid].items():
#                if value != 'nan':
#                    if key == 'headgroup':
#                        headgroup.append(w * value)
#                    elif key == 'sn-1':
#                        sn1.append(w * value)
#                    elif key == 'sn-2':
#                        sn2.append(w * value)
#                    elif key == 'total':
#                        total.append(w * value)
#                    else:
#                        continue
#                else:
#                    w_nan.append(1-w) # save 1 - w of a lipid into a list if the fragment quality is nan
#        else:
#            for key, value in system_fragment_qualities[lipid].items():
#                 if value != 'nan':
#                     if key == 'total':
#                         total.append(w * value)
#    #print(headgroup,sum(headgroup), np.prod(w_nan), w_nan)
#    out_dict['headgroup'] = sum(headgroup) * np.prod(w_nan) # multiply all elements of w_nan and divide the sum by the product
#    out_dict['sn-1'] = sum(sn1) * np.prod(w_nan)
#    out_dict['sn-2'] = sum(sn2) * np.prod(w_nan)
#    out_dict['total'] = sum(total) * np.prod(w_nan)

    ## EXTREMELY DIRTY FIX FOR WORKSHOP, SHOULD BE IMPROVED LATER
#    for lipid in system_fragment_qualities.keys():
#        w = simulation.molarFraction(lipid)
#        if lipid != 'CHOL':    
#            for key, value in system_fragment_qualities[lipid].items():                        
#                if value == 'nan':
#                   if key == 'headgroup':
#                       headgroup[:] = [x / (1-w) for x in headgroup]
#                   elif key == 'sn-1':
#                       sn1[:] = [x / (1-w) for x in sn1] 
#                   elif key == 'sn-2':
#                       sn2[:] = [x / (1-w) for x in sn2] 
#                   elif key == 'total':
#                       total[:] = [x / (1-w) for x in total]
#                else:
#                    continue

                         
#    out_dict['headgroup'] = sum(headgroup)
#    out_dict['sn-1'] = sum(sn1)
#    out_dict['sn-2'] = sum(sn2)
#    out_dict['total'] = sum(total)

#    return out_dict

    
 
#Form factor quality


# SAMULI: This one did not work because simulation and experimental data does not start at the same x-axis value.
#         I have commented out. A new version is below. It reads a array which already has a correct array of simulation and experimental data.



#def calc_k_e(simFFdata,expFFdata):
#    """Scaling factor as defined by Kučerka et al. 2008b, doi:10.1529/biophysj.107.122465  """
#    sum1 = 0
#    sum2 = 0
    
#   # print("simulation:" + str(len(simFFdata)))
#   # print("experiment:" + str(len(expFFdata)))
   
#    if len(expFFdata) <= len(simFFdata):
#        for i in range(0,len(expFFdata)): #experiment should contain less data points
#            F_s = simFFdata[i][1]
#            F_e = expFFdata[i][1]
#            deltaF_e = expFFdata[i][2]
        
#            sum1 = sum1 + np.abs(F_s)*np.abs(F_e)/(deltaF_e**2)
#            sum2 = sum2 + np.abs(F_e)**2 / deltaF_e**2
#        k_e = sum1 / sum2
#        return k_e
    
#    else:
#        return ""


def calc_k_e(SimExpData):
    
    """Scaling factor as defined by Kučerka et al. 2008b, doi:10.1529/biophysj.107.122465  """
    sum1 = 0
    sum2 = 0
    
    for data in SimExpData:
        F_e = data[1]
        deltaF_e = data[2]
        F_s = data[3]
        
        sum1 = sum1 + np.abs(F_s)*np.abs(F_e)/(deltaF_e**2)
        sum2 = sum2 + np.abs(F_e)**2 / deltaF_e**2
        k_e = sum1 / sum2

    if len(SimExpData) > 0:
        return k_e
    else:
        return ""

def FormFactorMinFromData(FormFactor):
    FFtmp = []
    for i in FormFactor:
        FFtmp.append(-i[1])

    try:
        w = scipy.signal.savgol_filter(FFtmp, 31, 1)
    except ValueError as e:
        print("FFtmp:")
        print(FFtmp)
        raise e

    minX = []

    peak_ind = scipy.signal.find_peaks(w)

    for i in peak_ind[0]:
        if FormFactor[i][0] > 0.1:
            minX.append(FormFactor[i][0])

    print(minX)
    return(minX)
    
def formfactorQuality(simFFdata, expFFdata):
    """Calculate form factor quality for a simulation as defined by Kučerka et al. 2010, doi:10.1007/s00232-010-9254-5 """

    # SAMULI: This creates a array containing experiments and simualtions with the overlapping x-axis values
    SimExpData = []   
    for SimValues in simFFdata:
        for ExpValues in expFFdata:
            if np.abs(SimValues[0]-ExpValues[0]) < 0.0005: # and ExpValues[0] < 0.41:
                SimExpData.append([ExpValues[0], ExpValues[1], ExpValues[2], SimValues[1]])

    # Calculates the scaling factor for plotting
    k_e = calc_k_e(SimExpData)

    SimMin = FormFactorMinFromData(simFFdata)
    ExpMin = FormFactorMinFromData(expFFdata)

    SQsum = (SimMin[0]-ExpMin[0])**2
    khi2 = np.sqrt(SQsum)*100
    N = len(SimExpData)

    print(SimMin, ExpMin, khi2)
    
    if N > 0:
        return khi2, k_e
    else:
        return ""

def formfactorQualitySIMtoEXP(simFFdata, expFFdata):
    """Calculate form factor quality for a simulation as defined by Kučerka et al. 2010, doi:10.1007/s00232-010-9254-5 """

    # SAMULI: This creates a array containing experiments and simualtions with the overlapping x-axis values
    SimExpData = []   
    for SimValues in simFFdata:
        for ExpValues in expFFdata:
            if np.abs(SimValues[0]-ExpValues[0]) < 0.0005: # and ExpValues[0] < 0.41:
                SimExpData.append([ExpValues[0], ExpValues[1], ExpValues[2], SimValues[1]])

    k_e = calc_k_e(SimExpData)
    
    sum1 = 0
    N = len(SimExpData)
    for i in range(0,len(SimExpData)):
        F_e = SimExpData[i][1]
        deltaF_e = expFFdata[i][2] 
        F_s = SimExpData[i][3]
        
        sum1 = sum1 + (np.abs(F_s) - k_e*np.abs(F_e))**2 / (k_e*deltaF_e)**2
    
        khi2 = np.sqrt(sum1) / np.sqrt(N - 1)

    if N > 0:
        return khi2, k_e
    else:
        return ""

def loadSimulations():

    systems = initialize_databank()

    simulations = []
    for system in systems:
        try:
            experiments = system['EXPERIMENT']
        except KeyError:
            continue
        else:
            if any(experiments.values()): #if experiments is not empty

                simOPdata = {} #order parameter files for each type of lipid
                for lipMol in system['COMPOSITION']:
                    if lipMol not in lipids_dict:
                        continue
                    filename2 = os.path.join(NMLDB_SIMU_PATH, system['path'], lipMol + 'OrderParameters.json')
                    OPdata = {}
                    try:
                        with open(filename2) as json_file:
                            OPdata = json.load(json_file)
                    except FileNotFoundError:
                        # OP data for this lipid is missed
                        pass
                    simOPdata[lipMol] = OPdata
                
                simFFdata = {} # form factor data
                filename2 = os.path.join(NMLDB_SIMU_PATH, system['path'], "FormFactor.json")
                try:
                    with open(filename2) as json_file:
                        simFFdata = json.load(json_file)
                except FileNotFoundError:
                    # FormFactor data for this system is missed
                    pass
                simulations.append(Simulation(system, simOPdata, simFFdata, system['path']))
            else:
                print("The simulation does not have experimental data.")
                continue
                    
    return simulations

###################################################################################################