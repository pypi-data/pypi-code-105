from numpy import arange, e, sin, cos
import matplotlib.pyplot as plt
from pandas import DataFrame

def Eiler_Koshi(functions, start, limits):
    
    '''
    Входные данные:
    Функции - [func1, func2 ...],
    Нач усл - [y1, y2 ...],
    Границы - [left, right, step]   
    '''
    
    
    
    dict_of_func = {}
    for func in functions:
        dict_of_func[func[:(func.find("'"))]] = func[(func.find('=')+1):].replace(' ','')

    x_plot = arange(limits[0],limits[1],limits[2])
    

    k = 0
    formats_i = ''
    formats_i1 = ''
    for key, val in dict_of_func.items():
        exec(f'{key}_i =  {start[k]}')
        exec(f'{key}_i1 = {start[k]}')
        exec(f'{key}_plot = []')
        formats_i += f'.replace("{key}", str({key}_i)).replace("x",str(x))'
        formats_i1 += f'.replace("{key}", str({key}_i1)).replace("x",str(x+limits[2]))'
        k += 1

        
    for x in x_plot:
        
        for key, val in dict_of_func.items():
            exec(f'{key}_i = {key}_i1')
            
        for key, val in dict_of_func.items():
            exec(f'{key}_i1 = float(eval(str({key}_i)+"+"+str({limits[2]})+"*"+str(eval("{val}"{formats_i}))))')
                
        for key, val in dict_of_func.items():
            exec(f'{key}_i1 = float(eval(str({key}_i))){"+"}{limits[2]}/2{"*("}float(eval("{val}"{formats_i})){"+"}float(eval("{val}"{formats_i1})){")"}')
            
        for key, val in dict_of_func.items():
            exec(f'{key}_plot.append({key}_i1)')
    
    dict_for_df = {'x': x_plot}
    for key, val in dict_of_func.items():  
        exec(f'dict_for_df["{key}"] = {key}_plot')
        
    return DataFrame(dict_for_df)
def Runge_Kutta(functions, start, limits):
    
    '''
    Входные данные:
    Функции - [func1, func2 ...],
    Нач усл - [y1, y2 ...],
    Границы - [left, right, step]   
    '''
    
    
    
    dict_of_func = {}
    for func in functions:
        dict_of_func[func[:(func.find("'"))]] = func[(func.find('=')+1):].replace(' ','')

    x_plot = arange(limits[0],limits[1] + limits[2],limits[2])
    

    k = 0
    formats_i_1 = ''
    formats_i_2 = ''
    formats_i_3 = ''
    formats_i_4 = ''
    
    for key, val in dict_of_func.items():
        exec(f'{key}_i =  {start[k]}')
        exec(f'{key}_plot = []')
        formats_i_1 += f'.replace("{key}", str({key}_i)).replace("x",str(x))'
        formats_i_2 += f'.replace("{key}", str({key}_i + {key}_1/2)).replace("x",str(x + limits[2]/2))'
        formats_i_3 += f'.replace("{key}", str({key}_i + {key}_2/2)).replace("x",str(x + limits[2]/2))'
        formats_i_4 += f'.replace("{key}", str({key}_i + {key}_3/2)).replace("x",str(x + limits[2]/2))'
        k += 1

        
    for x in x_plot:
         
        for key, val in dict_of_func.items():
            exec(f'{key}_plot.append({key}_i)')
            
        for key, val in dict_of_func.items():
            exec(f'{key}_1 = {limits[2]} * float(eval("{val}"{formats_i_1}))')
            
        for key, val in dict_of_func.items():
            exec(f'{key}_2 = {limits[2]} * float(eval("{val}"{formats_i_2}))')
                
        for key, val in dict_of_func.items():
            exec(f'{key}_3 = {limits[2]} * float(eval("{val}"{formats_i_3}))')
            
        for key, val in dict_of_func.items():
            exec(f'{key}_4 = {limits[2]} * float(eval("{val}"{formats_i_4}))')
    
        for key, val in dict_of_func.items():
            exec(f'{key}_i = {key}_i + (1/6)*({key}_1+2*{key}_2+2*{key}_3+{key}_4)')
            
        
                 
    dict_for_df = {'x': x_plot}
    for key, val in dict_of_func.items():  
        exec(f'dict_for_df["{key}"] = {key}_plot')
        
    return DataFrame(dict_for_df)
    
def analysis(df):
    """Просто отправьте в эту функци ответ от (Runge Kutta например...)"""
    
    
    cols = df.columns.tolist()
    
    for element in cols[1:]:
        plt.scatter(df[cols[0]], df[element], label = f'{element}({cols[0]})')
        plt.legend()
        plt.show()