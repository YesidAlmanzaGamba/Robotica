import sys
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QWidget,QMainWindow, QFileDialog
import rclpy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import pygame
from PyQt5.uic import loadUi
import os
import matplotlib.pyplot as plt
import json
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

class RosNodeThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.node = rclpy.create_node('pyqt_ros_node')
        self.subscriber = self.node.create_subscription(Twist,'/turtlebot_position',self.callback,10)

        self.global_x_cordinates = []
        self.global_y_cordinates = []

        self.x_pos_actual=0
        self.y_pos_actual=0

        self.x_pos_anterior=0
        self.y_pos_anterior=0
        self.text=""



        pygame.init()
        self.Dimensiones=(500,500)
        self.Pantalla = pygame.display.set_mode(self.Dimensiones)
        self.Pantalla.fill((0,0,0))
        pygame.display.set_caption("Trayectoria del robot ")
            
        self.reloj = pygame.time.Clock()


    def update_pixels(self,x,y):
        
        dim_x=self.Dimensiones[0]
        dim_y=self.Dimensiones[1]

        pix_y= self.rect_ecuacion(-2.55,2.55,dim_y,0,y)
        pix_x= self.rect_ecuacion(-2.55,2.55,0,dim_x,x)

        return pix_x,pix_y


    def rect_ecuacion(self,x1,x2,y1,y2,x):

        m=(y2-y1)/(x2-x1)
        y=m*(x-x1)+y1

        return int(y)
   

    def callback(self, msg):
        


        x,y,z=msg.linear.x,msg.linear.y,msg.linear.z #Descompresiòn de coordenadas

        self.text = str(x)+" "+str(y)+" "+str(z)

        if x not in self.global_x_cordinates:
            self.global_x_cordinates.append(float(x))

        if y not in self.global_y_cordinates:
            self.global_y_cordinates.append(float(y))

        

        self.x_pos_actual=x
        self.y_pos_actual=y

        actuales= self.update_pixels(self.x_pos_actual,self.y_pos_actual)
        anteriores= self.update_pixels(self.x_pos_anterior,self.y_pos_anterior)
        
        for Evento in pygame.event.get():
            if Evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.draw.line(self.Pantalla, (255, 0, 0), [anteriores[0], anteriores[1]], [actuales[0], actuales[1]], 5)
        
        pygame.display.update()

        self.reloj.tick(20)  # Limitamos a 20 fotogramas por segundo  

        self.x_pos_anterior=x
        self.y_pos_anterior=y

    
    def run(self):
        rclpy.spin(self.node)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('src/my_taller1/my_taller1/MainWindow.ui', self)
       
        self.start_position()
        self.timer = self.startTimer(100)
        self.global_x_cordinates = []
        self.global_y_cordinates = []

        self.button_run.clicked.connect(self.runCommand)
        self.button_clear.clicked.connect(self.editorOutput.clear)
        self.button_clear.clicked.connect(self.editorCommand.clear)

        self.run_colconBuild.clicked.connect(self.colconbuild) 
        self.button_local_setup.clicked.connect(self.local_setup) 

        self.nodo_Position.clicked.connect(self.start_position)
        self.button_capture.clicked.connect(self.capture_position)

        self.button_capture_coordinates.clicked.connect(self.capture_cordinates)

    
    def start_position(self):
        self.thread = RosNodeThread()
        self.thread.start()        

    def capture_position(self):

        x=self.global_x_cordinates
        y=self.global_y_cordinates

        if len(x)!=len(y):
            tam=0
            if len(x)>len(y):
                tam=len(y)-1
            else:
                tam=len(x)-1

            x=x[:tam]
            y=y[:tam]

        fig, ax = plt.subplots()
        # Dibujar puntos
        ax.plot(x,y)
        plt.xlim(-5,6)
        plt.ylim(-5,6)
        # Guardar el gráfico en formato png
        #plt.savefig('diagrama-dispersion.png')
        # Mostrar el gráfico
        plt.show()

    def capture_cordinates(self):
        print("Capture Coordinates")

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Seleccionar archivo JSON", "","JSON Files (*.json)", options=options)
        
        if file_name:
            current_dir = os.getcwd()
            relative_path = os.path.relpath(file_name, current_dir)

            print(relative_path)
            print(file_name)
        

            with open(relative_path, "w") as archivo:

                d = {"coordinates_x":self.global_x_cordinates, "coordinates_y": self.global_y_cordinates}
                json.dump(d, archivo, indent=2)


    
    def timerEvent(self, event):
        if hasattr(self.thread, 'text'):
            texto=str(self.thread.text).split()

            self.global_x_cordinates=list(self.thread.global_x_cordinates)
            self.global_y_cordinates=list(self.thread.global_y_cordinates)

            self.pos_x_3.setText(texto[0])
            self.pos_y_3.setText(texto[1])
            self.pos_z_3.setText(texto[2])

            #print(self.x_pos_anterior)
            #print(self.y_pos_anterior)

    def closeEvent(self, event):
        self.thread.node.destroy_node()
        rclpy.shutdown()

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

    def colconbuild(self):
        #self.start_thread("ros2_commands")
        self.runRos2Command("colcon build")
        #self.end_thread("ros2_comands")


    def local_setup(self):
        #self.start_thread("ros2_commands")
        self.runRos2Command(". install/local_setup.sh")
        #self.end_thread("ros2_comands")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.label_w.setStyleSheet("background-color:rgb(86,250,29)")

        elif event.key() == Qt.Key_A:
            self.label_a.setStyleSheet("background-color:rgb(86,250,29)")
        elif event.key() == Qt.Key_S:
            self.label_s.setStyleSheet("background-color:rgb(86,250,29)")
        elif event.key() == Qt.Key_D:
            self.label_d.setStyleSheet("background-color:rgb(86,250,29)")
        else:
            self.red()
          

    def red(self):
        self.label_d.setStyleSheet("background-color: rgb(165, 29, 45);color:rgb(255, 255, 255);font: 75 15pt Ubuntu;border-style:solid;border-radius:15px;")
        self.label_a.setStyleSheet("background-color: rgb(165, 29, 45);color:rgb(255, 255, 255);font: 75 15pt Ubuntu;border-style:solid;border-radius:15px;")
        self.label_s.setStyleSheet("background-color: rgb(165, 29, 45);color:rgb(255, 255, 255);font: 75 15pt Ubuntu;border-style:solid;border-radius:15px;")
        self.label_w.setStyleSheet("background-color: rgb(165, 29, 45);color:rgb(255, 255, 255);font: 75 15pt Ubuntu;border-style:solid;border-radius:15px;")


def main(args=None):
    rclpy.init(args=sys.argv)
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
  main()