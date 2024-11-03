import sys, pypresence,pickle,os
from pathlib import Path
from PyQt6.QtWidgets import QApplication,  QWidget, QLabel, QLineEdit, QPushButton,  QVBoxLayout
import PyQt6.QtCore as QtCore
import webbrowser

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


class LoginWindow(QWidget):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle('Custom rich presence')
        layout = QVBoxLayout()
        self.buttonnumber = 0
        self.setLayout(layout)
        layout.setStretch(0, 1)
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
        if not os.path.exists('clientid'):
            self.show()
        else:
            self.clientid.deleteLater()
            self.heading.deleteLater()
            self.subheading.deleteLater()
            self.btn_login.deleteLater()
            self.clientidlabel.deleteLater() 
            self.check_usid()
    def openlink(self):
        webbrowser.open(f'https://discord.com/developers/applications/{self.usid}/rich-presence/assets', new=2)
    def addbutton(self):
        self.buttonnumber += 1
        if self.buttonnumber == 1:
            presencebuttononelabel.setVisible(True)
            presencebuttononetext.setVisible(True)
            presencebuttononelink.setVisible(True)
            buttonremovelabel.setVisible(True)
        elif self.buttonnumber == 2:
            presencebuttontwolabel.setVisible(True)
            presencebuttontwotext.setVisible(True)
            presencebuttontwolink.setVisible(True)
            buttonremovelabel.setVisible(True)

    def removebutton(self):
        self.buttonnumber -= 1
        if self.buttonnumber == 0:
            presencebuttononelabel.setVisible(False)
            presencebuttononetext.setVisible(False)
            presencebuttononelink.setVisible(False)
            buttonremovelabel.setVisible(False)
        elif self.buttonnumber == 1:
            presencebuttontwolabel.setVisible(False)
            presencebuttontwotext.setVisible(False)
            presencebuttontwolink.setVisible(False)
            buttonremovelabel.setVisible(True)
    def check_usid(self):
        try:
            global presence
            if os.path.exists('clientid'):
                with open('clientid', 'rb') as f:
                    self.usid = pickle.load(f)
            else: self.usid = self.clientid.text()
            presence = pypresence.Presence(self.usid)
            self.setWindowTitle('Custom rich presence || Status: stopped')
            presence.connect()
            presence.close()
            with open('clientid', 'wb') as f:
                pickle.dump(self.usid, f)
            
            self.close()

            layout = self.layout()
            layout.setStretch(0, 1)
            global btn_one, btn_two, state, description, img, imgdesc
            presence = pypresence.Presence(self.usid)
            statelabel = QLabel('Description')
            state = QLineEdit()
            desclabel = QLabel('Header')
            description = QLineEdit()
            imglabel = QLabel('Image')
            imglinklabel = QLabel('add it here')
            imglinklabel.setObjectName('Imglink')
            imglinklabel.mousePressEvent = lambda ev: self.openlink()
            imgdesclabel = QLabel('Image description')
            imgdesc = QLineEdit()
            img = QLineEdit()
            imgdesc.setPlaceholderText('Image description') 
            state.setPlaceholderText('Enter description') 
            description.setPlaceholderText('Enter header')
            buttonslabel = QLabel('Add button (they dont show for yourself)')
            
            global presencebuttononelabel, presencebuttononetext, presencebuttononelink
            global presencebuttontwolabel, presencebuttontwotext, presencebuttontwolink, buttonremovelabel
            buttonremovelabel = QLabel('Remove button')
            
            presencebuttononelabel = QLabel('Button one')
            presencebuttononetext = QLineEdit('Text of button')
            presencebuttononelink = QLineEdit('Link for button')
            presencebuttontwolabel = QLabel('Button two')
            presencebuttontwotext = QLineEdit('Text of button')
            presencebuttontwolink = QLineEdit('Link for button')
            presencebuttononelabel.setVisible(False)
            presencebuttononetext.setVisible(False)
            presencebuttononelink.setVisible(False)
            presencebuttontwolabel.setVisible(False)
            presencebuttontwotext.setVisible(False)
            presencebuttontwolink.setVisible(False)
            buttonslabel.mousePressEvent = lambda ev: self.addbutton()
            buttonremovelabel.mousePressEvent = lambda ev: self.removebutton()
            buttonremovelabel.setVisible(False)

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

            layout.addWidget(imglinklabel)
            
            layout.addWidget(img)
            layout.addWidget(imgdesclabel)
            layout.addWidget(imgdesc)


            layout.addWidget(buttonslabel)
            
            layout.addWidget(presencebuttononelabel)
            layout.addWidget(presencebuttononetext)
            layout.addWidget(presencebuttononelink)
            layout.addWidget(presencebuttontwolabel)
            layout.addWidget(presencebuttontwotext)
            layout.addWidget(presencebuttontwolink)
            layout.addWidget(buttonremovelabel)
            layout.addWidget(btn_one)

            layout.addWidget(btn_two)
            
            self.show()
             
        except Exception as e:
            self.btn_login.setText('Invalid ID')
            self.show()
            try: os.remove('clientid')
            except: pass
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
        
        if self.buttonnumber == 1:

            presence.update(state=state.text(), details=description.text(), large_image=img.text(), large_text=imgdesc.text(), buttons=[{'label': presencebuttononetext.text(), 'url': presencebuttononelink.text()}])
        elif self.buttonnumber == 2:
            presence.update(state=state.text(), details=description.text(), large_image=img.text(), large_text=imgdesc.text(), buttons=[{'label': presencebuttononetext.text(), 'url': presencebuttononelink.text()},{'label': presencebuttontwotext.text(), 'url': presencebuttontwolink.text()}])
        else: presence.update(state=state.text(), details=description.text(), large_image=img.text(), large_text=imgdesc.text())
    def change_presence(self):
        if self.buttonnumber == 1:    
            presence.update(state=state.text(), details=description.text(), large_image=img.text(), large_text=imgdesc.text(), buttons=[{'label': presencebuttononetext.text(), 'url': presencebuttononelink.text()}])
        elif self.buttonnumber == 2:
            presence.update(state=state.text(), details=description.text(), large_image=img.text(), large_text=imgdesc.text(), buttons=[{'label': presencebuttononetext.text(), 'url': presencebuttononelink.text()},{'label': presencebuttontwotext.text(), 'url': presencebuttontwolink.text()}])
        else: presence.update(state=state.text(), details=description.text(), large_image=img.text(), large_text=imgdesc.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('start.css').read_text())
    window = LoginWindow()

    sys.exit(app.exec())