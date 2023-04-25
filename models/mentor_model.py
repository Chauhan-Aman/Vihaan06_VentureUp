from models import user_dbs

post_collection = user_dbs['post']


def add_post(post_data):
    # add a post
    try:
        post_collection.insert_one(post_data)
    except Exception as e:
        print(f"Error/add_post: {e}")


def get_post(mentors):
    posts = []
    try:
        public_posts = post_collection.find(
            {"private": False}
        )

        for post in public_posts:
            posts.append(post)
    except Exception as e:
        print(f"Error/get_post: {e}")
    
    
