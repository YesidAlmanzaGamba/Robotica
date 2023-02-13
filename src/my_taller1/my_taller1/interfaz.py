import sys

from PyQt5.QtWidgets import QApplication, QMainWindow,QPushButton
from PyQt5 import uic
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from PyQt5 import QtCore, QtWidgets
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QPlainTextEdit, QHBoxLayout, QVBoxLayout


import threading

class EmbTerminal(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminal, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)
        # Works also with urxvt:
        self.process.start('urxvt',['-embed', str(int(self.winId()))])
        self.setFixedSize(640, 480)


class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        uic.loadUi('src/my_taller1/my_taller1/MainWindow .ui', self)

        


        
        self.button_run.clicked.connect(self.runCommand)
        self.button_clear.clicked.connect(self.editorOutput.clear)
        self.run_colconBuild.clicked.connect(self.colconbuild) 
        self.button_local_setup.clicked.connect(self.local_setup) 
        self.nodo_Position.clicked.connect(self.nodoPosition)
        self.teleoperation_button.clicked.connect(self.nodoTeleoperation)

        self.editorCommand.insertPlainText('dir')

        self.local_setup
        self.ros2_commands=QThread()
        self.ros2_thread_position=threading.Thread(target=self.nodoPosition).start()
        self.ros2_thread_teleoperation=threading.Thread(target=self.nodoTeleoperation)
        

        self.show()

    def start_thread(self, thread_name:str):
        if thread_name=="ros2_commands":
            self.ros2_commands.start()
        elif thread_name=="ros2_thread_position":
            self.ros2_thread_position.start()

    def end_thread(self, thread_name:str):
        if thread_name=="ros2_commands":
            self.ros2_commands.quit()
        elif thread_name=="ros2_thread_position":
            self.ros2_thread_position.quit()


    
    def colconbuild(self):
        self.start_thread("ros2_commands")
        self.runRos2Command("colcon build")
        self.end_thread("ros2_comands")


    def local_setup(self):
        self.start_thread("ros2_commands")
        self.runRos2Command(". install/local_setup.sh")
        self.end_thread("ros2_comands")

    def nodoPosition(self):
        #self.start_thread("ros2_thread_position")
        self.runRos2Command("ros2 run my_taller1 nodo1")

    def nodoTeleoperation(self):
        try:
            self.runRos2Command("ros2 run my_taller1 keyboard_teleop_hold") 
        except:
            self.editorOutput.insertPlainText("Error ejecutando comando")
            

        

        
         



    def runCommand(self):
        
        command_line = self.editorCommand.toPlainText().strip()
        p = os.popen(command_line)
        try:
            if p:
                self.editorOutput.clear()
                output = p.read()
                self.editorOutput.insertPlainText(output)
        except:
            self.editorOutput.insertPlainText("Error ejecutando comando")


    def runRos2Command(self,ros2_message:str):

        
        #self.ros2_commands.start()
        command_line=""

        if ros2_message!=None:
            command_line = ros2_message
        
            self.editorCommand.clear()
            self.editorCommand.insertPlainText(command_line)
            
            p = os.popen(command_line)
            try:
                if p:
                    self.editorOutput.clear()
                    output = p.read()
                    self.editorOutput.insertPlainText(output)
            except:
                self.editorOutput.insertPlainText("Error ejecutando comando")
                #self.ros2_commands.quit()

            #self.ros2_commands.quit()
def main():
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()