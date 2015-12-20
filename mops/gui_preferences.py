
from PySide.QtGui import QGroupBox, QPushButton, QWidget, QGridLayout, QLabel, QFontMetrics, QLineEdit, QFont, \
    QInputDialog, QDialog, QVBoxLayout, QDateTimeEdit, QDialogButtonBox, QApplication
from PySide.QtCore import QDateTime, Qt

import mops.preferences

class GUIPreferences(QDialog):
    def __init__(self):
        super(GUIPreferences, self).__init__()

        preferences = mops.preferences.MopsPreferences()

        layout = QGridLayout(self)

        end_point, password = preferences.get_redis_login()
        self.endpoint_line_edit = QLineEdit(end_point)
        self.password_line_edit = QLineEdit(password)
        layout.addWidget(QLabel('redis endpoint'), 0, 0)
        layout.addWidget(self.endpoint_line_edit, 0, 1)
        layout.addWidget(QLabel('redis password'), 1, 0)
        layout.addWidget(self.password_line_edit, 1, 1)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.show()

    def accept(self):
        preferences = mops.preferences.MopsPreferences()
        preferences.set_redis_login(self.endpoint_line_edit.text(), self.password_line_edit.text())
        super().accept()

    def get_endpoint_and_password(self):
        return self.endpoint, self.password


def main():
    import sys
    app = QApplication(sys.argv)
    g = GUIPreferences()
    g.exec_()
    app.exec_()

if __name__ == '__main__':
    main()