def get_review_data(soup):
    reviewlist = []
    reviews = soup.find_all('div',{'data-hook':'review'})
    try:
        for item in reviews:
            review_dict = {
            'product':soup.title.text.replace('Amazon.in:Customer reviews: ','').strip(),
            'title': item.find(class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold").get_text().strip(),
            'rating': float(item.find('i',{'data-hook':'review-star-rating'}).get_text().strip().replace('out of 5 stars','')),
            'review': item.find('span',{'data-hook':'review-body'}).get_text().strip()
            }
            reviewlist.append(review_dict)
    except:
        pass
    return reviewlist