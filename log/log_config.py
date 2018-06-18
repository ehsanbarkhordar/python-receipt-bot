import logging
import os


class LogConfig:
    # 0:print to output        1:use graylog       2:both 0 and 1
    use_graylog = os.environ.get('BOT_USE_GRAYLOG', None) or "0"
    source = os.environ.get('LOG_SOURCE', None) or "receipt_bot"
    graylog_host = os.environ.get('BOT_GRAYLOG_HOST', None) or "graylog host"
    graylog_port = os.environ.get('BOT_GRAYLOG_PORT', None) or 12201
    log_level = int(os.environ.get('BOT_LOG_LEVEL', None) or logging.DEBUG)
    log_facility_name = os.environ.get('BOT_LOG_FACILITY_NAME', None) or "receipt_bot"
