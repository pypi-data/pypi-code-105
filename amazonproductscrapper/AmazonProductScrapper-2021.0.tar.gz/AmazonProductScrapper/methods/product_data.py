import pandas as pd
import time
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
        soup_var = get_soup(url)
        product_data_list = get_data(soup_var)
        for i in product_data_list:
            product_data_list_final.append(i)
        #print(len(product_data_list_final))
        time.sleep(0.1)
        printProgressBar(x,20,prefix = 'Progress:', suffix = 'Complete', length = 50)
        x = x + 1
        if not soup_var.find('li',{'class':'a-disabled a-last'}):
            pass
        else:
            break

    df = pd.DataFrame(product_data_list_final)
    return df
