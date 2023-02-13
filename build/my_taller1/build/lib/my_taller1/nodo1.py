
# ROS Client Library for Python
import rclpy
 
# Handles the creation of nodes
from rclpy.node import Node
 
# Handles string messages

from geometry_msgs.msg import Twist


import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import threading

import pygame




class Movement(Node):

  def __init__(self):
 
    # Initiate the Node class's constructor and give it a name
    super().__init__('movement_subscriber')
 
    # The node subscribes to messages of type std_msgs/String, 
    # over a topic named: /addison
    # The callback function is called as soon as a message is received.
    # The maximum number of queued messages is 10.
    self.subscription = self.create_subscription(Twist,'/turtlebot_position',self.listener_callback,10)
    self.subscription  # prevent unused variable warning

    self.global_x_cordinates = []
    self.global_y_cordinates = []
    
    pygame.init()
    self.Dimensiones=(500,500)
    self.Pantalla = pygame.display.set_mode(self.Dimensiones)
    pygame.display.set_caption("Trayectoria del robot ")
    
    self.reloj = pygame.time.Clock()
    self.Pantalla.fill((0,0,0))


    self.x_pos_actual=0
    self.y_pos_actual=0

    self.x_pos_anterior=0
    self.y_pos_anterior=0



  
    
    
    """
    self.figure=plt.figure()   
    self.ax=self.figure.add_subplot(1,1,1)


    self.h1,=plt.plot(self.global_x_cordinates,self.global_y_cordinates)
    plt.xlim(-20,20)
    plt.ylim(-20,20)
    

    dataCollector = threading.Thread(target =self.animate(self.h1,self.figure,self.global_x_cordinates,self.global_y_cordinates))
    dataCollector.start()
    """
    
    
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




  def listener_callback(self, msg):
    # Display a message on the console every time a message is received on the
    # addison topic

    for Evento in pygame.event.get():
      if Evento.type == pygame.QUIT:
          pygame.quit()

    
    x,y,z=msg.linear.x,msg.linear.y,msg.linear.z #Descompresiòn de coordenadas

    print("x: ",x)
    print("y: ",y)
    print("z: ",z)

    self.global_x_cordinates.append(x)
    self.global_y_cordinates.append(y)

    

    self.x_pos_actual=x
    self.y_pos_actual=y

    actuales= self.update_pixels(self.x_pos_actual,self.y_pos_actual)
    anteriores= self.update_pixels(self.x_pos_anterior,self.y_pos_anterior)
    

    print("actuales: ",actuales)
    print("anteriores: ",anteriores)
    
  

    pygame.draw.line(self.Pantalla, (255, 0, 0), [anteriores[0], anteriores[1]], [actuales[0], actuales[1]], 5)
    
    pygame.display.update()

    self.reloj.tick(20)  # Limitamos a 20 fotogramas por segundo  

    self.x_pos_anterior=x
    self.y_pos_anterior=y

  

   


  


  
"""
  def animate(num,h1,figure,x,y):

    ani=FuncAnimation(figure,update_line,fargs=(h1,x,y),interval=50,blit=False)
    plt.show()


def update_line(num,hl,x,y):

    hl.set_data(x, y)
    return hl,
"""

  
 
def main(args=None):
 
  # Initialize the rclpy library
  rclpy.init(args=args)
 
  # Create a subscriber
  movement_subscriber = Movement()
  

  # Spin the node so the callback function is called.c
  # Pull messages from any topics this node is subscribed to.
  rclpy.spin(movement_subscriber)
  #plt.show()
 
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  pygame.quit()
  movement_subscriber.destroy_node()
   
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
 
if __name__ == '__main__':
  main()


