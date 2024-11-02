import sys, pypresence,pickle
from pathlib import Path
from PyQt6.QtWidgets import QApplication,  QWidget, QLabel, QLineEdit, QPushButton,  QVBoxLayout
import PyQt6.QtCore as QtCore

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


class LoginWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(300, 200)
        self.setWindowTitle('Custom rich presence')

        self.isValid = False
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.usid = None
        self.heading = QLabel(
            'Welcome.',
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.heading.setObjectName('heading')

        self.subheading = QLabel(
            'Please enter your client id to log in.',
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.subheading.setObjectName('subheading')

        self.clientid = QLineEdit()
        self.clientid.setPlaceholderText('Enter your client id')

        self.btn_login = QPushButton('Login')
        self.clientidlabel = QLabel('Client id:') 
        self.btn_login.clicked.connect(self.check_usid)
        
        layout.addWidget(self.heading)
        layout.addWidget(self.subheading)
        layout.addWidget(self.clientidlabel)
        layout.addWidget(self.clientid)
        layout.addWidget(self.btn_login)
        
        self.show()

    def check_usid(self):
        try:
            global presence
            self.usid = self.clientid.text()
            presence = pypresence.Presence(self.usid)
            self.setWindowTitle('Custom rich presence || Status: stopped')
            presence.connect()
            QtCore.QCoreApplication.processEvents()
            self.btn_login.setText('Connecting...')
            presence.close()
            self.isValid = True
            with open('clientid', 'wb') as f:
                pickle.dump(self.clientid.text(), f)
            self.usid = self.clientid.text()
            self.btn_login.setText('Success!')
            
            self.close()
            self.setFixedSize(300, 400)
            layout = self.layout()
            self.clientid.deleteLater()
            self.heading.deleteLater()
            self.subheading.deleteLater()
            self.btn_login.deleteLater()
            self.clientidlabel.deleteLater()
            global btn_one, btn_two, state, description, img
            presence = pypresence.Presence(self.usid)
            statelabel = QLabel('Description')
            state = QLineEdit()
            desclabel = QLabel('Header')
            description = QLineEdit()
            imglabel = QLabel('Image')
            img = QLineEdit()
            state.setPlaceholderText('Enter description') 
            description.setPlaceholderText('Enter header')
            btn_one = QPushButton('Start presence!')
            btn_one.clicked.connect(self.start_presence)
            btn_two = QPushButton('Change presence')
            btn_two.clicked.connect(self.change_presence)
            btn_two.setVisible(False)
            layout.addWidget(statelabel)
            layout.addWidget(state)
            layout.addWidget(desclabel)
            layout.addWidget(description)
            layout.addWidget(imglabel)
            layout.addWidget(img)
            layout.addWidget(btn_one)
            layout.addWidget(btn_two)
            self.show()
             
        except pypresence.exceptions.InvalidID:
            self.btn_login.setText('Invalid ID')
    def stop_presence(self):
        
        btn_one.setText('Start presence!')
        btn_one.clicked.connect(self.start_presence) 
        btn_two.setVisible(False)
        QtCore.QCoreApplication.processEvents()
        presence.close()

    def start_presence(self):
        btn_one.setText('Stop presence!')
        btn_one.clicked.connect(self.stop_presence)
        btn_two.setVisible(True)
        QtCore.QCoreApplication.processEvents()
        presence.connect()
        presence.update(state=state.text(), details=description.text(), large_image=img.text())
        
    def change_presence(self):
        presence.update(state=state.text(), details=description.text(),large_image=img.text())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('start.css').read_text())
    window = LoginWindow()

    sys.exit(app.exec())