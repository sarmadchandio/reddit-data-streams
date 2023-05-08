import config
import Database

### Creating/connecting to database
db = Database.Database(config.REDDIT_DATA)
sample_pool = Database.Database(config.SAMPLE_POOL)

### Keep streaming data. If none write to the data base, clear cache
for comment in config.COMMENT_STREAM:
    try:
        if db._query_by_name(comment):
            print("{} : {}".format(comment.name, comment.body))
            # Insert the comment details in the database.
            db._insert_detail(comment)
            db._insert_relation(comment.parent_id, comment.name)

            # send comment to the sample_pool
            sample_pool._insert_id(comment.name)
    except Exception as e:
        print(e)
        config.LOG.error(e)