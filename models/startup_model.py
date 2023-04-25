from models import startup_dbs

startup_collection = startup_dbs['startup']
blog_collection = startup_dbs['blogs']


def register_startup(startup_data):
    # register startup
    try:
        startup_collection.insert_one(startup_data)
    except Exception as e:
        print(f"Error/register_startup: {e}")


def get_startup(name=False, founder=False):
    if name:
        try:
            startup_data = startup_collection.find_one(
                {"_id": name}
            )

            return startup_data
        except Exception as e:
            print(f"Error/get_startup/name: {e}")
            return False
    
    if founder:
        try:
            startup_data = startup_collection.find_one(
                {"founder": founder}
            )

            return startup_data
        except Exception as e:
            print(f"Error/get_startup/founder: {e}")
            return False


def get_blogs(company_id):
    # return blogs written by a startup
    try:
        blogs = blog_collection.find(
            {"company": company_id}
        )

        return blogs
    except Exception as e:
        print(f"Error/get_blogs: {e}")
        return False


def add_blog(blog_data):
    # add a blog
    try:
        blog_collection.insert_one(blog_data)
    except Exception as e:
        print(f"Error/add_blog: {e}")


def get_blog(blogid):
    try:
        blog_data = blog_collection.find_one(
            {"_id": blogid}
        )

        return blog_data
    except Exception as e:
        print(f"Error/get_blog: {e}")
        return False


def get_startups():
    try:
        data = startup_collection.find({})
        return data
    except Exception as e:
        print(f"Error/get_startup: {e}")
        return False
