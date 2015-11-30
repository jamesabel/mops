
import sys

from PySide import QtGui, QtCore

import mops.config
import mops.gui
import mops.db
import mops.system_metrics


def main(test_mode, verbose):
    app = QtGui.QApplication(sys.argv)
    config = mops.config.MopsConfig()
    endpoint, password = config.get_redis_login()

    if test_mode:
        # use this computer's metrics twice just for testing
        computers = {mops.system_metrics.get_computer_name() + '_a': mops.system_metrics.get_metrics(),
                     mops.system_metrics.get_computer_name() + '_b': mops.system_metrics.get_metrics()}
        db = None
    else:
        db = mops.db.DB(endpoint, password, verbose)
        db.set(mops.system_metrics.get_computer_name(), mops.system_metrics.get_metrics())
        computers = db.get()

    if verbose and db:
        db.dump()
    g = mops.gui.GUI(verbose)
    g.run(computers)
    sys.exit(app.exec_())