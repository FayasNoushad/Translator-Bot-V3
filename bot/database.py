import motor.motor_asyncio
from .vars import DEFAULT_LANGUAGE, DATABASE


class Database:
    def __init__(self, uri, database_name="Translator-Bot"):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.cache = {}
    
    def new_user(self, id):
        return {"id": id, "language": DEFAULT_LANGUAGE}
    
    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)
    
    async def get_user(self, id):
        user = self.cache.get(id)
        if user is not None:
            return user
        
        user = await self.col.find_one({"id": int(id)})
        self.cache[id] = user
        return user
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
    
    async def get_lang(self, id):
        user = await self.col.find_one({'id': int(id)})
        if user:
            return user.get("language", DEFAULT_LANGUAGE)

    async def update_lang(self, id, language):
        await self.col.update_one(
            {"id": id}, {"$set": {"language": language}}
        )


db = Database(DATABASE)
