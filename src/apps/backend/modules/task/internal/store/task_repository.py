from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from modules.application.repository import ApplicationRepository
from modules.logger.logger import Logger
from modules.task.internal.store.task_model import TaskModel

TASK_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "description", "created_at", "updated_at"],
        "properties": {
            "title": {"bsonType": "string", "description": "must be a string"},
            "description": {"bsonType": "string", "description": "must be a string"},
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"},
        },
    }
}


class TaskRepository(ApplicationRepository):
    collection_name = TaskModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("title")

        add_validation_command = {
            "collMod": cls.collection_name,
            "validator": TASK_VALIDATION_SCHEMA,
            "validationLevel": "strict",
        }

        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            if e.code == 26:
                collection.database.create_collection(cls.collection_name, validator=TASK_VALIDATION_SCHEMA)
            else:
                Logger.error(message=f"OperationFailure occurred for collection tasks: {e.details}")
        return True
