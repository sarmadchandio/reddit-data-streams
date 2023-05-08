import sqlite3
import config


class Database:
    def __init__(self, database):
        """
            database (string): name of the database that this class object will connect
        """
        # default timeout for q eury is 5 secs. If the db you are trying to query stays locked for more than 5 secs
        # Operational Error is raised
        self.connection = self._open_connection(database)
        self.cursor = self.connection.cursor()

        self._create_tables(database)


    def _query_by_name(self, thing_id):
        # If thing_id exists in the database return it, otherwise return (0,)
        """
            thing_id (reddit submission/comment): thing we are searching for
            _type ('submission' or 'comment'): this lets you know which table to look from
        """

        table_name = config.reddit_data_submissions_table if ('t3_' in thing_id) else config.reddit_data_comments_table
        self.cursor.execute(
            """
                SELECT EXISTS (SELECT 1 FROM {} WHERE id='{}' LIMIT 1)
            """.format(table_name, thing_id)
        )
        return self.cursor.fetchone()

    

    def _insert_detail(self, thing):
        # inserts 'thing' attributes into 'reddit-thing-details' table
        """
            thing (reddit comment or submission): thing obj attributes are inserted in the details table
        """
        try:
            
            comment = True if 't1' in thing.name else False
            if comment:
                self.cursor.execute(
                """
                    INSERT OR IGNORE INTO {}
                    VALUES ('{}', '{}', '{}', '{}')
                """.format(config.reddit_data_comments_table,
                           thing.name, thing.author, thing.body, thing.score)
                )
            
            else:
                selftext = None if not thing.selftext else thing.selftext
                self.cursor.execute(
                """
                    INSERT OR IGNORE INTO {}
                    VALUES ('{}', '{}', '{}', '{}', '{}')
                """.format(config.reddit_data_submissions_table,
                           thing.name, thing.author, thing.title, selftext, thing.score)
                )
            self.connection.commit()
        except Exception as e:
            config.LOG.warning(e)

    def _insert_relation(self, parent, child):
        # Inserts the parent and child relation of a 'submission/comments'
        
        try:
            self.cursor.execute(
            """
                INSERT OR IGNORE INTO {}
                VALUES ('{}', '{}', '{}')
            """.format(config.reddit_data_tree_table, 
                       parent.name, child.name, child.link_id)
            )
            self.connection.commit()
        except Exception as e:
            config.LOG.warning(e)

    def _insert_id(self, thing_id):
        try:
            self.cursor.execute(
            """
                INSERT OR IGNORE INTO {}
                VALUES ('{}')
            """.format(config.sample_pool_ids_table , thing_id)
            )
            self.connection.commit()
        except Exception as e:
            config.LOG.warning(e)
    
    def _create_tables(self, database):
        if database==config.REDDIT_DATA:
            # Creates the databases iff they are not created before
            self.cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS {}(
                        id VARCHAR(32) UNIQUE,
                        author VARCHAR(32),
                        body TEXT,
                        score INT
                    )
                """.format(config.reddit_data_comments_table)
            )
            
            self.cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS {}(
                        id VARCHAR(32) UNIQUE,
                        author VARCHAR(32),
                        title TEXT,
                        body TEXT,
                        score INT
                    )
                """.format(config.reddit_data_submissions_table)
            )

            self.cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS {}(
                        parent VARCHAR(32),
                        reply VARCHAR(32),
                        link_id VARCHAR(32),
                        CONSTRAINT UQ_parent_reply UNIQUE(parent, reply)
                    )
                """.format(config.reddit_data_tree_table)
            )
        
        
        elif database==config.SAMPLE_POOL:
            self.cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS {}(
                        id VARCHAR(32) UNIQUE
                    )
                """.format(config.sample_pool_ids_table)
            )
        
        self.connection.commit()
    
    
    # open connection to the provided database
    def _open_connection(self, database):
        return sqlite3.connect(database)

    # close the current connection to the dabase whenever class obj is destroyed
    def _close_connection(self):
        self.connection.close()