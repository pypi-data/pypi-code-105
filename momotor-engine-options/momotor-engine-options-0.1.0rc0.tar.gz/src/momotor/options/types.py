import typing

try:
    from typing import Literal  # 3.8+
except ImportError:
    from typing_extensions import Literal


StepTasksType = typing.Tuple[int, ...]
StepTaskNumberType = typing.Optional[typing.Tuple[int, ...]]

OptionTypeLiteral = Literal['str', 'bool', 'int', 'float']
LocationType = Literal['step', 'recipe', 'config', 'product']

SubDomainDefinitionType = typing.Dict[
    LocationType,
    typing.Union[str, typing.Sequence[typing.Optional[str]], None]
]
