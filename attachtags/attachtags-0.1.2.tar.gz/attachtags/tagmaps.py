"""这个模块定义了Tagmaps类型
"""
from functools import wraps
import logging

logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)


def exist_or_not(function):    # 判断是否有这个tag
    @wraps(function)
    def wrapper(self, *args, **kwargs) -> bool:
        if args[0] in list(self.get_map().keys()):
            function(self, *args, **kwargs)
            return True
        else:
            logging.error(f"Fail {function.__name__}:: not the \
tag: {args[0]}", end="")
#             print(f"""Fail {function.__name__}
#  - not the tag: {args[0]}""", end="")
            if len(args) > 1:
                print(f""" for {args[1]}""")
            else:
                print('\n')
            return False
    return wrapper


class TagMaps:
    def __init__(self):
        self.__map = dict()
        self.tagnames = set()

    def get_map(self) -> dict:
        return self.__map

    def create(self, new_name):
        if new_name not in list(self.__map.keys()):
            self.__map[new_name] = set()
            return True
        else:
            logging.error(f"Fail create:: tag {new_name} has already\
 existed")
            # print(f"tag {new_name} has already existed")
            return False

    @exist_or_not
    def delete(self, goal):
        del self.__map[goal]

    @exist_or_not
    def rename(self, old_name, new_name):
        if not self.create(new_name):
            logging.info(f"{old_name} and {new_name} were merged")
            # print("two tags were merged")
        self.__map[new_name].update(self.__map[old_name])
        self.delete(old_name)

    def show(self, goal: str) -> set:
        tag_set = set()
        for tag in self.__map.keys():
            if goal in self.__map[tag]:
                tag_set.add(tag)
        return tag_set

    def search(self, tags, path):
        for tag in tags:
            if path in self.__map[tag]:
                return True
            return False

    @exist_or_not
    def attach(self, tag, path):
        if path not in self.__map[tag]:
            self.__map[tag].add(path)
        else:
            logging.warning(f"{path} was existed")
            # print(f"{path} was existed, skipping")

    @exist_or_not
    def remove(self, tag, path):
        if path in self.__map[tag]:
            self.__map[tag].remove(path)
        else:
            logging.warning(f"{path} is not with {tag}")
            # print(f"{path} is not with {tag}")


if __name__ == '__main__':
    tag = TagMaps()
    if tag.create('foo'):
        print(tag.rename('foo', 'bar'))
