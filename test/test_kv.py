
import mops.system_metrics
import mops.db
import mops.logger


def test_kv():
    temp_folder = 'temp'
    mops.logger.init(temp_folder)

    m = mops.system_metrics.get_metrics()
    kv = mops.db.dict_to_kv(m)
    m2 = mops.db.kv_to_dict(kv)
    assert(m == m2)
