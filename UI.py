from PySide6.QtCore import Qt
from PySide6.QtCore import QRect
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6 import QtGui
import sys

f = open("Theme.qss", 'r')
pss = f.read()


# <OVERRIDINGS>
class QScrollArea(QScrollArea):
    def __init__(self, *args, **kwargs):
        super(QScrollArea, self).__init__(*args, **kwargs)

        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)


class QPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        self.setMinimumHeight(50)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


class QVBoxLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QVBoxLayout, self).__init__(*args, **kwargs)

        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)


class QHBoxLayout(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QHBoxLayout, self).__init__(*args, **kwargs)

        self.setAlignment(Qt. AlignmentFlag.AlignCenter)
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
# </OVERRIDINGS>


class WindowMain(QWidget):

    def __init__(self):
        super(WindowMain, self).__init__()

        self.setup_ui()

        self.setStyleSheet(pss)

        layout_main = QVBoxLayout()

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.NoFrame)

        scoll_contens = QWidget(self)
        layout_scollarea = QVBoxLayout()
        layout_scollarea.setSpacing(20)
        layout_scollarea.setContentsMargins(0, 20, 0, 20)

        group_ex_appbar = QWidget(self)
        layout_ex_appbar = QVBoxLayout()
        layout_ex_appbar.setAlignment(Qt.AlignmentFlag.AlignTop)

        widget = QWidget(self)
        widget.setFixedHeight(140)
        layout_widget = QHBoxLayout()

        image = QtGui.QPixmap("./assets/C01/Thumbnail.png")
        preview = QLabel(self)
        preview.setPixmap(image)
        preview.setFixedHeight(120)
        preview.setFixedWidth(120)
        preview.setScaledContents(True)

        layout_widget.addWidget(preview)
        widget.setLayout(layout_widget)

        title = QLabel("OSC for Watch", self, objectName="Heading")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        currunt = QLabel("YYYY-MM-DD, HH : MM", self, objectName="Sub")
        currunt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_ex_appbar.addWidget(widget)
        layout_ex_appbar.addWidget(title)
        layout_ex_appbar.addWidget(currunt)

        group_ex_appbar.setLayout(layout_ex_appbar)
        layout_scollarea.addWidget(group_ex_appbar)

        ip_btn = QPushButton(self, objectName="Rounded")

        ip_label = QLabel("IP", ip_btn, objectName="Heading")
        ip_label.setGeometry(QRect(24, 5, 320, 20))

        ip_text = QLabel("127.0.0.1", ip_btn, objectName="SubAccent")
        ip_text.setGeometry(QRect(24, 25, 320, 20))

        layout_scollarea.addWidget(ip_btn)

        group_port = QWidget(self)
        layout_port = QVBoxLayout()

        sport_btn = QPushButton(self, objectName="TopRounded")

        sport_label = QLabel("Sender Port", sport_btn, objectName="Heading")
        sport_label.setGeometry(QRect(24, 5, 320, 20))

        sport_text = QLabel("9000", sport_btn, objectName="SubAccent")
        sport_text.setGeometry(QRect(24, 25, 320, 20))

        rport_btn = QPushButton(self, objectName="BottomRounded")

        rport_label = QLabel("Receiver Port", rport_btn, objectName="Heading")
        rport_label.setGeometry(QRect(24, 5, 320, 20))

        rport_text = QLabel("9001", rport_btn, objectName="SubAccent")
        rport_text.setGeometry(QRect(24, 25, 320, 20))

        layout_port.addWidget(sport_btn)
        layout_port.addWidget(rport_btn)
        group_port.setLayout(layout_port)

        layout_scollarea.addWidget(group_port)
        scoll_contens.setLayout(layout_scollarea)

        group_general = QWidget(self)
        layout_general = QVBoxLayout()

        date_btn = QPushButton(self, objectName="TopRounded")
        date_label = QLabel("Date and time", date_btn, objectName="Heading")
        date_label.setGeometry(QRect(24, 5, 320, 20))
        date_text = QLabel("Parameters", date_btn, objectName="Sub")
        date_text.setGeometry(QRect(24, 25, 320, 20))

        layout_general.addWidget(date_btn)

        media_btn = QPushButton(self, objectName="BottomRounded")
        media_label = QLabel("Media control", media_btn, objectName="Heading")
        media_label.setGeometry(QRect(24, 5, 320, 20))
        media_text = QLabel("Parameters", media_btn, objectName="Sub")
        media_text.setGeometry(QRect(24, 25, 320, 20))

        layout_general.addWidget(media_btn)
        group_general.setLayout(layout_general)
        layout_scollarea.addWidget(group_general)

        about_btn = QPushButton(self, objectName="Rounded")
        about_label = QLabel("About", about_btn, objectName="Heading")
        about_label.setGeometry(QRect(24, 5, 320, 20))
        about_text = QLabel("Author · Version", about_btn, objectName="Sub")
        about_text.setGeometry(QRect(24, 25, 320, 20))

        layout_scollarea.addWidget(about_btn)
        scroll_area.setWidget(scoll_contens)
        layout_main.addWidget(scroll_area)

        self.setLayout(layout_main)

        # <BUTTON EVENT>
        ip_btn.clicked.connect(lambda: print("Hello"))
        media_btn.clicked.connect(lambda: self._media_btn_event())
        # </BUTTON EVENT>

    def _make_btn_group(self, *args: QPushButton) -> QWidget:
        length = len(args)
        if length > 1:
            group = QWidget(self)
            layout = QVBoxLayout()
            idx = 0
            for arg in args:
                if idx == 0:
                    arg.setObjectName("TopRoundedButton")
                elif idx == length - 1:
                    arg.setObjectName("BottomRoundedButton")
                else:
                    arg.setObjectName("ButtonRect")

                layout.addWidget(arg)

            group.setLayout(layout)
            return group
        elif length == 1:
            return args[0]

        else:
            raise ReferenceError

    def _media_btn_event(self):
        media = WindowMedia()
        media.show()
        media.exec()

    def setup_ui(self):
        self.setWindowTitle("OSC for Watch")
        self.setWindowIcon(QtGui.QPixmap(QPixmap("./assets/icon.png")))
        self.setMinimumSize(370, 500)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)


class WindowMedia(QWidget):
    def __init__(self):
        super(WindowMedia, self).__init__()
        self.setStyleSheet(pss)

        layout = QVBoxLayout()
        scroll_area = QScrollArea(self)

        scroll_contents = QWidget(self)
        layout_contents = QVBoxLayout(self)

        toggle = QPushButton(self, objectName="Rounded")
        toggle_text = QLabel("OFF", toggle, objectName="Heading")
        toggle_text.setGeometry(QRect(0, 0, 300, 40))
        layout_contents.addWidget(toggle)

        scroll_contents.setLayout(layout_contents)
        layout.addWidget(scroll_area)
        scroll_area.setWidget(scroll_contents)
        self.setLayout(layout)

    def setup_ui(self):
        self.setWindowTitle("OSC for Watch")
        self.setWindowIcon(QtGui.QPixmap(QPixmap("./assets/icon.png")))
        # self.setFixedWidth(370)
        self.setStyleSheet(pss)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = WindowMain()
    w.show()
    # asyncio.run(main.start())
    app.exec()
