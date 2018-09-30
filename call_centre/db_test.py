from db import *


init_db()

# assert insert_phone_number("53") == 1
#
# assert insert_phone_number("52") == 2
#
# assert insert_phone_number("52") == -1


# insert_incident("test1", "0x3f", 1, 1, 1, 1)
#
# insert_incident("test2", "0x3f", 1, 1, 1, 1)
#
# insert_incident(
#         "test1", "0x3f", 1, 1, 1, 1, datetime(year = 2018, month = 10, day = 1, hour = 0, minute = 0, second = 0)
# )

insert_report("p1", "i1", "loc1", 1, 1, 1, 1)
insert_report("p2", "i1", "loc1", 1, 1, 1, 1)

assert insert_report("p1", "i1", "loc1", 1, 1, 1, 1) == -1

print(query_time_interval(datetime.now() - timedelta(minutes = 15), datetime.now() + timedelta(minutes = 15)))

# Pls add ur test cases below
