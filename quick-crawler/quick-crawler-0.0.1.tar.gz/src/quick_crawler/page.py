import requests
import csv
import json
from bs4 import BeautifulSoup

def quick_html_page(url,headers=None,page_encoding='utf-8',save_file_path=None,save_encoding="utf-8"):
    if headers==None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }
    response = requests.get(url, headers=headers)
    html_str = response.content.decode(encoding=page_encoding)
    if save_file_path!=None:
        f_out = open(save_file_path, "w", encoding=save_encoding)
        f_out.write(str(html_str))
        f_out.close()
    return html_str

def quick_html_object(html_str):
    soup = BeautifulSoup(html_str, features="lxml")
    return soup

def quick_html_page_range(url,headers=None,page_encoding='utf-8',save_encoding="utf-8",save_file_path=None,min_page=1,max_page=100):
    list_html_str=[]
    for pi in range(min_page,max_page+1):
        current_url=url.replace("{pi}",str(pi))
        print(current_url)
        if save_file_path!=None:
            html_str=quick_html_page(current_url,headers,page_encoding, save_file_path=save_file_path.replace("{pi}",str(pi)), save_encoding=save_encoding)
        else:
            html_str = quick_html_page(current_url, headers, page_encoding)
        list_html_str.append(html_str)
    return list_html_str

def quick_remove_unicode(str,encoding='gbk',decoding='gbk'):
    string_encode = str.encode(encoding, "ignore")
    string_decode = string_encode.decode(decoding)
    return string_decode

def quick_save_csv(save_path,field_names,list_rows):
    with open(save_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for row in list_rows:
            dict_model = {}
            for f in field_names:
                dict_model[f]=row[f]
            writer.writerow(dict_model)

def quick_json_obj(url,headers=None,data=None):
    if headers==None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }
    if data!=None:
        x = requests.get(url, headers=headers, data=data)
    else:
        x = requests.get(url, headers=headers)
    # print(x.text)
    raw_str = quick_remove_unicode(x.text)
    pageObj = json.loads(raw_str)
    return pageObj

def quick_read_csv(csv_path,fields):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        list_result=[]
        for row in reader:
            l=[]
            for f in fields:
                l.append(row[f])
            list_result.append(l)
        return list_result

def quick_download_file(url,save_file_path,headers=None,):
    if headers!=None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }
    r = requests.get(url, headers=headers, stream=True)
    if r.status_code == 200:
        open(save_file_path, 'wb').write(r.content)  # 将内容写入图片

def quick_post_html_page(url,headers=None,data=None):
    if headers!=None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }
    if data!=None:
        r = requests.post(url, json=data,
                      headers=headers)
    else:
        r = requests.post(url)
    return r.text

def quick_post_json_obj(url,headers=None,data=None):
    if headers==None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }
    if data!=None:
        x = requests.post(url, headers=headers, data=data)
    else:
        x = requests.post(url, headers=headers)
    # print(x.text)
    raw_str = quick_remove_unicode(x.text)
    pageObj = json.loads(raw_str)
    return pageObj