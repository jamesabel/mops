
import mops.preferences
import mops.logger


def test_preferences():
    temp_folder = 'temp'
    mops.logger.init(temp_folder)

    c = mops.preferences.MopsPreferences(temp_folder)
    c.clear()
    endpoint = 'my_endpoint'
    password = 'my_password'
    run_on_startup = True
    c.set_redis_login(endpoint, password)
    c.set_run_on_startup(run_on_startup)
    read_endpoint, read_password = c.get_redis_login()
    read_run_on_startup = c.get_run_on_startup()
    assert(read_endpoint == endpoint)
    assert(read_password == password)
    assert(read_run_on_startup == run_on_startup)

