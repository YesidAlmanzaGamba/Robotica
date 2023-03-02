import rclpy
from example_interfaces.srv import AddTwoInts

class MyServiceNode:
    def __init__(self):
        self.node = rclpy.create_node('my_service_node')
        self.srv = self.node.create_service(
            AddTwoInts, 'string_length', self.string_length_callback)

    def string_length_callback(self, request, response):
        response.sum = len(request.a)
        self.node.get_logger().info(
            f"Received request with string {request.a} and returning length {response.sum}")
        return response

def main(args=None):
    rclpy.init(args=args)
    my_service_node = MyServiceNode()
    rclpy.spin(my_service_node.node)
    my_service_node.node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
