
import time

import mops.system_metrics
import mops.server_db
import mops.logger


def test_kv():
    temp_folder = 'temp'
    mops.logger.init(temp_folder)

    collector = mops.system_metrics.AggregateCollector()
    collector.start()
    time.sleep(3)  # todo: use an event for this that the collector has collected everything
    m = collector.get_metrics()
    collector.request_exit()
    kv = mops.server_db.dict_to_kv(m)
    m2 = mops.server_db.kv_to_dict(kv)
    assert(m == m2)
