
import time
import sys

from PySide.QtGui import *

import mops.system_metrics
import mops.server_db
import mops.logger
import mops.gui_systems


def test_gui_systems():
    temp_folder = 'temp'
    mops.logger.init(temp_folder)

    app = QApplication(sys.argv)

    collector = mops.system_metrics.AggregateCollector()
    collector.start()
    time.sleep(3)  # todo: use an event for this that the collector has collected everything
    m = collector.get_metrics()
    gui = mops.gui_systems.GUI(False)
    gui.run(m)
    collector.request_exit()

    mops.logger.init()

