#  -*- coding: utf-8 -*-
from volcengine.example.cdn import ak, sk
from volcengine.cdn.service import CDNService

if __name__ == '__main__':
    svc = CDNService()
    svc.set_ak(ak)
    svc.set_sk(sk)

    resp = svc.describe_content_quota()
    print(resp)
