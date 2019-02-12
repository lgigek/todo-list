import logging

my_formatter = logging.Formatter("%(asctime)s %(levelname)7s "
                                 "[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s")

my_handler = logging.StreamHandler()
my_handler.setFormatter(my_formatter)

logging.getLogger().addHandler(my_handler)
logging.getLogger().setLevel(logging.DEBUG)
