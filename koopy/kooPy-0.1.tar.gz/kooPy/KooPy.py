import requests
import json

class Koo:
    def getUserProfile(self, userName, format='dict', method='filter'):
        """ 
        Get user profile.

        Parameters:
        userId (str): userid of the user from koo.
        limited (bool): if True, only return limited profile.
        format (str): if 'dict', return a dict. if 'json', return a json string.
        method (str): if 'filter', return only important fields. if 'raw', return all fields.

        Returns:
        dict or json string: user profile.

        """

        url = f"https://www.kooapp.com/apiV1/users/handle/{userName}"
        r = requests.get(url)
        user = r.json()
        if method == 'filter':
            userData = {
                "userId": user["id"],
                "username": user["handle"],
                "displayName": user["name"],
                "profileImage": user["profileImage"],
                "title": user["title"],
                "description": user["description"],
                "createdAt": user["createdAt"],
                "followerCount": user["followerCount"],
                "followingCount": user["followingCount"],
                "socialProfile": user["socialProfile"],
                "totalKoos": user["kusCount"]
            }
        elif method == 'raw':
            userData = user
        if format == 'json':
            try:
                return json.dumps(userData,ensure_ascii=False, indent=4, sort_keys=True) 
            except UnicodeDecodeError:
                return json.dumps(userData,ensure_ascii=True, indent=4, sort_keys=True)
        elif format == 'dict':
            return userData
        
    def getUserKoos(self, userName, limit=10, format='dict',method='filter'):
        """
        Get user koos.

        Parameters:
        userName (str): userName of the user from koo.
        limit (int): limit of koos.
        format (str): if 'dict', return a dict. if 'json', return a json string.
        method (str): if 'filter', return only important fields. if 'raw', return all fields.

        Returns:
        dict or json string: user koos.

        """

        koos = self.getUserKoosRaw(userName, limit)

        koosData = []
        for koo in koos['feed']:
            kooItems = {}
            if method == 'filter':
                for kooItem in koo['items']:
                    kooItems['handle'] = kooItem['handle']
                    kooItems['name'] = kooItem['name']
                    kooItems['profileImage'] = kooItem['profileImageBaseUrl']
                    kooItems['createdAt'] = kooItem['createdAt']
                    kooItems['kuUrl'] = kooItem['kuUrl']
                    kooItems['title'] = kooItem['title']
                    kooItems['media'] = kooItem['mediaMap']
                    kooItems['comments'] = kooItem['nkus']
                    kooItems['likes'] = kooItem['nlikes']
                    kooItems['reKoos'] = kooItem['nreKoos']
            elif method == 'raw':
                kooItems = koo
            koosData.append(kooItems)
        if format == 'json':
            try:
                return json.dumps(koosData,ensure_ascii=False, indent=4, sort_keys=True) 
            except UnicodeDecodeError:
                return json.dumps(koosData,ensure_ascii=True, indent=4, sort_keys=True)
        elif format == 'dict':
            return koosData
    
    def getTrendingKoos(self, limit=3, format='dict', method='filter'):
        """
        Get trending koos. Minimum limit is 3 and Maximum limit is 100.

        Parameters:
        limit (int): limit of koos, default is 3 and maximum is 100.
        format (str): if 'dict', return a dict. if 'json', return a json string.
        method (str): if 'filter', return only important fields. if 'raw', return all fields.

        Returns:
        dict or json string: trending koos.

        """
        
        # Check limit
        # IMP: For some reason, for any limit koo will add +2 to the limit only if limit is below 250 or somewhere there. When limit increases beyond 250, it will add +1 to the limit.
        if limit <= 3:
            limit = 1
        elif limit > 100:
            limit = 98
        else:
            limit = limit - 2

        url = f"https://www.kooapp.com/apiV1/consumer_feed/explore?limit={limit}&offset=0&showPoll=false"
        r = requests.get(url)
        koos = r.json()

        koosData = []
        for koo in koos['feed']:
            kooItems = {}
            if koo['uiItemType'] == 'koo':
                if method == 'filter':
                    for kooItem in koo['items']:
                        kooItems['name'] = kooItem['name']
                        kooItems['profileImage'] = kooItem['profileImageBaseUrl']
                        kooItems['createdAt'] = kooItem['createdAt']
                        kooItems['kuUrl'] = kooItem['kuUrl']
                        kooItems['title'] = kooItem['title']
                        kooItems['media'] = kooItem['mediaMap']
                        kooItems['comments'] = kooItem['nkus']
                        kooItems['likes'] = kooItem['nlikes']
                        kooItems['reKoos'] = kooItem['nreKoos']
                elif method == 'raw':
                    kooItems = koo
                
                koosData.append(kooItems)
        if format == 'json':
            try:
                return json.dumps(koosData,ensure_ascii=False, indent=4, sort_keys=True) 
            except UnicodeDecodeError:
                return json.dumps(koosData,ensure_ascii=True, indent=4, sort_keys=True)
        elif format == 'dict':
            return koosData