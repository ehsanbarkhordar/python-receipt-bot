import os


class MyConfig:
    bot_id = os.environ.get('BOT_ID', None) or "receipt_bot"
    bot_token = os.environ.get('TOKEN', None) or "YOUR TOKEN"
    time_sleep = int(os.environ.get('TIME_SLEEP', None) or "2")
    max_try_times = int(os.environ.get('MAX_TRY_TIMES', None) or "3")
    upload_mime_type = os.environ.get('UPLOAD_MIME_TYPE',
                                      None) or "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    upload_file_name = os.environ.get('UPLOAD_FILE_NAME', None) or "receipts.xlsx"
    caption_text = os.environ.get('UPLOAD_CAPTION_TEXT', None) or "test_caption"
    direction_excel = os.environ.get('TEMP_EXCEL_DIR', None) or 'Excel/my_receipt_excel.xlsx'
    excel_sheet_name = os.environ.get('TEMP_EXCEL_SHEET_NAME', None) or 'Sheet1'
