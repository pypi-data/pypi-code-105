import rosbag
import importlib
import argparse

ros_primitive_types = [
    "bool",
    "byte",
    "char",
    "int8",
    "uint8",
    "int16",
    "uint16",
    "int32",
    "uint32",
    "int64",
    "uint64",
    "float32",
    "float64",
    "string",
]

preview_bag = rosbag.Bag("newBag.bag", "w")


def _map_ros_messages(original_message, new_msg):
    message_fields = _get_message_fields(original_message)
    for field_name, field_type in message_fields:
        try:
            field_value = getattr(original_message, field_name)
            _map_value(field_type=field_type, field_value=field_value, field_name=field_name, new_msg=new_msg)
        except AttributeError:
            pass
    return new_msg

def _map_value(field_type, field_value, field_name, new_msg):
    if field_type in ros_primitive_types:
        setattr(new_msg, field_name, field_value)
        return
    _map_ros_messages(field_value, getattr(new_msg, field_name))


def _get_message_fields(message):
    return zip(message.__slots__, message._slot_types)


def update_bag(original_bag: rosbag.Bag, data_class, topic_name: str):
    for topic, msg, t in original_bag.read_messages(topics=topic_name):
        new_msg = _map_ros_messages(msg, data_class())
        preview_bag.write(topic, new_msg, t)


def init(bag: rosbag.Bag):
    bag_topics = bag.get_type_and_topic_info().topics
    for topic, topic_tuple in bag_topics.items():
        x = topic_tuple.msg_type.split("/")
        import_string = x[0]
        for i in range(len(x)):
            if i == 0:
                continue
            if i == len(x) - 1:
                import_string = import_string + ".msg"
                data_class = importlib.import_module(import_string)
                update_bag(bag, getattr(data_class, x[i]), topic)
                break
            import_string = import_string + "." + x[i]
    preview_bag.close()

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bag-file", dest="bag", help="Path of the bag file")
    options = parser.parse_args()
    if not options.bag:
        parser.error("[-] Please specify a bag file path to be updated, use --help for more info")
    return options

def main(*args):
    options = get_arguments()
    init(rosbag.Bag(options.bag))

if __name__ == "__main__":
    main()
