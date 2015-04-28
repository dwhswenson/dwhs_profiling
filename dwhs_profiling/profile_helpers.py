import profile
import pstats
import pandas as pd

class StatManager(object):
    
    property_functions = {
        None : (lambda x : None, None),
        'ncalls' : (lambda x : x[1], 0)    
    }
    
    def __init__(self, function_dictionary):
        self.function_dictionary = function_dictionary
        self.stats = None

    def run_stats(self, cmd):
        self.stats = pstats.Stats(profile.Profile().run(cmd)).strip_dirs()
        return self
    
    def get_property(self, prop, functions=None):
        if functions == 'all':
            keys = self.stats.stats.keys()
        elif functions is None:
            keys = self.function_dictionary.values()
        else:
            keys = [self.function_dictionary[f] for f in functions]
        vals = []
        for k in keys:
            try:
                line_data = self.stats.stats[k]
            except KeyError:
                line_data = None
            if line_data is not None:
                res = self.property_functions[prop][0](line_data)
            else:
                res = self.property_functions[prop][1]
            vals.append(res)
        return vals

def df_for_property(stat_dict, keyheaders=None, prop = None):
    """
    stat_dict : dictionary of { key : stat_manager }
    prop : element of StatManager.property_functions.keys()
    """
    rows = []
    for key in stat_dict.keys():
        if keyheaders is None:
            keyheaders=["Key " + str(i) for i in range(len(key))]
        statm = stat_dict[key]
        counts = statm.get_property(prop)
        row = tuple(list(key) + counts)
        rows.append(row)
        
    headers = keyheaders + statm.function_dictionary.keys()
    return pd.DataFrame(data=rows, columns=headers)

