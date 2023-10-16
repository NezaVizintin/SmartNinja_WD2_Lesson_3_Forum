import smartninja_redis
import os
import uuid

redis = smartninja_redis.from_url(os.environ.get("REDIS_URL"))


def csrf_token_set(username):
    csrf_token = str(uuid.uuid4())  # create csrf token

    redis.set(name=csrf_token, value=username)  # store CSRF token into Redis for that specific user
    # putting the csrf token as the name means we can store many tokens for a single user
    # (if the user would have many forms opened in different tabs)

    return csrf_token

def csrf_token_check(csrf_token, username):
    if csrf_token:
        stored_csrf_username = redis.get(name=csrf_token)  # get username value stored under the csrf name from redis
        if not stored_csrf_username:
            return False
#        if stored_csrf_username and stored_csrf_username == username:

        return stored_csrf_username.decode() == username
    else:
        return False
