import argparse
import os
from .tagmaps import TagMaps
import logging

logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)


def _create(arg, tag_maps: TagMaps):
    for tag in arg.new_tag:
        tag_maps.create(tag)


def _delete(arg, tag_maps: TagMaps):
    for tag in arg.goal_tag:
        tag_maps.delete(tag)


def _rename(arg, tag_maps: TagMaps):
    for tag in arg.old_name:
        if tag != arg.new_name[0]:
            tag_maps.rename(tag, arg.new_name[0])
        else:
            logging.warning("old name should differs from new name")
            # print("old name should differs from new name")


def _show(arg, tag_maps: TagMaps):
    if arg.some:
        for f in arg.path:
            abs_f = os.path.abspath(f)
            if not os.path.exists(f):
                logging.warning(f"path {f} not found, skipped")
                # print(f"path {f} not found, skipped")
            else:
                tag_set = tag_maps.show(abs_f)
                print(f"{abs_f}:\n - {' '.join(tag_set)}")
    # elif arg.use_pickle:
    #     pass
    else:
        if len(arg.path) == 1:
            f = os.path.abspath(arg.path[0])
            if not os.path.exists(f):
                logging.error(f"path {f} not found")
                # print(f"path {f} not found")
            else:
                tag_set = tag_maps.show(f)
                print(f"{' '.join(tag_set)}")
        else:
            logging.error("Must one path")
            # print("Must one path")


def _search(arg, tag_maps: TagMaps):
    abs_path = os.path.abspath(arg.goal_path)
    if not os.path.isdir(abs_path):
        logging.error(f"Dir {arg.goal_path} not found")
        # print(f"Dir {arg.goal_path} not found")
    else:
        goal_list = set()
        for f in os.listdir(abs_path):
            ref_f = os.path.join(abs_path, f)
            if tag_maps.search(arg.tags, ref_f):
                goal_list.add(ref_f)
        if arg.abs:
            print('\n'.join(goal_list))
        else:
            print(' '.join(
                map(os.path.relpath, goal_list)
                ))


def _attach(arg, tag_maps: TagMaps):
    if arg.all_in_dirs:
        for path in arg.paths:
            abs_path = os.path.abspath(path)
            if not os.path.isdir(path):
                logging.warning(f"Dir {path} not found, skipped")
                # print(f"Dir {path} not found, skipped")
            else:
                for f in os.listdir(abs_path):
                    abs_f = os.path.join(abs_path, f)
                    tag_maps.attach(arg.tag, abs_f)
    # elif arg.use_pickle:
    #     pass
    else:
        for path in arg.paths:
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                logging.warning(f"path {path} not found, skipped")
                # print(f"path {path} not found, skipped")
            else:
                tag_maps.attach(arg.tag, abs_path)


def _remove(arg, tag_maps: TagMaps):
    if arg.all_in_dirs:
        for path in arg.paths:
            abs_path = os.path.abspath(path)
            if not os.path.isdir(path):
                logging.warning(f"Dir {path} not found, skipped")
                # print(f"Dir {path} not found, skipped")
            else:
                for f in os.listdir(abs_path):
                    abs_f = os.path.join(abs_path, f)
                    tag_maps.remove(arg.tag, abs_f)
    # elif arg.use_pickle:
    #     pass
    else:
        for path in arg.paths:
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                logging.warning(f"path {path} not found, skipped")
                # print(f"path {path} not found, skipped")
            else:
                tag_maps.remove(arg.tag, abs_path)


# def _export(arg, tag_maps: TagMaps):
#     pass


def arg_to_map(arg: argparse.ArgumentParser, tag_maps: TagMaps):
    exec("_"+arg.key_+"(arg, tag_maps)")
    logging.info(f"{arg.key_.upper()} is OK!!!")
