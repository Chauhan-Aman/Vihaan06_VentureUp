from models import user_dbs

user_collection = user_dbs['users']



def get_info(username):
    # return user info
    try:
        user_data = user_collection.find_one(
            {"_id": username}
        )

        if user_data:
            return user_data
    except Exception as e:
        print(f"Error/get_info: {e}")
        return False


def register(data):
    # register user
    try:
        user_collection.insert_one(data)
        return True
    except Exception as e:
        print(f"Error/register: {e}")
        return False


def register_mentor(mentor_id, mentor_data):
    # update the mentor's database
    try:
        user_collection.update_one(
            {"_id": mentor_id},
            {"$set": mentor_data}
        )
    except Exception as e:
        print(f"Error/register_mentor: {e}")


def register_investor(investor_id, investor_data):
    # update investor's database
    try:
        user_collection.update_one(
            {"_id": investor_id},
            {"$set": investor_data}
        )
    except Exception as e:
        print(f"Error/register_investor: {e}")
