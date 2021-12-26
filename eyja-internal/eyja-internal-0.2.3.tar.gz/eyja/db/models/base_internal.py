from typing import List


class BaseInternal:
    namespace: str = None
    indexes: List[str] = [
        'created_at',
        'updated_at',
    ]
