import pandas as pd
import time
#from methods import soup
#from methods import review_attributes
#from methods import printProgressBar
from .soup import get_soup
from .review_attributes import get_review_data
from .progress import printProgressBar

def product_review_data(url,n):
    product_data_list = []
    product_data_list_final = []

    printProgressBar(0,20,prefix = 'Progress:', suffix = 'Complete', length = 50)
    x = 1
    while True:
        url_array = url.split("/")
        if x==1:
            url_1 = 'https://www.amazon.in/'+url_array[3]+'/product-reviews/'+url_array[5]+'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
        else:
            url_1 = 'https://www.amazon.in/'+url_array[3]+'/product-reviews/'+url_array[5]+'/ref=cm_cr_arp_d_paging_btm_next_'+str(x)+'?ie=UTF8&reviewerType=all_reviews&pageNumber='+str(x)
        try:
            soup_var = get_soup(url_1)
            product_data_list = get_review_data(soup_var)
            if product_data_list==[]:
                continue
        except:
            continue
        product_data_list_final.extend(product_data_list)
        #print(len(product_data_list_final))
        #time.sleep(0.1)
        printProgressBar(x,n,prefix = 'Progress:', suffix = 'Complete', length = 50)
        if x==n:
            break
        x = x + 1
        if not soup_var.find('li',{'class':'a-disabled a-last'}):
            pass
        else:
            break

    df = pd.DataFrame(product_data_list_final)
    return df
