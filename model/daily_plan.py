from commonkit.sqlalchemy.base_dto import BaseDTO
from commonkit.utilities.uuid_utilities import UUIDUtilities
class DailyPlan(BaseDTO):
    id: str = UUIDUtilities.generate_unique_string()
    task:str = None
    goal:str = None
    day_session:str = None
    day:str = None
    user_name:str = None
    chat_id:int = None
    is_done:bool = False