import config
import Database

### Creating/connecting to databases
db = Database.Database(config.REDDIT_DATA)
sample_pool = Database.Database(config.SAMPLE_POOL)

### 
for submission in config.SUBMISSION_STREAM:
    try:
        if submission:
            print("{} : {}".format(submission.name, submission.title))
            # Insert the submission details in the database.
            db._insert_detail(submission)
            db._insert_relation(submission.name, submission.name)

            # send comment to the sample_pool
            sample_pool._insert_id(submission.name)
    except Exception as e:
        print(e)
        config.LOG.error(e)






