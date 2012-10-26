
# This file has been generated at Fri Oct 26 16:39:35 2012

from openalea.core import *


__name__ = 'alinea.adel.fitting'

__editable__ = True
__description__ = 'midrib fitting and simplification'
__license__ = 'CECILL'
__url__ = ''
__alias__ = ['adel.fitting']
__version__ = '0.0.1'
__authors__ = 'C. Pradal, C. Fournier'
__institutes__ = 'INRA, CIRAD, INRIA'
__icon__ = ''


__all__ = ['thermal_time_thermal_time', 'fit_fit_leaves', 'fit_simplify', 'fit_fit_leaf', 'fit_adel_input_data_fit_adel_input_data', 'dimension_fitting_dimension_fitting', 'fit_fit']



thermal_time_thermal_time = Factory(name='thermal_time',
                authors='C. Pradal, C. Fournier (wralea authors)',
                description='Calculates the thermal time increment.',
                category='data processing',
                nodemodule='thermal_time',
                nodeclass='thermal_time',
                inputs=[{'interface': None, 'name': 'requested_dates', 'value': None, 'desc': 'The dates for which the thermal time increment has to be calculated. These dates must belong to input_data, and be >= to emergence_date.'}, {'interface': IDict, 'name': 'emergence_date', 'value': {'hour': 0, 'month': 5, 'second': 0, 'year': 1998, 'day': 31, 'minute': 0}, 'desc': 'The emergence date. The interval [emergence date, emergence date + 1 year[ must be included in input_data. emergence_datetime must be <= than requested_dates'}, {'interface': None, 'name': 'input_data', 'value': None, 'desc': 'The input data. Expect a pandas.DataFrame object. The dataframe index must contain dates.'}, {'interface': IEnumStr(enum=['daily', 'hourly']), 'name': 'data_type', 'value': None, 'desc': "The type of the input data. Can be either 'daily' or 'hourly'."}, {'interface': IEnumStr(enum=['linear_TT', 'compensated_TT']), 'name': 'thermal_time_increment_method', 'value': None, 'desc': "The method used for thermal time increment calculation. Can be either 'linear_TT' or 'compensated_TT'."}, {'interface': IFloat, 'name': 'latitude', 'value': 55, 'desc': "The latitude where the data have been measured. Used to convert 'daily' data to 'hourly' data."}],
                outputs=[{'interface': None, 'name': 'temperature_increment', 'desc': 'The thermal time increment calculated (pandas.DataFrame).'}],
                widgetmodule=None,
                widgetclass=None,
               )




fit_fit_leaves = Factory(name='fit leaves',
                authors='C. Pradal, C. Fournier (wralea authors)',
                description='Replace measured midrib by fit and simplified curves',
                category='fitting',
                nodemodule='fit',
                nodeclass='fit_leaves',
                inputs=[{'interface': IDict, 'name': 'leaves', 'value': {}, 'desc': ''}, {'interface': IInt, 'name': 'nb_points', 'value': 7, 'desc': ''}],
                outputs=[{'interface': IDict, 'name': 'leaves', 'desc': 'New database'}],
                widgetmodule=None,
                widgetclass=None,
               )




fit_simplify = Factory(name='simplification',
                authors='C. Pradal, C. Fournier (wralea authors)',
                description='leaf simplification',
                category='fitting',
                nodemodule='fit',
                nodeclass='simplify',
                inputs=[{'interface': ISequence, 'name': 'leaf', 'value': [], 'desc': 'midrib (x, y, s, r)'}, {'interface': IInt, 'name': 'nb_points', 'value': 3, 'desc': 'target number of points after simplification'}],
                outputs=[{'interface': ISequence, 'name': 'leaf'}],
                widgetmodule=None,
                widgetclass=None,
               )




fit_fit_leaf = Factory(name='fit midrib',
                authors='C. Pradal, C. Fournier (wralea authors)',
                description='Fit a midrib with a spline curve of degree 5.',
                category='fitting',
                nodemodule='fit',
                nodeclass='fit_leaf',
                inputs=[{'interface': ISequence, 'name': 'leaf'}],
                outputs=[{'interface': ISequence, 'name': 'leaf'}, {'interface': IFloat, 'name': 'surface'}],
                widgetmodule=None,
                widgetclass=None,
               )




fit_adel_input_data_fit_adel_input_data = Factory(name='fit_adel_input_data',
                authors='C. Pradal, C. Fournier (wralea authors)',
                description='Fit ADEL input data.',
                category='data processing',
                nodemodule='fit_adel_input_data',
                nodeclass='fit_adel_input_data',
                inputs=None,
                outputs=({'interface': IInt, 'name': 'axis_table', 'desc': 'the axis table'}, {'interface': IInt, 'name': 'absolute_phen_table', 'desc': 'the absolute phen table'}, {'interface': IInt, 'name': 'relative_phen_table', 'desc': 'the relative phen table'}, {'interface': IInt, 'name': 'absolute_organ_dimensions_table', 'desc': 'the absolute dim table'}, {'interface': IInt, 'name': 'leaf_dynamic_parameters_table', 'desc': 'the leaf_dynamic_parameters table'}, {'interface': IInt, 'name': 'first_leaf_phen_table', 'desc': 'the first leaf phen table'}, {'interface': IInt, 'name': 'HS_GL_SSI_dynamic_table', 'desc': 'the HS_GL_SSI dynamic table'}, {'interface': IInt, 'name': 'relative_organ_dimensions_table', 'desc': 'the relative dim table'}, {'interface': IInt, 'name': 'tillering_dynamic_table', 'desc': 'the tillering dynamic table'}),
                widgetmodule=None,
                widgetclass=None,
               )




dimension_fitting_dimension_fitting = Factory(name='dimension_fitting',
                authors='C. Pradal, C. Fournier (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='dimension_fitting',
                nodeclass='dimension_fitting',
                inputs=[{'interface': None, 'name': 'ref_axis', 'value': None, 'desc': ''}, {'interface': None, 'name': 'dimT_tofit', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'dimT_fitted_df', 'desc': 'pandas.dataframe'}],
                widgetmodule=None,
                widgetclass=None,
               )




fit_fit = Factory(name='fit',
                authors='C. Pradal, C. Fournier (wralea authors)',
                description='fit a leaf (x, y, s, r)',
                category='fitting',
                nodemodule='fit',
                nodeclass='fit',
                inputs=[{'interface': ISequence, 'name': 'x', 'value': [], 'desc': 'midrib axis'}, {'interface': ISequence, 'name': 'y', 'value': [], 'desc': 'midrib ordinate'}, {'interface': ISequence, 'name': 's', 'value': [], 'desc': 'midrib curvilinear abscisse'}, {'interface': ISequence, 'name': 'r', 'value': [], 'desc': 'midrib radius'}, {'interface': IInt, 'name': 'nb_points', 'value': 3, 'desc': 'target number of points after simplification'}],
                outputs=[{'interface': ISequence, 'name': 'leaf'}],
                widgetmodule=None,
                widgetclass=None,
               )




