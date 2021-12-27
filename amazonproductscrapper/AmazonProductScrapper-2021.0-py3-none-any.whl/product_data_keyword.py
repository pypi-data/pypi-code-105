from .methods import product_data

def load_Amazon_product_data(keyword):
    #keyword = input("Enter a keyword to search : ")
    df_1 = product_data(keyword)
    print("Loading Successful, Size of Dataframe : ",df_1.shape)
    return df_1

#df_product = load_Amazon_product_data("laptops")
