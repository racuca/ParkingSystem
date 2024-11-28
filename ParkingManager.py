import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QGraphicsView,
    QFrame, QVBoxLayout, QLabel, QSpinBox, QPushButton, QStatusBar
)
from PySide6.QtCore import Qt

class ParkingManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Parking Management System")
        self.setGeometry(100, 100, 1200, 600)  # 1200x600 창 크기 설정

        # Splitter로 화면 나누기
        splitter = QSplitter(Qt.Horizontal, self)

        # 왼쪽: 주차장 화면 (QGraphicsView)
        self.graphics_view = QGraphicsView()
        self.graphics_view.setFrameStyle(QFrame.Box | QFrame.Plain)  # 외곽선 추가
        self.graphics_view.setLineWidth(1)  # 외곽선 두께
        splitter.addWidget(self.graphics_view)

        # 오른쪽: 설정 및 기능 UI
        right_panel = QFrame()  # QFrame으로 변경
        right_panel.setFrameStyle(QFrame.Box | QFrame.Plain)  # 외곽선 추가
        right_panel.setLineWidth(1)  # 외곽선 두께

        right_layout = QVBoxLayout()

        # 스케일 설정 UI
        right_layout.addWidget(QLabel("스케일 설정 (1cm = ?m):"))
        self.scale_input = QSpinBox()
        self.scale_input.setValue(1)  # 기본값: 1cm = 1m
        self.scale_input.setRange(1, 100)  # 최소 1, 최대 100
        right_layout.addWidget(self.scale_input)

        # 스케일 적용 버튼
        apply_scale_btn = QPushButton("적용")
        apply_scale_btn.clicked.connect(self.apply_scale)
        right_layout.addWidget(apply_scale_btn)

        # 빈 공간 채우기
        right_layout.addStretch()
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)

        # Splitter를 메인 윈도우에 설정
        self.setCentralWidget(splitter)

        # Status Bar 추가
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")  # 초기 메시지

    def apply_scale(self):
        scale = self.scale_input.value()
        self.status_bar.showMessage(f"스케일 설정: 1cm = {scale}m")  # 상태 표시줄 메시지
        # QGraphicsView 스케일 변경 로직 추가 예정

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ParkingManager()
    main_window.show()
    sys.exit(app.exec_())