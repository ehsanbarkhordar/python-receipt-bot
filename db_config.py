import os


class DBConfig:
    db_string_main = 'postgresql://{}:{}@{}:{}/{}'
    db_string = db_string_main.format(os.environ.get('PG_USER', None) or "postgres username",
                                      os.environ.get('PG_PASS', None) or "postgres password",
                                      os.environ.get('PG_HOST', None) or "localhost",
                                      os.environ.get('PG_PORT', None) or "5432",
                                      os.environ.get('PG_DB_NAME', None) or "postgres db name")
