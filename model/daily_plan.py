from dataclasses import dataclass
from commonkit.utilities.uuid_utilities import UUIDUtilities
from typing import Any, TypeVar, get_type_hints

@dataclass
class DailyPlan:
    id: str = UUIDUtilities.generate_unique_string()
    task:str = None
    goal:str = None
    day_session:str = None
    day:str = None
    user_name:str = None
    chat_id:int = None
    is_done:bool = False

    @classmethod
    def from_dict(cls, data: dict):
        type_hints_dict = get_type_hints(cls)
        filtered_data = {}
        for k, v in type_hints_dict.items():
            if k in data:
                filtered_data.update({k: data[k]})
            else:
                filtered_data.update({k: None})
        return cls(**filtered_data)

    def to_dict(self) -> dict:
        type_hints_dict = get_type_hints(self.__class__)
        data = {}
        for k, v in type_hints_dict.items():
            if hasattr(self, k):
                data.update({k: getattr(self, k)})
        return data
