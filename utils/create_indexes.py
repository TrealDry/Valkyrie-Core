from utils import database as db


db.account_comment.create_index("account_id")
db.account_stat.create_index("username", unique=True)
db.action_download.create_index("level_id")
db.action_download.create_index("account_id")
db.action_like.create_index("item_id")
db.action_like.create_index("account_id")
db.daily_level.create_index("daily_id", unique=True)
db.friend_req.create_index("account_id")
db.friend_req.create_index("recipient_id")
db.level.create_index("account_id")
db.level_comment.create_index("account_id")
db.level_comment.create_index("level_id")
db.message.create_index("account_id")
db.message.create_index("recipient_id")
db.song.create_index("account_id")

print("DONE!")
