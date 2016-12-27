
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel, QDialogButtonBox, QApplication

import mops.preferences
import mops.util
import mops.logger


class GUIPreferences(QDialog):
    """
    dialog popup for user preferences
    """
    def __init__(self):
        super(GUIPreferences, self).__init__()

        preferences = mops.preferences.MopsPreferences()

        layout = QGridLayout(self)

        end_point, password = preferences.get_redis_login()
        max_width = mops.util.str_max_width([end_point, password])
        self.endpoint_line_edit = QLineEdit(end_point)
        self.endpoint_line_edit.setMinimumWidth(max_width)
        self.password_line_edit = QLineEdit(password)
        self.password_line_edit.setMinimumWidth(max_width)
        layout.addWidget(QLabel('redis endpoint:', alignment=Qt.AlignRight), 0, 0)
        layout.addWidget(self.endpoint_line_edit, 0, 1)
        layout.addWidget(QLabel('redis password:', alignment=Qt.AlignRight), 1, 0)
        layout.addWidget(self.password_line_edit, 1, 1)

        layout.addWidget(QLabel(''), 2, 0)
        layout.addWidget(QLabel("If you don't already have a redis database you can get one free at:"), 3, 1)
        get_redis_le = QLineEdit("www.redislabs.com")
        get_redis_le.setReadOnly(True)
        layout.addWidget(get_redis_le, 4, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, 5, 1)

        self.show()

    def accept(self):
        preferences = mops.preferences.MopsPreferences()
        preferences.set_redis_login(self.endpoint_line_edit.text(), self.password_line_edit.text())
        super().accept()

    def get_endpoint_and_password(self):
        return self.endpoint, self.password


def main():
    import sys
    import mops.logger

    mops.logger.init()

    app = QApplication(sys.argv)
    g = GUIPreferences()
    g.exec_()
    app.exec_()

if __name__ == '__main__':
    main()