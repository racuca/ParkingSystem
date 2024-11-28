import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("PySide6 설치 성공!")
label.show()
sys.exit(app.exec_())