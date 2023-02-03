
import rclpy
from geometry_msgs.msg import Twist

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('movement_publisher')
    publisher = node.create_publisher(Twist, '/turtlebot_cmdVel')
    msg = Twist()

    i = 0
    while True:
        msg.linear.x = i
        node.get_logger().info('Publicando: "{0}"'.format(msg.linear.x))
        publisher.publish(msg)
        i += 1
        rclpy.spin_once(node)

if __name__ == '__main__':
    main()