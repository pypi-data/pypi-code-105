import argparse
import requests
import hashlib
import random

https_url = "https://openapi.youdao.com/api"  # Api的https地址
app_key = "0feea8d9170c2a8a"  # 应用ID
secret_key = "UiXzbLvNDhxMbxiO1f2epTw7w0vSaWCx"  # 应用密钥
api_docs = "http://ai.youdao.com/docs/api.s#"  # 有道翻译api和说明文档
language = {  # 语言转换表
    "zh-CHS": "中文",
    "ja": "日文",
    "en": "英文",
    "ko": "韩语",
    "fr": "法语",
    "ru": "俄语",
    "pt": "葡萄牙",
    "es": "西班牙文",
    "EN": "英文",
    "zh": "中文"
}

# 生成md5签名
def to_sign(q, salt):
    """
    签名要进行UTF-8编码(否则中文无法翻译)
    :param q: 翻译文本
    :param salt: 随机数
    :return: sign: md5签名
    """
    sign = app_key + q + salt + secret_key
    m = hashlib.md5()
    m.update(sign.encode('utf-8'))
    sign = m.hexdigest()
    return sign


# 生成api_url
def get_api_url(sign, salt, q="Hello World", from_lan="auto", to_lan="auto"):
    api_url = "{}?q={}&sign={}&from={}&to={}&appKey={}&salt={}".format(https_url, q, sign, from_lan, to_lan, app_key, salt)
    return api_url


# 解析返回的json字段生成翻译
def resolve_res(trans_json):
    """
    把API返回的json字段解析成文字
    :param trans_json: json
    :return: string
    """
    if type(trans_json) != dict:
        print(mixStyle("返回字段格式不正确:"),type(trans_json))
        return ""
    if trans_json["errorCode"] != '0':  # 查询正确与否
        print(mixStyle("查询失败,errorCode:{},可查询官方文档:{}").format(trans_json["errorCode"], api_docs))
        return ""

    # result = backStyle_4("====== 翻译结果 ======") + "\n"  # 翻译结果
    result = ""  # 翻译结果

    if 'l' in trans_json:  # 转换关系
        lan2lan = trans_json['l'].split('2')
        fromLanguege = frontStyle_4(language[lan2lan[0]])
        trans = frontStyle_2('->')
        toLanguege = frontStyle_4(language[lan2lan[1]])
        result += "{} {} {}".format(fromLanguege, trans, toLanguege) + '\n'

    if 'query' in trans_json:  # 查询词句
        result += backStyle_4(trans_json['query']) + '\n'
    if 'translation' in trans_json:  # 翻译结果
        translation = backStyle_4("结果:" + "; ".join(trans_json['translation']))
        result += translation + '\n'
    if 'basic' in trans_json:  # 词义及发音
        basic = ""
        if 'uk-phonetic' in trans_json['basic']:  # 英式发音
            basic += frontStyle_4('英[{}]').format(frontStyle_2(trans_json['basic']['uk-phonetic']))
        if 'us-phonetic' in trans_json['basic']:  # 美式发音
            basic += frontStyle_4('美[{}]').format(frontStyle_2(trans_json['basic']['us-phonetic']))

        basic += "\n" + backStyle_1("词义:") + "\n" + frontStyle_4("\n".join(trans_json['basic']['explains']))
        result += basic + '\n'
    if 'web' in trans_json:  # 网络释义
        web = backStyle_1("网络释义:") + "\n"
        web_dic = ""
        for web_trans in trans_json['web']:
            web_dic += '{},{}'.format(web_trans['key'], "; ".join(web_trans['value'])) + '\n'
        web += frontStyle_4(web_dic)
        result += web + '\n'

    return result

"""打印前景色"""
def frontStyle_0(word):
    return f'\033[30m{word}\033[0m'
def frontStyle_1(word):
    return f'\033[31m{word}\033[0m'
def frontStyle_2(word):
    return f'\033[32m{word}\033[0m'
def frontStyle_3(word):
    return f'\033[33m{word}\033[0m'
def frontStyle_4(word):
    return f'\033[34m{word}\033[0m'
def frontStyle_5(word):
    return f'\033[35m{word}\033[0m'
def frontStyle_6(word):
    return f'\033[36m{word}\033[0m'
def frontStyle_7(word):
    return f'\033[37m{word}\033[0m'

"""打印背景色"""
def backStyle_0(word):
    return f'\033[40m{word}\033[0m'
def backStyle_1(word):
    return f'\033[41m{word}\033[0m'
def backStyle_2(word):
    return f'\033[42m{word}\033[0m'
def backStyle_3(word):
    return f'\033[43m{word}\033[0m'
def backStyle_4(word):
    return f'\033[44m{word}\033[0m'
def backStyle_5(word):
    return f'\033[45m{word}\033[0m'
def backStyle_6(word):
    return f'\033[46m{word}\033[0m'
def backStyle_7(word):
    return f'\033[47m{word}\033[0m'

"""打印显示方式"""
def displayStyle_0(word):
    return f'\033[0m{word}\033[0m'
def displayStyle_1(word):
    return f'\033[1m{word}\033[0m'
def displayStyle_2(word):
    return f'\033[4m{word}\033[0m'
def displayStyle_3(word):
    return f'\033[5m{word}\033[0m'
def displayStyle_4(word):
    return f'\033[7m{word}\033[0m'
def displayStyle_5(word):
    return f'\033[8m{word}\033[0m'

"""综合打印"""
def mixStyle(word):
    return f'\033[5;31;47m综合打印\033[0m'

def main():
    parser = argparse.ArgumentParser(description='Translation tool, translate CN <---> EN')
    parser.add_argument('words', type=str, nargs='+', help='Words need to be translated')
    args = parser.parse_args()
    keywords = args.words
    keyword = ''
    for key in keywords:
        keyword += str(key) + ' '
    if keyword == '':
        print(backStyle_1("翻译文本为空,请重新输入"))
        return 1
    salt = str(random.randint(12345, 56789))  # 生成随机数
    sign = to_sign(keyword, salt)  # 生成签名
    api_url = get_api_url(q=keyword, sign=sign, salt=salt, from_lan='auto', to_lan='auto',)
    try:
        translation_json = requests.get(api_url)
    except Exception as e:
        print(backStyle_1("没有网络连接:") + frontStyle_2(e))
        return 2
    if not translation_json.ok:
        print(backStyle_1("网络查询错误:") + frontStyle_2(translation_json))
        return 3
    result = resolve_res(trans_json=translation_json.json())
    print(result)
    return result
    

if __name__ == '__main__':
    main()