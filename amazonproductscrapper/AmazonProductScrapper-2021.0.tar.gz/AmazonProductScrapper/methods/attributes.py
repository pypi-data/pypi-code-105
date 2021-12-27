def get_data(soup):
    product_data_list = []
    product_data = soup.find_all('div',{'data-component-type':'s-search-result'})
    try:
        for item in product_data:
            product_data_dict = {
            'Product_Name':item.find(class_="a-size-medium a-color-base a-text-normal").get_text().strip(),
            'Product_Price': float(item.find(class_="a-price-whole").get_text().strip().replace(',','').replace('₹','')),
            'Actual_Product_Price': float(((item.find(class_="a-price a-text-price")).find(class_="a-offscreen")).get_text().strip().replace(' ','').replace('\n','').replace(',','').replace('₹','')),
            'No._of_ratings': int(item.find(class_="a-size-base").get_text().strip().replace(',','')),
            'Link': item.find(class_="a-link-normal a-text-normal")['href'].strip(),
            }
            product_data_list.append(product_data_dict)
    except:
        pass
    return product_data_list
