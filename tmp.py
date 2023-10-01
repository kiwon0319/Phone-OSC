from PySide6.QtCore import Qt
from PySide6.QtCore import QRect
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6 import QtGui
import sys

btn_top_round = """
QWidget{
    background-color: "#202020";
    border-top-right-radius: 25;
    border-top-left-radius: 25;
    color: White;
    text-align: left;
    padding-left: 25;
    padding-right: 25;
    padding-top: 5;
}

QWidget:hover:!pressed{
    background-color : "#252525"
}

QWidget:pressed{
    background-color : "#303030"
}
"""

btn_bottom_round = """
QWidget{
    background-color: "#202020";
    border-bottom-right-radius: 25;
    border-bottom-left-radius:25;
    color: White;
    text-align:left top;
    padding-left:25;
    padding-right:25;
    padding-top: 5;
}

QWidget:hover:!pressed{
    background-color : "#252525"
}

QPushButton:pressed{
    background-color : "#303030"
}
"""

btn_round = """
QWidget{
    background-color: "#202020";
    border-radius: 25;
    color: White;
    text-align:left;
    padding-left:25;
    padding-right:25;
    padding-top: 5;
}

QWidget:hover{
    background-color : "#252525"
}

QWidget:pressed{
    background-color : "#303030"
}
"""

label_primary = """
    color: #3e91ff;
    align: left;
    font: 12px;
    background-color: rgba(0, 0, 0, 0)
"""

label_sub = """
    color: #4d4d4d;
    align: left;
    font: 12px;
    background-color: rgba(0, 0, 0, 0)
"""

label_heading = """
    color: white;
    align: left;
    font: 18px;
    background-color: rgba(0, 0, 0, 0)
"""


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

        title = QLabel("OSC for Watch", self)
        title.setStyleSheet("color: white; font: 18px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        currunt = QLabel("YYYY-MM-DD, HH : MM", self)
        currunt.setStyleSheet("color:white; font: 12px")
        currunt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_ex_appbar.addWidget(widget)
        layout_ex_appbar.addWidget(title)
        layout_ex_appbar.addWidget(currunt)

        group_ex_appbar.setLayout(layout_ex_appbar)
        layout_scollarea.addWidget(group_ex_appbar)

        ip_btn = QPushButton(self)
        ip_btn.setStyleSheet(btn_round)

        ip_label = QLabel("IP", ip_btn)
        ip_label.setGeometry(QRect(0, 0, 320, 20))
        ip_label.setStyleSheet(label_heading)

        ip_text = QLabel("127.0.0.1", ip_btn)
        ip_text.setGeometry(QRect(0, 20, 320, 20))
        ip_text.setStyleSheet(label_primary)

        layout_scollarea.addWidget(ip_btn)

        group_port = QWidget(self)
        layout_port = QVBoxLayout()

        sport_btn = QPushButton(self)
        sport_btn.setStyleSheet(btn_top_round)

        sport_label = QLabel("Sender Port", sport_btn)
        sport_label.setGeometry(QRect(0, 0, 320, 20))
        sport_label.setStyleSheet(label_heading)

        sport_text = QLabel("9000", sport_btn)
        sport_text.setGeometry(QRect(0, 20, 320, 20))
        sport_text.setStyleSheet(label_primary)

        rport_btn = QPushButton(self)
        rport_btn.setStyleSheet(btn_bottom_round)

        rport_label = QLabel("Reciver Port", rport_btn)
        rport_label.setGeometry(QRect(0, 0, 320, 20))
        rport_label.setStyleSheet(label_heading)

        rport_text = QLabel("9001", rport_btn)
        rport_text.setGeometry(QRect(0, 20, 320, 20))
        rport_text.setStyleSheet(label_primary)

        layout_port.addWidget(sport_btn)
        layout_port.addWidget(rport_btn)
        group_port.setLayout(layout_port)

        layout_scollarea.addWidget(group_port)
        scoll_contens.setLayout(layout_scollarea)

        group_general = QWidget(self)
        layout_general = QVBoxLayout()

        date_btn = QPushButton(self)
        date_btn.setStyleSheet(btn_top_round)

        date_label = QLabel("Date and time", date_btn)
        date_label.setGeometry(QRect(0, 0, 320, 20))
        date_label.setStyleSheet(label_heading)

        date_text = QLabel("Parameters", date_btn)
        date_text.setGeometry(QRect(0, 20, 320, 20))
        date_text.setStyleSheet(label_sub)

        layout_general.addWidget(date_btn)

        media_btn = QPushButton(self)
        media_btn.setStyleSheet(btn_bottom_round)

        media_label = QLabel("Media control", media_btn)
        media_label.setGeometry(QRect(0, 0, 320, 20))
        media_label.setStyleSheet(label_heading)

        media_text = QLabel("Parameters", media_btn)
        media_text.setGeometry(QRect(0, 20, 320, 20))
        media_text.setStyleSheet(label_sub)

        layout_general.addWidget(media_btn)
        group_general.setLayout(layout_general)
        layout_scollarea.addWidget(group_general)

        about_btn = QPushButton(self)
        about_btn.setStyleSheet(btn_round)

        about_label = QLabel("About", about_btn)
        about_label.setGeometry(QRect(0, 0, 320, 20))
        about_label.setStyleSheet(label_heading)

        about_text = QLabel("Author · Version", about_btn)
        about_text.setGeometry(QRect(0, 20, 320, 20))
        about_text.setStyleSheet(label_sub)

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
        self.setStyleSheet("background-color:#000000")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)


class WindowMedia(QWidget):
    def __init__(self):
        super(WindowMedia, self).__init__()
        self.setStyleSheet("background-color: #000000")

        layout = QVBoxLayout()
        scroll_area = QScrollArea(self)

        scroll_contents = QWidget(self)
        layout_contents = QVBoxLayout(self)

        toggle = QPushButton(self)
        toggle.setStyleSheet(btn_round)
        toggle_text = QLabel("OFF", toggle)
        toggle_text.setGeometry(QRect(0, 0, 300, 40))
        toggle_text.setStyleSheet(label_heading)
        layout_contents.addWidget(toggle)

        scroll_contents.setLayout(layout_contents)
        layout.addWidget(scroll_area)
        scroll_area.setWidget(scroll_contents)
        self.setLayout(layout)

    def setup_ui(self):
        self.setWindowTitle("OSC for Watch")
        self.setWindowIcon(QtGui.QPixmap(QPixmap("./assets/icon.png")))
        # self.setFixedWidth(370)
        self.setStyleSheet("background-color:#000000")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = WindowMain()
    w.show()
    # asyncio.run(main.start())
    app.exec()
