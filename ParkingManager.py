import math
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QGraphicsView,
    QFrame, QVBoxLayout, QLabel, QSpinBox, QPushButton, QStatusBar,
    QGraphicsScene, QGraphicsPolygonItem, QWidget, QGraphicsRectItem, QSlider
)
from PySide6.QtGui import QMouseEvent, QPolygonF, QPen, QColor, QPainter, QBrush
from PySide6.QtCore import Qt, QPointF, QRectF


class GraphicsView(QGraphicsView):
    def __init__(self, dpi, scalefactor=1, parent=None):
        super().__init__(parent)
        self.scalefactor = scalefactor
        self.dpi = dpi  # 화면 DPI
        self.pixels_per_cm = dpi / 2.54  # 1cm 당 픽셀 수 계산
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)  # 외곽선 추가
        self.setLineWidth(1)
        self.setRenderHint(QPainter.Antialiasing)  # 안티앨리어싱 활성화
        self.setRenderHint(QPainter.SmoothPixmapTransform)  # 스무스 픽스맵 활성화

        # 눈금자 그리기
        self.draw_ruler()

    def resizeEvent(self, event):
        """뷰가 리사이즈될 때 sceneRect를 자동으로 조정"""
        rect = self.viewport().rect()  # 뷰포트의 픽셀 영역
        scene_rect = QRectF(0, 0, rect.width(), rect.height())
        self.setSceneRect(scene_rect)  # Scene 영역 설정
        self.draw_ruler()  # 눈금자 다시 그리기
        super().resizeEvent(event)

    def draw_ruler(self):
        """가장자리에 눈금자를 그리는 함수"""
        self.scene.clear()
        pen = QPen(Qt.black)
        pen.setWidth(1)

        # 눈금자 간격 계산
        spacing = self.scalefactor * self.pixels_per_cm
        rect = self.sceneRect()

        # 위쪽 눈금자
        x = 0
        while x <= rect.width():
            self.scene.addLine(x, 0, x, 5, pen)  # 위쪽 눈금
            x += spacing

        # 왼쪽 눈금자
        y = 0
        while y <= rect.height():
            self.scene.addLine(0, y, 5, y, pen)  # 왼쪽 눈금
            y += spacing

        # 아래쪽 눈금자
        x = 0
        while x <= rect.width():
            self.scene.addLine(x, rect.height(), x, rect.height() - 5, pen)  # 아래쪽 눈금
            x += spacing

        # 오른쪽 눈금자
        y = 0
        while y <= rect.height():
            self.scene.addLine(rect.width(), y, rect.width() - 5, y, pen)  # 오른쪽 눈금
            y += spacing

    def set_scalefactor(self, factor):
        """scalefactor 를 업데이트하고 눈금자 다시 그리기"""
        self.scalefactor = factor
        self.draw_ruler()



class ParkingManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 사용자 입력: 모니터 해상도와 크기
        horizontal_resolution = 1920  # 모니터 가로 해상도
        vertical_resolution = 1080  # 모니터 세로 해상도
        diagonal_size_inch = 24  # 모니터 대각선 길이 (인치)

        # DPI 계산
        dpi = math.sqrt(horizontal_resolution ** 2 + vertical_resolution ** 2) / diagonal_size_inch

        self.setWindowTitle("Parking Management System")
        self.setGeometry(100, 100, 1200, 600)  # 1200x600 창 크기 설정

        # Splitter로 화면 나누기
        splitter = QSplitter(Qt.Horizontal, self)

        self.graphics_view = GraphicsView(dpi, parent=splitter)
        splitter.addWidget(self.graphics_view)

        # 오른쪽: 설정 및 기능 UI
        right_panel = QFrame()  # QFrame으로 변경
        right_panel.setFrameStyle(QFrame.Box | QFrame.Plain)  # 외곽선 추가
        right_panel.setLineWidth(1)  # 외곽선 두께

        right_layout = QVBoxLayout()

        # 스케일 설정 UI
        right_layout.addWidget(QLabel("Scale Factor"))
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)  # 최소 배율
        slider.setMaximum(10)  # 최대 배율
        slider.setValue(1)  # 기본 값
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)

        # 슬라이더 값 변경 이벤트 연결
        slider.valueChanged.connect(self.update_scalefactor)
        right_layout.addWidget(slider)

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

        # 외곽선 정보 초기화
        self.polygon_points = []
        self.polygon_item = None

        # 눈금 관련 변수 설정
        self.scale_factor = 1  # 1m = 10px (초기 비율)
        self.grid_step = 50  # 눈금 간격 (픽셀 단위)

    def update_scalefactor(self, value):
        """scalefactor 변경 처리"""
        self.graphics_view.set_scalefactor(value)


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
        #rect = self.scene.addRect(
        #    center_x - width / 2, center_y - height / 2, width, height,
        #    pen=QPen(QColor("red")),
        #)
        rect = QGraphicsRectItem(0, 0, width, height)
        pen = QPen(Qt.GlobalColor.cyan)
        pen.setWidth(1)
        rect.setPen(pen)
        rect.setPos(0, 0)
        self.scene.addItem(rect)

        # 상태 표시줄 업데이트
        self.status_bar.showMessage(f"Drawn rectangle: {width}m x {height}m at center")

        # QGraphicsView의 스케일링을 추가하여 사각형이 보이도록
        self.graphics_view.scale(self.scale_factor, self.scale_factor)

        # 화면을 업데이트하여 그린 사각형이 보이도록 하기
        self.graphics_view.viewport().update()

        # QGraphicsView의 뷰포트를 자동으로 갱신하여 사각형이 화면에 보이도록 하기
        #self.graphics_view.ensureVisible(rect)


    def draw_grid(self, painter):
        """눈금 그리기"""
        # 그리드 간격을 스케일에 맞게 계산
        grid_step_scaled = self.grid_step * self.scale_factor

        # 눈금 간격에 맞춰 가로, 세로 선 그리기
        width = self.graphics_view.width()
        height = self.graphics_view.height()

        # 눈금 그리기 (화면 중앙을 기준으로 시작)
        left = -width // 2
        top = -height // 2
        right = width // 2
        bottom = height // 2

        print(left, top, right, bottom)

        # 세로 눈금 그리기
        print("세로눈금그리기")
        x = left
        while x < right:
            painter.drawLine(x, top, x, bottom)
            x += grid_step_scaled

        # 가로 눈금 그리기
        print("가로눈금그리기")
        y = top
        while y < bottom:
            painter.drawLine(left, y, right, y)
            y += grid_step_scaled


    def wheelEvent(self, event):
        """마우스 휠로 확대/축소"""
        angle = event.angleDelta().y()
        scale_change = 0.5  # 확대/축소 비율 조정
        if angle > 0:
            self.scale_factor += scale_change  # 확대
        else:
            self.scale_factor -= scale_change  # 축소

        print(f"scale factor {self.scale_factor}")
        # 확대/축소가 너무 커지지 않도록 범위 제한
        self.scale_factor = max(0.1, min(self.scale_factor, 100))  # 스케일 제한 (최소 0.1배, 최대 3배)

        # 확대/축소 적용
        self.graphics_view.resetTransform()  # 기존 변환 초기화
        self.graphics_view.scale(self.scale_factor, self.scale_factor)  # 새 스케일 적용

        # 상태 표시줄 업데이트
        self.status_bar.showMessage(f"Scale factor: {self.scale_factor:.2f}")

        # 화면을 다시 그리기
        self.graphics_view.viewport().repaint()

        # 기본 이벤트 처리
        event.accept()

    def drawBackground(self, painter, rect):
        print("drawBackground")
        """배경 그리기 (눈금 그리기)"""
        # 그리드 그리기
        painter.setPen(QPen(Qt.lightGray, 1, Qt.DashLine))  # 그리드 선 설정
        self.draw_grid(painter)

        # 화면을 갱신하도록 강제로 업데이트
        #self.graphics_view.viewport().repaint()

    def resizeEvent(self, event):
        """창 크기 조정 시 호출되어 drawBackground 호출을 보장"""
        self.graphics_view.viewport().update()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ParkingManager()
    main_window.show()
    sys.exit(app.exec())