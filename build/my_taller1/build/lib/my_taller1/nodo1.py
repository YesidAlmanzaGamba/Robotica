
# ROS Client Library for Python
import rclpy
 
# Handles the creation of nodes
from rclpy.node import Node
 
# Handles string messages

from geometry_msgs.msg import Twist


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re
import threading







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

    self.figure=plt.figure()   
    self.ax=self.figure.add_subplot(1,1,1)

    self.h1,=plt.plot(self.global_x_cordinates,self.global_y_cordinates)
    plt.xlim(-20,20)
    plt.ylim(-20,20)
    

    dataCollector = threading.Thread(target =self.animate(self.h1,self.figure,self.global_x_cordinates,self.global_y_cordinates))
    dataCollector.start()
    plt.show()
    
    


  def listener_callback(self, msg):
    # Display a message on the console every time a message is received on the
    # addison topic

    
    x,y,z=msg.linear.x,msg.linear.y,msg.linear.z #Descompresiòn de coordenadas

    print("x: ",x)
    print("y: ",y)
    print("z: ",z)

    self.global_x_cordinates.append(x)
    self.global_y_cordinates.append(y)

  
    

    """

 
    """



  
 
  def animate(num,h1,figure,x,y):

    ani=FuncAnimation(figure,update_line,fargs=(h1,x,y),interval=50,blit=False)


def update_line(num,hl,x,y):

    hl.set_data(x, y)
    return hl,


  
 
def main(args=None):
 
  # Initialize the rclpy library
  rclpy.init(args=args)
 
  # Create a subscriber
  movement_subscriber = Movement()
  

  # Spin the node so the callback function is called.c
  # Pull messages from any topics this node is subscribed to.
  rclpy.spin(movement_subscriber)
  plt.show()
 
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  movement_subscriber.destroy_node()
   
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
 
if __name__ == '__main__':
  main()


