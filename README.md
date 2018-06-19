# Receipt bot

Complete, useful and simple bot in bale-messenger using by bale Python SDK for export excel receipts from a db.

## Getting Started

Create your own bot with @bot_father in bale. Next, you can use python and install official balebot library to run this project.

### Prerequisites



1- Python3.x

2- Bot's token in bale-messenger

3- PostgreSql database

4- Graylog (Optional)


### Installing

Here is step by step instruction to run this bot.

**First step:**
Install all needed python libraries with pip.

```
pip install balebot
pip install SQLAlchemy
pip install psycopg2-binary
pip install openpyxl
```

**Second step:**
install [postgreSql](https://www.postgresql.org/) local or use a ready-up database.

**Third step:**
Set your own config in receipt_config.py, db_config.py and log_config.py. 

## Running the bot

Run receipt_bot.py and it would be connected if you could see something like below.
```
2018-05-26 18:50:19,239  network.py:32  DEBUG:
"connect: wss://api.bale.ai/v1/bots/bad3fe107273e3c521f4856ee0dbe83bc5a91a16"
```
## Versioning

1.0.0

## Authors

* **[EhsanBarkhordar](https://github.com/ehsanbarkhordar)** -initial work

See also the list of [contributors](https://github.com/ehsanbarkhordar/python-receipt-bot/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details