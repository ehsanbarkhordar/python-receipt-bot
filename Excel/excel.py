from Jalali.jalali import Gregorian
from openpyxl.styles.colors import RED, GREEN
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from receipt_config import MyConfig
from constant.messages import TxtMessages, LogMessages
from log.logger import TollLogger
import string
import datetime

alphabet = list(string.ascii_uppercase)
my_logger = TollLogger.get_logger()


def make_file_location(user_id):
    location = "Excel/" + str(user_id) + str(datetime.datetime.now().strftime('_%y%m%d%H%M%S%f')) + ".xlsx"
    return location


def make_excel(result_set, user_id):
    if not result_set.rowcount > 0:
        my_logger.info(LogMessages.no_data_found, extra={"user_id": user_id, "tag": "info"})
        return False
    my_logger.info(LogMessages.excel_creation_started, extra={"user_id": user_id, "tag": "info"})
    location = make_file_location(user_id)
    template = load_workbook(filename=MyConfig.direction_excel)
    sheet1 = template[MyConfig.excel_sheet_name]
    row = 2
    for r in result_set:
        gregorian_date = r.receipt_date.strftime("%Y-%m-%d")
        gregorian_time = r.receipt_date.strftime("%H:%M:%S")
        jalali = Gregorian(gregorian_date).persian_string()
        if r.is_successful == 1:
            success = TxtMessages.success
        else:
            success = TxtMessages.fail
        red = Font(color=RED)
        green = Font(color=GREEN)
        al = Alignment(horizontal="center", vertical="center")

        expenses = [jalali, gregorian_time, r.amount, r.receipt_id, r.receipt_name, r.receipt_type,
                    r.user_id, success, r.amount, r.card_number, r.description]

        for i in range(len(expenses)):
            sheet1[alphabet[i] + str(row)].value = expenses[i]
            sheet1[alphabet[i] + str(row)].alignment = al

            # if alphabet[i] == 'C' and sheet1[alphabet[i] + str(row)].value:
            #     amount = str(sheet1[alphabet[i] + str(row)].value)
            #     if amount[0] == "-":
            #         sheet1[alphabet[i] + str(row)].font = red
            #     else:
            #         sheet1[alphabet[i] + str(row)].font = green
        row += 1

    template.save(location)
    return location
