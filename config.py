import praw
import logging
# This is a config file with global variables. These can be accessed by using config.<varname>
# in any other file

# main storage data base. Stores all the posts/comments that a stream encounters
REDDIT_DATA = 'reddit-data.db'
reddit_data_submissions_table = 'reddit_submission_details'
reddit_data_comments_table = 'reddit_comment_details'
reddit_data_tree_table = 'reddit_thing_tree'

# Only stores the ids of the new comments/posts that haven't been added to reddit-clone.
SAMPLE_POOL = 'sample-pool.db'
sample_pool_ids_table = 'reddit_thing_ids'

# praw reddit instance to make streams
REDDIT = praw.Reddit(
    client_id = "_d8oiYvEnv94dyjqZrnJIg",
    client_secret = "-XsxLbo7FCW3-z_Bl9xroF7hsUuswg",
    password ="F:C5qPZ9dgSn:Wd",
    user_agent ="shadow-clone",
    username ="Dora-The-Explorerrr"
)

# stream objects
SUBMISSION_STREAM = REDDIT.subreddit("AskReddit").stream.submissions(skip_existing=True, pause_after=3)
COMMENT_STREAM = REDDIT.subreddit("AskReddit").stream.comments(skip_existing=True, pause_after=3)


# TODO: Add file and stream handler to the logger so have the logs in file and you see them on the
# stream as well.

# Formatting the logger
logging.basicConfig(filename='all_files.log', level=logging.INFO, 
                    format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
# database logger
LOG = logging.getLogger('all_files')









