from sqlalchemy import create_engine
from sqlalchemy import Column, Table, String, Integer, BigInteger, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_config import DBConfig
from constant.messages import LogMessages
from receipt_config import MyConfig
from Excel.excel import make_excel
from log.logger import TollLogger
import time
import datetime

my_logger = TollLogger.get_logger()

db_string = DBConfig.db_string
db = create_engine(db_string)
meta = MetaData(db)
Base = declarative_base()
Session = sessionmaker(db)
session = Session()


def is_connect_db(connections):
    my_logger.info(LogMessages.connecting_to_db, extra={"tag": "info"})
    try:
        db.connect()
        my_logger.info(LogMessages.db_connected, extra={"tag": "info"})
    except:
        if connections < MyConfig.max_try_times:
            time.sleep(MyConfig.time_sleep)
            c = connections + 1
            return is_connect_db(c)
        else:
            my_logger.error(LogMessages.db_not_connected, extra={"tag": "error"})
            return False


receipt = Table('receipt', meta,
                Column('receipt_id', Integer),
                Column('receipt_name', String),
                Column('receipt_type', String),
                Column('receipt_date', String),
                Column('user_id', String),
                Column('amount', BigInteger),
                Column('card_number', String),
                Column('description', String),
                Column('is_successful', Integer))


def select_query(user_id, s_date, e_date):
    if is_connect_db(1) is False:
        return 0
    else:
        with db.connect() as conn:
            e_date += datetime.timedelta(days=1)
            print("e_date: ", e_date, "s_date: ", s_date)
            select_statement = receipt.select().where(receipt.c.user_id == user_id).where(
                receipt.c.receipt_date.between(s_date, e_date))
            print(select_statement)
            result_set = conn.execute(select_statement)
            print("result: ", result_set)
            try:
                excel_location = make_excel(result_set, user_id)
            except:
                my_logger.info(LogMessages.excel_creation_error, extra={"tag": "info"})
                return 1
            if excel_location is False:
                return 2
            else:
                my_logger.info(LogMessages.excel_creation_finished, extra={"user_id": user_id, "tag": "info"})
                return excel_location


# select_query("15415", datetime.datetime.today().strftime('%Y-%m-%d'), datetime.datetime.today().strftime('%Y-%m-%d'))
