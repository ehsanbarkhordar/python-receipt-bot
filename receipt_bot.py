import asyncio
from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater
from constant.messages import TxtMessages, LogMessages
from log.logger import TollLogger
from db.db_handler import select_query
from Jalali.jalali import Persian, date_validation, date_format_converter, check_dates_order
import os
import time
from receipt_config import MyConfig

updater = Updater(token=MyConfig.bot_token,
                  loop=asyncio.get_event_loop())
bot = updater.bot
dispatcher = updater.dispatcher
my_logger = TollLogger.get_logger()


def success(response, user_data):
    print("success : ", response)
    print(user_data)


def failure(response, user_data):
    print("failure : ", response)
    user_data = user_data['kwargs']
    user_peer = user_data["user_peer"]
    try_times = int(user_data["try_times"])
    message = user_data["message"]
    if try_times < MyConfig.max_try_times:
        try_times += 1
        kwargs = {"message": message, "user_peer": user_peer, "try_times": try_times}
        time.sleep(MyConfig.time_sleep)
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
    else:
        my_logger.error(LogMessages.can_not_send_message, extra={"tag": "error"})


@dispatcher.command_handler(["start"])
def conversation_starter(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    btn_list = [TemplateMessageButton(text=TxtMessages.start, value=TxtMessages.start, action=0)]
    general_message = TextMessage(TxtMessages.start_conversation)
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
    my_logger.info(LogMessages.start_conversation, extra={"user_id": user_id, "tag": "info"})
    dispatcher.register_conversation_next_step_handler(update, [CommandHandler("start", conversation_starter),
                                                                MessageHandler(TemplateResponseFilter(
                                                                    keywords=[TxtMessages.start]), request_start_date)])


def request_start_date(bot, update):
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    message = TextMessage(TxtMessages.take_start_date)
    kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
    my_logger.info(LogMessages.start_conversation, extra={"user_id": user_id, "tag": "info"})
    dispatcher.register_conversation_next_step_handler(update, [CommandHandler("start", conversation_starter),
                                                                MessageHandler(TextFilter(), start_date)])


def start_date(bot, update):
    s_date = update.get_effective_message().text
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    my_logger.debug(LogMessages.start_date_received, extra={"user_id": user_id, "tag": "debug"})
    validation = date_validation(s_date)
    if validation is True:
        my_logger.info(LogMessages.valid_date, extra={"user_id": user_id, "tag": "info"})
        dispatcher.set_conversation_data(update=update, key="start_date", value=s_date)
        message = TextMessage(TxtMessages.take_end_date)
        kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
        dispatcher.register_conversation_next_step_handler(update, [CommandHandler("start", conversation_starter),
                                                                    MessageHandler(TextFilter(), end_date)])
    else:
        my_logger.warning(LogMessages.invalid_date, extra={"user_id": user_id, "tag": "warning"})
        message = TextMessage(validation)
        kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
        dispatcher.register_conversation_next_step_handler(update, [CommandHandler("start", conversation_starter),
                                                                    MessageHandler(TextFilter(), start_date)])


def end_date(bot, update):
    e_date = update.get_effective_message().text
    user_peer = update.get_effective_user()
    user_id = user_peer.peer_id
    my_logger.debug(LogMessages.end_date_received, extra={"user_id": user_id, "tag": "debug"})
    s_date = dispatcher.get_conversation_data(update, key="start_date")
    if date_validation(e_date) is not True:
        message = TextMessage(date_validation(e_date))
        kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
        my_logger.warning(LogMessages.invalid_date, extra={"user_id": user_id, "tag": "warning"})
        dispatcher.register_conversation_next_step_handler(update, [CommandHandler("start", conversation_starter),
                                                                    MessageHandler(TextFilter(), end_date)])
        return 1
    if check_dates_order(s_date, e_date) is not True:
        message = TextMessage(check_dates_order(s_date, e_date))
        kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
        my_logger.warning(LogMessages.e_date_should_older_log, extra={"user_id": user_id, "tag": "warning"})
        dispatcher.register_conversation_next_step_handler(update, [CommandHandler("start", conversation_starter),
                                                                    MessageHandler(TextFilter(), end_date)])
        return 1
    s_date = Persian(date_format_converter(s_date)).gregorian_datetime()
    e_date = Persian(date_format_converter(e_date)).gregorian_datetime()
    excel = select_query(user_id, s_date, e_date)
    if excel == 0:
        message = TextMessage(TxtMessages.try_later)
        my_logger.error(LogMessages.db_not_connected, extra={"tag": "error"})
        kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure,
                         kwargs=kwargs)
        dispatcher.finish_conversation(update)
        my_logger.debug(LogMessages.finish_conversion, extra={"user_id": user_id, "tag": "info"})
        return 1
    elif excel == 1:
        message = TextMessage(TxtMessages.try_later)
        my_logger.error(LogMessages.cannot_make_excel, extra={"tag": "error"})
        kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure,
                         kwargs=kwargs)
        dispatcher.finish_conversation(update)
        my_logger.debug(LogMessages.finish_conversion, extra={"user_id": user_id, "tag": "info"})
        return 1
    elif excel == 2:
        message = TextMessage(TxtMessages.no_data_found)
        kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(message, user_peer, success_callback=success, failure_callback=failure,
                         kwargs=kwargs)
        my_logger.error(LogMessages.no_data_found, extra={"user_id": user_id, "tag": "error"})
        dispatcher.finish_conversation(update)
        my_logger.debug(LogMessages.finish_conversion, extra={"user_id": user_id, "tag": "info"})
        return 1

    def file_upload_success(result, user_data):
        """Its the link of upload photo but u cant see anything with it because you need to take a token from server.
            actually this link is just for uploading a file not download. If you want to download this file you should
            use get_file_download_url() and take a token from server.
        """
        print("upload was successful : ", result)
        print(user_data)
        my_logger.info(LogMessages.upload_success, extra={"user_id": user_id, "tag": "info"})
        file_id = str(user_data.get("file_id", None))
        access_hash = str(user_data.get("user_id", None))
        excel_message = DocumentMessage(file_id=file_id, access_hash=access_hash, name=MyConfig.upload_file_name,
                                        file_size=os.path.getsize(excel),
                                        mime_type=MyConfig.upload_mime_type,
                                        caption_text=TextMessage(text=MyConfig.caption_text),
                                        file_storage_version=1)

        kwargs = {"message": excel_message, "user_peer": user_peer, "try_times": 1}
        bot.send_message(excel_message, user_peer, success_callback=success, failure_callback=failure,
                         kwargs=kwargs)
        os.remove(excel)
        my_logger.info(LogMessages.excel_deleted, extra={"user_id": user_id, "tag": "info"})

    def file_upload_failure(result, user_data):
        my_logger.error(LogMessages.upload_fail, extra={"user_id": user_id, "tag": "error"})
        user_data = user_data['kwargs']
        try_times = int(user_data["try_times"])
        if try_times < MyConfig.max_try_times:
            try_times += 1
            kwargs = {"try_times": try_times}
            time.sleep(MyConfig.time_sleep)
            bot.upload_file(file=excel, file_type="file", success_callback=file_upload_success,
                            failure_callback=file_upload_failure, kwargs=kwargs)
        else:
            my_logger.error(LogMessages.exit_bot, extra={"tag": "error"})
            import sys
            sys.exit()

    kwargs = {"try_times": 1}
    my_logger.info(LogMessages.uploading_started, extra={"user_id": user_id, "tag": "info"})
    bot.upload_file(file=excel, file_type="file", success_callback=file_upload_success,
                    failure_callback=file_upload_failure, kwargs=kwargs)
    dispatcher.finish_conversation(update)
    my_logger.debug(LogMessages.finish_conversion, extra={"user_id": user_id, "tag": "debug"})


updater.run()
