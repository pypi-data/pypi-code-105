import datetime, decimal, os, re, time, traceback, redis, json, pymongo, logging, xlrd, base64

from captcha.image import ImageCaptcha, random_color
from random import randint
from io import BytesIO
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from binascii import b2a_hex, a2b_hex
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import InstrumentedAttribute, DeclarativeMeta, sessionmaker
from xlrd import xldate_as_tuple
from xlsxwriter import Workbook


class OrmClient:
    db_support_lit = ['mysql', 'sqlserver', 'postgresql']

    def __init__(self, db_type='mysql', host='127.0.0.1', port=3306, username='root', password='W4096reader',
                 database='roi'):
        assert db_type in self.db_support_lit, '数据库类型不支持，请在下面三个中选择：\n{}'.format('、'.join(self.db_support_lit))

        self.db_type = db_type
        self.conn_info = {
            'host': host,
            'port': port,
            'username': username,
            'password': password,
            'database': database,
        }
        self.make_session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def make_session(self):
        engine_dict = {
            'mysql': 'mysql+pymysql',
            'sqlserver': 'mssql+pymssql',
            'postgresql': 'postgresql+psycopg2'
        }
        conn_string = '://{username}:{password}@{host}:{port}/{database}'
        engine_string = (engine_dict[self.db_type] + conn_string).format(**self.conn_info)
        self.engine = create_engine(engine_string)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def make_filter(self, model, fields_in: list = None, fields_no: list = None):
        """
        sqlalchemy query条件生成器
        :param model: sqlalchemy 模型
        :param fields_in: 显示字段列表
        :param fields_no: 隐藏字段列表
        :return: query list
        """
        query_filter = []
        if fields_in:
            for field in fields_in:
                attr = getattr(model, field) if field in dir(model) else None
                if attr:
                    query_filter.append(attr)

        elif fields_no:
            for attr in dir(model):
                if attr in fields_no or attr.startswith('_'):
                    continue
                condition = getattr(model, attr)
                if isinstance(condition, InstrumentedAttribute):
                    query_filter.append(condition)

        return query_filter if query_filter else [model]


class MongoClient:
    def __init__(self, **kwargs):
        self.conn_mongo = pymongo.MongoClient('mongodb://{user}:{password}@{host}:{port}'.format(**kwargs))
        """
        示例
        self.site_db = self.conn_mongo['robot']['sites']
        self.site_db.create_index('url', unique=True)
        self.job_db = self.conn_mongo['robot']['jobs']
        self.job_db.create_index('j_id', unique=True)
        self.customer_db = self.conn_mongo['robot']['customer']
        self.project_db = self.conn_mongo['robot']['project']
        self.history_db = self.conn_mongo['robot']['history']
        self.user_db = self.conn_mongo['robot']['users']
        
        增
        self.site_db.insert(**kwargs)
        查
        self.site_db.find({}, {'_id': 0, 'site_name': 1, 'url': 1}).sort([('create_time', -1)].skip(1).limit(1)
        改
        self.customer_db.update({'c_id': old_cid},
                                {'$set': {'c_id': cid, 'name': name, 'creater': creater, 'remark': remark}}, multi=True)
        """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_mongo.close()
        return


class RedisClient:
    def __init__(self, host='123.57.66.110', port=6379, db=0, password='W4096redis'):
        pool = redis.ConnectionPool(host=host, port=port, password=password, decode_responses=True)
        self.conn = redis.Redis(connection_pool=pool, db=db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def push(self, key, value):
        self.conn.lpush(key, value)

    def set(self, key, value, path=None, ex=None):
        """
        :param key: key
        :param value: value
        :param path: 文件夹名称
        :param ex: 过期时间
        :return: None
        """
        if path:
            self.conn.set(f'{path}:{key}', value)
        else:
            self.conn.set(key, value, ex=ex)

    def get(self, key, path=None):
        return self.conn.get(f'{path}:{key}') if path else self.conn.get(key)

    def delete(self, key, path=None):
        """
        :return: 1：删除成功； None：键不存在
        """
        return self.conn.delete(f'{path}:{key}') if path else self.conn.delete(key)


class LocalFaker:
    """
    生成随机数据
    """

    def __init__(self):
        self.f = Faker(locale='zh_CN')

    def name(self):
        return self.f.name()

    def address(self):
        return self.f.address()

    def email(self):
        return self.f.email()

    def bank_no(self):
        self.f.bban()  # 基本银行账号

    def company(self):
        self.f.company()  # 公司名称

    def job(self):
        self.f.job()  # 职位

    def md5(self):
        self.f.md5(raw_output=False)  # Md5

    def bool(self):
        self.f.boolean(chance_of_getting_true=50)  # 布尔值

    def pwd(self):
        self.f.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)  # 密码

    def phone(self):
        self.f.phone_number()  # 手机号

    def sfz(self):
        self.f.ssn(min_age=18, max_age=90)  # 身份证


class AlchemyEncoder(json.JSONEncoder):
    """
    sqlalchemy 模型转字典，特殊类型处理类，使用方式
    json.dumps(dict, cls=AlchemyEncoder)
    """

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:  # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.strftime("%Y-%m-%d %H:%M:%S")
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (datetime.datetime.min + data).time().isoformat()
                    elif isinstance(data, datetime.time):
                        fields[field] = data.strftime("%H:%M:%S")
                    else:
                        fields[field] = None
            return fields
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        elif isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S")
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class PKCS7Encoder(object):
    @staticmethod
    def decode(bytestring, k=16):
        val = bytestring[-1]
        if val > k:
            raise ValueError('Input is not padded or padding is corrupt')
        l = len(bytestring) - val
        return bytestring[:l]

    @staticmethod
    def encode(bytestring, k=16):
        l = len(bytestring.encode('utf-8'))
        val = k - (l % k)
        return bytes(bytestring, 'utf-8') + bytes([val] * val)


class CryptoHelper:
    def __init__(self, key='12345678900000001234567890000000', iv='1234567890000000'):
        self.KEY = bytes(key, 'utf8')
        self.IV = bytes(iv, 'utf8')

    @staticmethod
    def encrypt_md5(text):
        """
        md5 加密
        """
        h = MD5.new()
        h.update(bytes(text, 'utf8'))
        return h.hexdigest()

    def encrypt_aes(self, text):
        """
        aes 加密
        """
        if type(text) is not str:
            text = json.dumps(text, cls=AlchemyEncoder)

        cryptor = AES.new(self.KEY, AES.MODE_CBC, self.IV)
        pad_text = PKCS7Encoder.encode(text)
        ciphertext = cryptor.encrypt(pad_text)
        return str(b2a_hex(ciphertext), encoding='utf-8').upper()

    def decrypt_aes(self, text):
        """
        aes 解密
        """
        cryptor = AES.new(self.KEY, AES.MODE_CBC, self.IV)
        pad_text = cryptor.decrypt(a2b_hex(text))
        try:
            return PKCS7Encoder.decode(pad_text).decode('utf-8')
        except:
            return None


class Tools:
    @staticmethod
    def make_res(results: list, fields: list = None):
        """
        :param results: ORM查询结果集
        :param fields: 显示字段
        :return: 列表
        """
        # items = [dict(result) for result in results]

        items = []
        if not fields:
            items = [dict(result) for result in results]
        else:
            for result in results:
                item = {}
                for field in fields:
                    if field in result._fields:
                        item[field] = getattr(result, field)
                    else:
                        item[field] = f'不存在该字段{field}'
                items.append(item)
        return json.dumps(items, cls=AlchemyEncoder)

    @staticmethod
    def get_birth_from(card_no):
        """
        :param card_no: str 身份证号
        :return: 出生年月
        """
        if card_no is None or card_no == '':
            return None
        card_length = len(card_no)
        if card_length == 18:
            try:
                birth = datetime.datetime.strptime(card_no[6:14], '%Y%m%d')
            except Exception as e:
                print(e)
                return None
            return birth
        elif card_length == 15:
            try:
                birth = datetime.datetime.strptime('19' + card_no[6:12], '%Y%m%d')
            except Exception as e:
                print(e)
                return None
            return birth
        else:
            return None

    @staticmethod
    def make_captcha(length=4, width=160, height=60, fonts=None, font_sizes=None, char_range='0123456789',
                     dots=False, curve=False):
        """
        生成验证码吗，返回验证码数字、图片二进制流
        """
        chars = ''.join([(char_range[randint(0, len(char_range) - 1)]) for i in range(length)])

        background = random_color(238, 255)
        color = random_color(10, 200, randint(220, 255))

        ic = ImageCaptcha(width=width, height=height, fonts=fonts, font_sizes=font_sizes)
        image = ic.create_captcha_image(chars, color, background)

        # 生成验证码干扰点
        if dots:
            ic.create_noise_dots(image, color, width=3, number=30)

        # 生成验证码干扰曲线。
        if curve:
            ic.create_noise_curve(image, color)

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        # image.show()
        image.close()
        img_str = base64.b64encode(buffered.getvalue())
        return chars, img_str

    @staticmethod
    def transform_unix(num):
        """
        unix时间转换 -- 微信使用
        :param num:
        :return: 日期
        """
        format = '%Y-%m-%d %H:%M:%S'
        value = time.localtime(int(num))
        dt = time.strftime(format, value)
        return dt

    @staticmethod
    def transfrom_datetime(obj):
        """
        将时间对象转换为字符串
        :param obj: 时间对象
        :return:
        """
        obj_support_list = [datetime.datetime, datetime.date, datetime.timedelta, datetime.time]
        assert type(obj) in obj_support_list, '类型不支持'

        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        elif isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S")

    @staticmethod
    def str_to_timestamp(timestr, strformat='%Y-%m-%d %H:%M:%S'):
        """
        字符串转时间戳
        :param timestr: 时间字符串
        :param strformat: 转换格式 (%Y-%m-%d %H:%M:%S)
        :return: 时间戳 (前10位)
        """
        ret = int(time.mktime(time.strptime(timestr, strformat)))

        return ret

    @staticmethod
    def send_mail(mail_title, mail_content, recievers=['527439841@qq.com'], file_path=None, style='plain'):
        # 发送邮件
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # 第三方 SMTP 服务
        mail_host = "smtp.qq.com"  # SMTP服务器
        mail_user = "527439841@qq.com"  # 用户名
        mail_pass = "jvubnbbddlrgcbbf"  # 授权密码，非登录密码

        content = mail_content
        title = mail_title  # 邮件主题

        message = MIMEMultipart()
        # 正文
        message.attach(MIMEText(content, style, 'utf-8'))
        message['From'] = "{}".format(mail_user)
        message['To'] = ",".join(recievers)
        message['Subject'] = title

        # 构造附件1
        if file_path:
            file_name = file_path.split('\\')[-1]  # 文件名中不能含中文
            att1 = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="{}"'.format(file_name)
            message.attach(att1)

        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(mail_user, mail_pass)  # 登录验证
            smtpObj.sendmail(mail_user, recievers, message.as_string())  # 发送
        except smtplib.SMTPException as e:
            traceback.print_exc()
            print(e)

    @staticmethod
    def make_logger(path=None):
        if not path:
            path = os.getcwd()
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        os.makedirs(path, exist_ok=True)
        log_name = path + 'log.txt'
        logfile = log_name
        fh = logging.FileHandler(logfile, mode='a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    @staticmethod
    def get_excel_data(path):
        """获取excel数据，返回列表，每一项为行内所有值"""
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        rows = sheet.nrows
        item_list = []
        for row in range(rows):
            data = sheet.row_values(row)
            row_content = []
            for j, each in enumerate(data):
                ctype = sheet.cell(row, j).ctype
                cell = sheet.cell_value(row, j)
                if ctype == 3:
                    date_tuple = xldate_as_tuple(cell, 0)
                    cell = str(datetime.datetime(*date_tuple))
                row_content.append(cell)
            item_list.append(row_content)
        return item_list

    @staticmethod
    def save_xls(body, path, head=[], replace=False):
        """
        保存文件到excel
        :param head: 头部 [h1, h2, h3]
        :param body: 内容 [[l1], [l2], ..., [ln]]
        :param path: 保存文件路径
        :return:
        """
        assert type(head) is list, 'head 必须为列表'
        assert type(body) is list, 'body 必须为列表'

        if os.path.exists(path):
            if replace:
                os.remove(path)
            else:
                assert not os.path.exists(path), '文件已存在'

        workbook = Workbook(path)
        sheet = workbook.add_worksheet('sheet1')
        yellow_style = workbook.add_format(
            {'bold': True, 'font_name': 'Arial', 'font_size': 10, 'bg_color': 'yellow', 'color': 'black',
             'valign': 'center', 'align': 'left'})
        black_style = workbook.add_format(
            {'bold': True, 'font_name': 'Arial', 'font_size': 10, 'bg_color': 'black', 'color': 'white',
             'valign': 'center', 'align': 'left'})
        align_style = workbook.add_format({'align': 'left', 'valign': 'left'})
        head_column = 0
        if head:
            body_column = 1
            for index in range(len(head)):
                sheet.write(head_column, index, head[index], black_style)
        else:
            body_column = 0

        for index in range(len(body)):
            for i in range(len(body[index])):
                # # 周列
                # if i == 1:
                #     sheet.write_formula(body_column, i, '="第"&WEEKNUM(A{},2)&"周"'.format(body_column + 1))
                #     continue

                # # 金额列
                # if i == 5:
                #     sheet.write_formula(body_column, i, '=D{}*E{}'.format(body_column + 1, body_column + 1))
                #     continue

                info = body[index][i]
                if isinstance(info, int) or isinstance(info, float) or (info.isdigit() and len(info) < 12):
                    sheet.write_number(body_column, i, int(info))
                else:
                    sheet.write(body_column, i, body[index][i])
            body_column += 1

        sheet.set_column('A:W', cell_format=align_style)
        sheet.set_column(0, 0, width=10)
        sheet.set_column(9, 9, width=16)
        sheet.freeze_panes(1, 0)
        workbook.close()

    @staticmethod
    def excel_color(xls_path, head_list=['标题', '概要', '正文']):
        """
        excel 关键字标红
        在原路径下生成新文件文件名为原文件名 + new
        :param xls_path: 文件路径
        注：关键词列必须位于最后一列
        """
        import xlrd
        import jieba
        from xlsxwriter import Workbook

        old_book = xlrd.open_workbook(xls_path)
        sheets = old_book.sheets()
        new_file_path = xls_path.replace('.', 'new.')
        new_workbook = Workbook(new_file_path)

        red_style = new_workbook.add_format({'color': 'red', 'font_name': 'Arial', 'font_size': 10})
        bold_style = new_workbook.add_format({'bold': True, 'font_name': 'Arial', 'font_size': 10})
        font_style = new_workbook.add_format({'font_name': 'Arial', 'font_size': 10})

        for index, sheet in enumerate(sheets):
            print(index, sheet.name)
            old_sheet = sheet
            rows_num = old_sheet.ncols
            new_sheet = new_workbook.add_worksheet(sheet.name)

            for col in range(rows_num):
                values = old_sheet.col_values(col, start_rowx=0)
                head = values[0]
                if head in head_list:
                    for row, each in enumerate(values):
                        if each:
                            keywords = old_sheet.col_values(colx=rows_num - 1, start_rowx=row)[0].split(',')
                            lst = []
                            for i in keywords:
                                lst.extend(i.split())
                            keywords = ''.join(keywords)
                            format_list = []
                            for i in lst:
                                each = re.sub(i, '^^^^{}^^^^'.format(i), each, flags=re.IGNORECASE)
                            words = each.split('^^^^')
                            for word in words:
                                if not word:
                                    continue
                                try:
                                    result = re.findall(r'{}'.format(word), keywords, re.IGNORECASE)
                                except:
                                    format_list.append(word)
                                    continue
                                if result:
                                    format_list.extend((red_style, word))
                                else:
                                    format_list.append(word)

                            if format_list:
                                new_sheet.write_rich_string(row, col, *format_list)
                            else:
                                new_sheet.write(row, col, ' ')
                else:
                    new_sheet.write_column(0, col, values, cell_format=font_style)
            new_sheet.set_row(0, cell_format=bold_style)
            new_sheet.freeze_panes(1, 0)

        new_workbook.close()


if __name__ == '__main__':
    pass

    # with SqlserverClient() as s:
    #     s.excute('select * from dbo.Dict t')
    #     results = s.fetchall()
    # for item in results:
    #     print(item)

    # with PgClientOrm() as s:
    #     pass

