import requests

class Client:
    def __init__(self, token: str):
        self.token = token
        self.user_id = ''
        self.get_requests_header = {
            'Authorization': 'Bearer ' + self.token,
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8'
        }


    def authenticate(self):
        """
        GET https://api.medium.com/v1/me
        """
        h = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8'
        }
        r = requests.get('https://api.medium.com/v1/me', headers=h)

        response = r.json()

        if r.status_code == 200:
            self.user_id = response['data']['id']
            return response['data']
        else:
            raise RuntimeError(response['errors'][0]['message'])


    def get_pubblications(self):
        """
        GET https://api.medium.com/v1/users/{{userId}}/publications
        """
        r = requests.get('https://api.medium.com/v1/users/' + self.user_id + '/publications',
            headers=self.get_requests_header)
        
        response = r.json()

        if r.status_code == 200:
            return response['data']
        else:
            raise RuntimeError(response['errors'][0]['message'])


    def get_contributors(self, pubblication_id):
        """
        GET https://api.medium.com/v1/publications/{{publicationId}}/contributors
        """
        r = requests.get('https://api.medium.com/v1/publications/' + pubblication_id + '/contributors',
            headers=self.get_requests_header)

        response = r.json()

        if r.status_code == 200:
            return response['data']
        else:
            raise RuntimeError(response['errors'][0]['message'])


    def create_post(self, title, content_format, content,
        tags=[], canonical_url='', publish_status='public',
        license='all-rights-reserved', notify_followers='false'):
        """
        POST https://api.medium.com/v1/users/{{authorId}}/posts
        """
        header = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8'
        }
        data = {
            'title': title,
            'contentFormat': content_format,
            'content': content,
            'tags': tags,
            'canonicalUrl': canonical_url,
            'publishStatus': publish_status,
            'license': license,
            'notifyFollowers': notify_followers
        }
        
        r = requests.post('https://api.medium.com/v1/users/' + self.user_id + '/posts',
            headers=header, json=data)

        response = r.json()

        if r.status_code == 201:
            return response['data']
        else:
            raise RuntimeError(str(r.status_code) + ": " + response['errors'][0]['message'])