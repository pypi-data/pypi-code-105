import requests


def mostrar_avatar(usuario):
    """
    O sistema buscará a foto que o avatar possui no Github
    :param usuario: str com nome do usuário
    :return: str com o link do avatar
    """
    url = f'https://api.github.com/users/{usuario}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(mostrar_avatar('clarasantosmf'))
