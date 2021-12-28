import pandas as pd
import time
#from methods import soup
#from methods import attributes
#from methods import progress
from .soup import get_soup
from .attributes import get_data
from .progress import printProgressBar

def product_data(keyword):
    product_data_list = []
    product_data_list_final = []

    printProgressBar(0,20,prefix = 'Progress:', suffix = 'Complete', length = 50)
    x = 1
    while True:
        url = 'https://www.amazon.in/s?k='+keyword+'&page='+str(x)+'&ref=sr_pg_'+str(x)
        try:
            soup_var = get_soup(url)
            product_data_list = get_data(soup_var)
            if product_data_list==[]:
                continue
        except:
            continue
        product_data_list_final.extend(product_data_list)
        #print(len(product_data_list_final))
        time.sleep(1.0)
        printProgressBar(x,20,prefix = 'Progress:', suffix = 'Complete', length = 50)
        x = x + 1
        if x==21:
            break
        if not soup_var.find('li',{'class':'a-disabled a-last'}):
            pass
        else:
            break
    df = pd.DataFrame(product_data_list_final)
    return df
