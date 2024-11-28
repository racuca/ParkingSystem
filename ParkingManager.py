import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QGraphicsView,
    QFrame, QVBoxLayout, QLabel, QSpinBox, QPushButton, QStatusBar,
    QGraphicsScene, QGraphicsPolygonItem, QWidget
)
from PySide6.QtGui import QMouseEvent, QPolygonF, QPen, QColor, QPainter
from PySide6.QtCore import Qt, QPointF


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
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setFrameStyle(QFrame.Box | QFrame.Plain)  # 외곽선 추가
        self.graphics_view.setLineWidth(1)  # 외곽선 두께
        splitter.addWidget(self.graphics_view)

        # 외곽선 정보 초기화
        self.polygon_points = []
        self.polygon_item = None

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

        # 사각형 그리기 UI
        right_layout.addWidget(QLabel("사각형 크기 설정:"))
        self.width_input = QSpinBox()
        self.width_input.setRange(1, 1000)  # 최소 1m, 최대 1000m
        self.width_input.setValue(20)  # 기본값
        right_layout.addWidget(QLabel("가로 길이 (m):"))
        right_layout.addWidget(self.width_input)

        self.height_input = QSpinBox()
        self.height_input.setRange(1, 1000)  # 최소 1m, 최대 1000m
        self.height_input.setValue(10)  # 기본값
        right_layout.addWidget(QLabel("세로 길이 (m):"))
        right_layout.addWidget(self.height_input)

        draw_rect_btn = QPushButton("사각형 그리기")
        draw_rect_btn.clicked.connect(self.draw_rectangle)
        right_layout.addWidget(draw_rect_btn)



        # 빈 공간 채우기
        right_layout.addStretch()
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)

        # Splitter 크기 비율을 4:1로 설정 (왼쪽: 오른쪽 = 4:1)
        splitter.setSizes([960, 240])  # [왼쪽 크기, 오른쪽 크기] 1200px 화면 기준

        # Splitter를 메인 윈도우에 설정
        self.setCentralWidget(splitter)

        # Status Bar 추가
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")  # 초기 메시지

        # 눈금 관련 변수 설정
        self.scale_factor = 10  # 1m = 10px (초기 비율)
        self.grid_step = 50  # 눈금 간격 (픽셀 단위)


    def apply_scale(self):
        scale = self.scale_input.value()
        self.status_bar.showMessage(f"스케일 설정: 1cm = {scale}m")  # 상태 표시줄 메시지
        # QGraphicsView 스케일 변경 로직 추가 예정

    def mousePressEvent(self, event: QMouseEvent):
        """마우스 클릭으로 외곽선 점 추가"""
        if event.button() == Qt.LeftButton:
            # 그래픽 뷰에서 클릭한 위치를 장면 좌표로 변환
            scene_pos = self.graphics_view.mapToScene(event.pos())
            self.polygon_points.append(scene_pos)
            self.status_bar.showMessage(f"Added point: {scene_pos.x():.2f}, {scene_pos.y():.2f}")

            # 점이 두 개 이상일 때 외곽선 업데이트
            if len(self.polygon_points) > 1:
                self.update_polygon()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """더블 클릭으로 외곽선 그리기 완료"""
        if event.button() == Qt.LeftButton and len(self.polygon_points) > 2:
            self.finalize_polygon()

    def update_polygon(self):
        """외곽선 업데이트"""
        if self.polygon_item:
            self.scene.removeItem(self.polygon_item)

        # 점 리스트를 기반으로 다각형 생성
        polygon = QPolygonF(self.polygon_points)
        pen = QPen(QColor("blue"))
        pen.setWidth(2)

        self.polygon_item = QGraphicsPolygonItem(polygon)
        self.polygon_item.setPen(pen)
        self.scene.addItem(self.polygon_item)

    def finalize_polygon(self):
        """외곽선 고정"""
        self.status_bar.showMessage("Outer boundary finalized")
        self.polygon_points = []  # 점 리스트 초기화

    def draw_rectangle(self):
        """입력된 크기의 사각형을 중앙에 그리기"""
        # 입력받은 가로/세로 크기
        width = self.width_input.value()
        height = self.height_input.value()

        # 장면 중심에 사각형 좌표 설정
        center_x = 0
        center_y = 0
        rect = self.scene.addRect(
            center_x - width / 2, center_y - height / 2, width, height,
            pen=QPen(QColor("red")),
        )

        # 상태 표시줄 업데이트
        self.status_bar.showMessage(f"Drawn rectangle: {width}m x {height}m at center")

        # 사각형 배율 조정 (1cm = 1m로 가정)
        self.graphics_view.setTransform(self.graphics_view.transform().scale(self.scale_factor, self.scale_factor))

        # 장면 갱신
        self.scene.update()

        # 화면을 업데이트하여 그린 사각형이 보이도록 하기
        self.graphics_view.viewport().update()

        # QGraphicsView의 뷰포트를 자동으로 갱신하여 사각형이 화면에 보이도록 하기
        self.graphics_view.ensureVisible(rect)

        # 눈금 그리기
        self.draw_grid()

    def draw_grid(self):
        """눈금 그리기"""
        painter = QPainter(self.graphics_view.viewport())
        painter.setPen(QPen(QColor(200, 200, 200)))  # 연한 회색 눈금

        # 눈금 간격에 맞춰 가로, 세로 선 그리기
        for x in range(-self.width() // 2, self.width() // 2, self.grid_step):
            painter.drawLine(x, -self.height() // 2, x, self.height() // 2)  # 세로 눈금
        for y in range(-self.height() // 2, self.height() // 2, self.grid_step):
            painter.drawLine(-self.width() // 2, y, self.width() // 2, y)  # 가로 눈금

        painter.end()

    def wheelEvent(self, event):
        """마우스 휠로 확대/축소"""
        angle = event.angleDelta().y()
        if angle > 0:
            self.scale_factor *= 1.1  # 확대
        else:
            self.scale_factor /= 1.1  # 축소

        # 뷰의 스케일 변경
        self.graphics_view.setTransform(self.graphics_view.transform().scale(self.scale_factor, self.scale_factor))

        # 상태 표시줄 업데이트
        self.status_bar.showMessage(f"Scale factor: {self.scale_factor:.2f}")

        # 눈금 그리기
        self.draw_grid()

        # 기본 이벤트 처리
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ParkingManager()
    main_window.show()
    sys.exit(app.exec())