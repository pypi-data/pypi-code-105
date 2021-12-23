from plover_next_stroke.sorting import SortingType


CONFIG_ITEMS = {
    "row_height": 30,
    "page_len": 10,
    "sorting_type": SortingType.FREQUENCY
}


class NextStrokeConfig:
    def __init__(self, values: dict = None):
        if values is None:
            values = dict()

        for key, default in CONFIG_ITEMS.items():
            if key in values:
                setattr(self, key, values[key])
            else:
                setattr(self, key, default)

    def copy(self) -> "NextStrokeConfig":
        value_dict = {k: getattr(self, k) for k in CONFIG_ITEMS.keys()}
        return NextStrokeConfig(value_dict)
