# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tolha', 'tolha.models']

package_data = \
{'': ['*']}

install_requires = \
['fastapi-utils>=0.2.1,<0.3.0',
 'loguru>=0.5.3,<0.6.0',
 'playwright>=0.142.3,<0.143.0',
 'pydantic[dotenv]>=1.8.2,<2.0.0',
 'python-decouple>=3.3,<4.0']

setup_kwargs = {
    'name': 'tolha',
    'version': '0.2.0',
    'description': 'Unofficial Library to access your my telco data',
    'long_description': '# Tolha - โทรหา\nเข้าถึงประวัติการโทรของตัวเองง่ายๆ จากค่ายมือถือของคุณ\n> ช่วยคุณนับความคิดถึงใครซักคนแบบ programmable\n\n\n## Highlight and Feature\n1. fully-type, with `pydantic`\n2. no docs, since api is so simple #hackerStyle\n3. Support Python 3.10.1+ #hackerStyle\n\n## Get Started\n```bash\n# support python 3.10+\npip install tolha\n```\n\n```python\nfrom tolha.myais import get_all_call_history\n\n# type down, myais credential\ninvoices, call_usages = get_all_call_history(phone_number_or_username=\'0995555555\', password=\'password1234\', national_id=\'1515566254125\')\n\nprint(invoices[0])\n# Invoice(invoice_number=\'W-IN-16-6412-xxxxxx\', is_required_sr=False, period_description=\'ค่าใช้บริการวันที่ 24/11/2021 - 23/12/2021 (Due Date 15/01/2022)\', period_from=\'24/11/2021\', period_to=\'23/12/2021\', payment_due_date=\'15/01/2022\', total_balance=\'405.75\', outstanding_balance=\'0.00\', is_payable=False, event_seq=\'211224000\', billing_system=\'NONBOS\', bill_cycle=\'ธันวาคม 2564\', remark=\'สามารถดูใบแจ้งค่าใช้บริการได้วันที่ 30 ธ.ค. 2564\')\n\n\nprint(call_usages[\'ธันวาคม 2564\'][0])\n# Call(datetime=datetime.datetime(2021, 11, 24, 9, 43), destination_phoneNumber=\'08xxxxxxxx\', destination_network=\'AIS\', origin=\'Udon Thani\', destination=\'AIS\', addons=\'\', duration=datetime.timedelta(seconds=60), calculated_cost=1.5, actual_cost=0.0, note=\'\')\n```\n\n## Dev\n\n### This is a movement.\n<a href="https://imgflip.com/i/5z7hhh"><img src="https://i.imgflip.com/5z7hhh.jpg" title="made at imgflip.com"/></a><div>\n\nFeel free to join and enlighten yourself, make your life a bit more programmable.\n\n### Roadmap\n1. add other metric\n2. make cli\n3. add other telco\n4. add async\n5. add other non telco - read facebook messenger dump/ google duo dump\n\n### Tools for CSS Selector\nuse <https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb>\n',
    'author': 'Nutchanon Ninyawee',
    'author_email': 'nutchanon@codustry.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CircleOnCircles/tolha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
