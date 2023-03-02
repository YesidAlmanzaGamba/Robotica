#!/usr/bin/env python3
import rclpy
from interface_t1.srv import MiServicio


def mi_servicio_callback(request, response):
    response.salida = "Respuesta a " + request.entrada
    print("Recibido: ", request.entrada)
    print("Enviado: ", response.salida)
    return response


def main(args=None):
    rclpy.init(args=args)

    node = rclpy.create_node('mi_servicio')

    servicio = node.create_service(MiServicio, 'mi_servicio', mi_servicio_callback)

    print("Servicio listo.")

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Servicio detenido.")

    node.destroy_service(servicio)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

