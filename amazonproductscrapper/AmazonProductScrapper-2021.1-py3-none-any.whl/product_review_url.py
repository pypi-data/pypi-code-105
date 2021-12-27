from .methods import product_review_data
#from .methods import product_data

def load_Amazon_product_review_data(url,n):
    #keyword = input("Enter a keyword to search : ")
    df_1 = product_review_data(url,n)
    print("Loading Successful, Size of Dataframe : ",df_1.shape)
    return df_1

#df_review = load_Amazon_product_review_data("https://www.amazon.in/Boat-BassHeads-900-Wired-Headphone/dp/B074ZF7PVZ/ref=sr_1_3?crid=UPDZLG5ER2D3&keywords=headphones&qid=1640276178&sprefix=headphone%2Caps%2C647&sr=8-3",100)
#print(df_review)

