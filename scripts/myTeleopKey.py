import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportRelative
from turtlesim.srv import TeleportAbsolute

import termios, sys, os, tty
from numpy import pi

# Definir la velocidad de la tortuga
vel = 2

# Definir la posición y orientación central de la tortuga
posicion_central = (5.5, 5.5, 0)
orientacion_central = 0

# Función para mover la tortuga hacia adelante
def mover_adelante():
    msg = Twist()
    msg.linear.x = vel
    msg.angular.z = 0
    pub.publish(msg)

# Función para mover la tortuga hacia atrás
def mover_atras():
    msg = Twist()
    msg.linear.x = -vel
    msg.angular.z = 0
    pub.publish(msg)

# Función para girar la tortuga en sentido horario
def girar_horario():
    msg = Twist()
    msg.linear.x = 0
    msg.angular.z = -vel
    pub.publish(msg)

# Función para girar la tortuga en sentido antihorario
def girar_antihorario():
    msg = Twist()
    msg.linear.x = 0
    msg.angular.z = vel
    pub.publish(msg)

# Función para volver a la posición y orientación central de la tortuga
def volver_centro():
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleport_absolute = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        teleport_absolute(posicion_central[0], posicion_central[1], orientacion_central)
    except rospy.ServiceException as e:
        print("Service call failed: ", e)

# Función para girar la tortuga 180 grados
def girar_180():
    print("dentro de nuevo  ")
    msg = Twist()
    msg.linear.x = 0
    msg.angular.z = pi
    pub.publish(msg)
    #rospy.wait_for_service('/turtle1/teleport_relative')
    #try:
    #    teleport_relative = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
    #    teleport_relative(0, 0, pi)
    #except rospy.ServiceException as e:
    #    print("Service call failed: ", e)

# Configuración de la tecla de salida del programa
def setup_terminal():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    return old_settings

# Restauración de la configuración original del terminal
def restore_terminal(old_settings):
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == '__main__':
    # Inicializar el nodo ROS
    rospy.init_node('teclado_tortuga')

    # Crear un objeto publicador para enviar comandos de movimiento a la tortuga
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    # Configurar el terminal para recibir las teclas presionadas
    old_settings = setup_terminal()

    try:
        while not rospy.is_shutdown():
            key = ord(sys.stdin.read(1))
            print(key)
            # Mover hacia adelante con la tecla 'w'
            if key == 119:
                mover_adelante()
            # Mover hacia atrás con la tecla 's'
            elif key == 115:
                mover_atras()
            # Girar en sentido horario con la tecla 'd'
            elif key == 100:
                girar_horario()
            # Girar en sentido antihorario con la tecla 'a'
            elif key == 97:
                girar_antihorario()
            # Girar 180°
            elif key == 114:
                girar_180()
            elif key == 32:
                volver_centro()
    except: 
        print("Error")
