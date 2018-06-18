class TxtMessages:
    start_conversation = "*سلام. من بات تهیه گزارش هستم.*\nبرای شروع دکمه زیر را بفشارید:"
    take_start_date = "تاریخ شروع گزارش را در قالب یک عدد ۸ رقمی" \
                      " وارد کنید:\n*مثال: ۶ بهمن ۹۶ را به صورت ۱۳۹۶۱۰۰۶ و با اعداد لاتین وارد کنید*"

    take_end_date = "تاریخ خاتمه گزارش را در قالب یک عدد ۸ رقمی" \
                    " وارد کنید:\n*مثال: مثال: ۱۳ فروردین ۹۷ را به صورت ۱۳۹۷۰۱۱۳ و با اعداد لاتین وارد کنید*"

    receipt_ready = "گزارش مورد نظر شما در حال آماده‌سازی است. لطفا شکیبایی فرمایید."
    no_data_found = "در این بازه هیچ تراکنشی یافت نشد."
    invalid_num = "تاریخ ورودی باید فقط در قالب یک عدد ۸ رقمی باشد."
    invalid_length = "طول عدد تاریخ ورودی باید ۸ رقم باشد."
    invalid_date = "لطفا تاریخ را به صورت صحیح وارد کنید."
    try_later = "متاسفیم!\nدر حال حاظر بات قادر به پاسخ گویی نمی باشد.\nلطفا کمی بعد دوباره تلاش کنید."
    e_date_start_after_s_date = "تاریخ پایانی باید پس از تاریخ شروع باشد."
    account_no = "شماره کارت/شماره حساب انجام تراکنش"
    account_name = "نام کارت/شماره حساب انجام تراکنش"
    transaction_type = "نوع تراکنش"
    transaction_id = "شماره پیگیری"
    is_successful = "وضعیت"
    amount = "واریز/برداشت"
    description1 = "شرح ۱"
    description2 = "شرح ۲"
    description3 = "شرح ۳"
    details = "اطلاعات"
    fail = "ناموفق"
    success = "موفق"
    date = "تاریخ"
    time = "ساعت"
    start = "شروع"


class LogMessages:
    start_conversation = "conversation is started"
    finish_conversion = "conversation is finished"

    start_date_received = "first date is received"
    end_date_received = "last date is received"

    excel_creation_started = "excel creation is started"
    excel_creation_finished = "excel creation is finished"
    excel_creation_error = "excel creation has a error"
    excel_deleted = "excel is deleted"

    no_data_found = "no data found in this period"
    data_found = "Data found in this period"

    invalid_date = "date is invalid"
    valid_date = "Date entered is valid"

    can_not_send_message = "bot can't send message"
    upload_fail = "upload failed"
    upload_success = "upload success"
    uploading_started = "uploading_started"

    connecting_to_db = "Connecting to database ..."
    db_connected = "Database connected successfully"
    db_not_connected = "Database does not connected"

    e_date_should_older_log = "end date should be older than start date"
    cannot_make_excel = "can not make excel"
    exit_bot = "bot exit"
