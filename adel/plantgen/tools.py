# -*- python -*-
#
#       Adel.PlantGen
#
#       Copyright 2006-2012 INRIA - CIRAD - INRA
#
#       File author(s): Camille Chambon <camille.chambon@grignon.inra.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
'''
Generic routines used in the :mod:`alinea.adel.plantgen` package. These routines can also be 
used by other packages. 

Authors: Mariem Abichou, Camille Chambon, Bruno Andrieu
'''


import random
import math

import numpy as np
from scipy.optimize import leastsq

def decide_child_cohorts(decide_child_cohort_probabilities, parent_cohort_index=-1, first_child_delay=2):
    '''
    Decide (recursively) of the child cohorts actually produced by a parent cohort, 
    according to the *decide_child_cohort_probabilities* and the *parent_cohort_index*. The main 
    stem always exists.
    
    :Parameters:
    
        - `decide_child_cohort_probabilities` (:class:`dict`) - the probabilities of the 
          child cohorts.
        - `parent_cohort_index` (:class:`int`) - the index of the parent cohort.
        - `first_child_delay` (:class:`int`) - the delay between the parent cohort and 
          the first child cohort. This delay is expressed in number of cohorts.

    :Returns:
        The indices of the child cohorts.
    
    :Returns Type:
        list
    
    .. warning:: *decide_child_cohort_probabilities* must be a dict.
                 *parent_cohort_index* must be a int.
                 *first_child_delay* must be a int.
    
    '''
    assert isinstance(decide_child_cohort_probabilities, dict)
    assert isinstance(parent_cohort_index, int)
    assert isinstance(first_child_delay, int)
    child_cohort_numbers = []
    first_possible_cohort_number = parent_cohort_index + first_child_delay
    if first_possible_cohort_number == 1:
        # The main stem always exists, thus add it.
        child_cohort_numbers.append(first_possible_cohort_number)
        child_cohort_numbers.extend(decide_child_cohorts(decide_child_cohort_probabilities, 
                                                               first_possible_cohort_number))
    else:
        # Find the children of the secondary stem.
        for cohort_number_str, cohort_probability in decide_child_cohort_probabilities.iteritems():
            cohort_number = int(cohort_number_str)
            if cohort_number >= first_possible_cohort_number:
                if cohort_probability >= random.random():
                    child_cohort_numbers.append(cohort_number)
                    child_cohort_numbers.extend(decide_child_cohorts(decide_child_cohort_probabilities, 
                                                                           cohort_number))
    return child_cohort_numbers


def calculate_MS_final_leaves_number(MS_leaves_number_probabilities):
    '''
    Calculate the final number of leaves of a main stem. This is done by randomly 
    drawing a number in a probability distribution. Uses the probabilities 
    of the main stem leaves number. 
    
    :Parameters:
    
        - `MS_leaves_number_probabilities` (:class:`dict`) - the probabilities 
          of the main stem leaves number.
          
    :Returns:
        The final number of leaves of the main stem.
    
    :Returns Type:
        :class:`float`
        
    .. warning:: *MS_leaves_number_probabilities* must be a :class:`dict`.
    
    '''
    assert isinstance(MS_leaves_number_probabilities, dict)
    random_value = random.random()
    probabilities_sum = 0.0
    MS_final_leaves_number = None
    for leaves_number_str, leaves_probability in MS_leaves_number_probabilities.iteritems():
        probabilities_sum += leaves_probability
        if random_value <= probabilities_sum:
            MS_final_leaves_number = float(leaves_number_str)
            break
    return MS_final_leaves_number


def calculate_tiller_final_leaves_number(MS_final_leaves_number, cohort_number, secondary_stem_leaves_number_coefficients):
    '''
    Calculate the final number of leaves of a tiller.  
    Uses the final number of leaves of  the main stem, the index of the cohort to 
    which belongs the tiller, and specific coefficients.  
    
    :Parameters:
    
        - `MS_final_leaves_number` (:class:`float`) - the final number of leaves of the 
          main stem.
        - `cohort_number` (:class:`int`) - the index of cohort.
        - `secondary_stem_leaves_number_coefficients` (:class:`dict`) - The coefficients 
          a_1 and a_2 to calculate the final number of leaves on tillers from 
          the final number of leaves on main stem. Calculation is done as follow::
        
              tiller_final_leaves_number 
                  = a_1 * MS_final_leaves_number - a_2 * cohort_number

    :Returns:
        The final number of leaves of a tiller.
    
    :Returns Type:
        :class:`float`
        
    .. warning:: 
        
        * *MS_final_leaves_number* must be a :class:`float`.
        * *cohort_number* must be an :class:`int`.
        * *secondary_stem_leaves_number_coefficients* must be a :class:`dict`.
    
    '''
    assert isinstance(MS_final_leaves_number, float)
    assert isinstance(cohort_number, int)
    assert isinstance(secondary_stem_leaves_number_coefficients, dict)
    a_1 = secondary_stem_leaves_number_coefficients['a_1']
    a_2 = secondary_stem_leaves_number_coefficients['a_2']
    return a_1* MS_final_leaves_number - a_2 * cohort_number
    

def decide_time_of_death(max_axes_number, min_axes_number, TT_em_phytomer1, TT_bolting, TT_flowering):
    '''
    Decide the thermal times (relative to canopy emergence) when the axes stop 
    growing. Uses a linear function which describes the decay of the global population. 

    :Parameters:
    
        - `max_axes_number` (:class:`int`) - the maximum number of existing axes.
        - `min_axes_number` (:class:`int`) - the minimum number of existing axes. 
        - `TT_em_phytomer1` (:class:`list`) - Thermal times (relative to canopy emergence) 
          of tip emergence of the first true leaf (not coleoptile or prophyll)
        - `TT_bolting` (:class:`float`) - date in thermal time at which the bolting starts.
        - `TT_flowering` (:class:`float`) - The flowering date.

    :Returns: 
        the thermal times (relative to canopy emergence) when the axes stops growing.
    
    :Returns Type: 
        :class:`list`
        
    .. warning:: 
    
        * *max_axes_number* must an :class:`int`.
        * *min_axes_number* must an :class:`int`.
        * *TT_em_phytomer1* must a :class:`list`.
        * *TT_bolting* must an :class:`float`.
        * *TT_flowering* must an :class:`float`.
        * *min_axes_number*, *max_axes_number*, *TT_bolting* and *TT_flowering* 
          must be positive or null.
        * *TT_bolting* must be smaller (or equal) than *TT_flowering*.
        * *min_axes_number* must be smaller (or equal) than *max_axes_number*.

    '''
    assert isinstance(max_axes_number, int)
    assert isinstance(min_axes_number, int)
    assert isinstance(TT_em_phytomer1, list)
    assert isinstance(TT_bolting, float)
    assert isinstance(TT_flowering, float)
    
    assert max_axes_number >= 0 and min_axes_number >=0 and TT_bolting >= 0 and TT_flowering >= 0
    assert TT_bolting <= TT_flowering
    assert min_axes_number <= max_axes_number
    
    polynomial_coefficient_array = np.polyfit([TT_flowering, TT_bolting], [min_axes_number, max_axes_number], 1)
                
    remaining_axes_number = max_axes_number
    T_em_leaf1_tuples = zip(TT_em_phytomer1[:], range(len(TT_em_phytomer1)))
    T_em_leaf1_tuples.sort()
    T_stop_axis_tuples = []
    for tt in range(int(TT_bolting), int(TT_flowering) + 1):
        simulated_axes_number = int(np.polyval(polynomial_coefficient_array, tt))
        axes_to_delete_number = remaining_axes_number - simulated_axes_number
        while axes_to_delete_number > 0:
            max_emf_1, axis_row_number = T_em_leaf1_tuples.pop()
            T_stop_axis_tuples.append((axis_row_number, tt))
            axes_to_delete_number -= 1
            remaining_axes_number -= 1
        if remaining_axes_number == 0:
            break 
    T_stop_axis_tuples.sort()
    T_stop_axis_row_number_list = [T_stop_axis_tuple[0] for T_stop_axis_tuple in T_stop_axis_tuples]
    TT_stop_axis_list = [T_stop_axis_tuple[1] for T_stop_axis_tuple in T_stop_axis_tuples]
    for i in range(len(TT_em_phytomer1)):
        if i not in T_stop_axis_row_number_list:
            TT_stop_axis_list.insert(i, np.nan)
    return TT_stop_axis_list 


def fit_poly(x_meas_array, y_meas_array, fixed_coefs, a_starting_estimate):
    '''
    Calculate the best-fit parameter *a*, where *a* is the coefficient of highest 
    degree of a polynomial. The other polynomial coefficients are supposed to be 
    known and are given in *fixed_coefs*.
    We first define a function to compute the residuals. Then we use the least-squares 
    fit routine of scipy to find the best-fit parameter *a*, selecting *a_starting_estimate* 
    as starting position and using (*x_meas_array*, *y_meas_array*) as the measured 
    data to fit. Finally, we calculate the *RMSE* to check the validity of the fit. 

    .. seealso:: :func:`scipy.optimize.leastsq` 

    :Parameters:
    
        - `x_meas_array` (:class:`numpy.ndarray`) - the x-coordinates. These data are 
          measured.
        - `y_meas_array` (:class:`numpy.ndarray`) - the y-coordinates. These data are 
          measured.
        - `fixed_coefs` (:class:`list`) - the other coefficients of the polynomial to fit 
          (*x_meas_array*, *y_meas_array*) to. 
          These coefficients are not fitted. They are given from highest degree 
          to lowest degree ("descending powers").
        - `a_starting_estimate` (float) - the starting estimate for the minimization.
          
    :Returns: 
        the best-fit coefficient *a* and the *RMSE* of the fit.
    
    :Returns Type: 
        :class:`tuple` of :class:`float`
        
    .. warning:: 
    
        * *x_meas_array* must be a :class:`numpy.ndarray`.
        * *y_meas_array* must be a :class:`numpy.ndarray`.
        * *fixed_coefs* must be a :class:`list`.
        * *a_starting_estimate* must be a float.
                 
        
    '''
    assert isinstance(x_meas_array, np.ndarray)
    assert isinstance(y_meas_array, np.ndarray)
    assert isinstance(fixed_coefs, list)
    assert isinstance(a_starting_estimate, float)
    def residuals(p, y, x):
        a, = p
        err = y - peval(x, a)
        return err
    def peval(x, a):
        return np.poly1d([a] + fixed_coefs)(x)
    p, cov, infodict, mesg, ier = leastsq(residuals, [a_starting_estimate], args=(y_meas_array, x_meas_array), full_output=1)
    # RMSE_gl
    chisq = (infodict['fvec']**2).sum()
    dof = len(x_meas_array) - 1 # dof is degrees of freedom
    rmse = np.sqrt(chisq / dof)
    return p[0], rmse
