from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from modules.application.repository import ApplicationRepository
from modules.logger.logger import Logger

COMMENT_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["task_id", "user_id", "content", "created_at", "updated_at"],
        "properties": {
            "task_id": {"bsonType": "objectId", "description": "must be a valid ObjectId reference to a task"},
            "user_id": {"bsonType": "objectId", "description": "must be a valid ObjectId reference to a user"},
            "content": {"bsonType": "string", "description": "must be a string"},
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"},
        },
    }
}


class CommentRepository(ApplicationRepository):
    collection_name = "comments"

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("task_id")
        collection.create_index("user_id")
        collection.create_index("created_at")

        add_validation_command = {
            "collMod": cls.collection_name,
            "validator": COMMENT_VALIDATION_SCHEMA,
            "validationLevel": "strict",
        }

        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            if e.code == 26:
                collection.database.create_collection(cls.collection_name, validator=COMMENT_VALIDATION_SCHEMA)
            else:
                Logger.error(message=f"OperationFailure occurred for collection comments: {e.details}")
        return True
