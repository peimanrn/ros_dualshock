import rospy
import pygame
import os
from std_msgs.msg import *
from geometry_msgs.msg import Twist


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
    @staticmethod
    def talker(direct):
        rospy.init_node('dualshockPublisher', anonymous=False)
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
        vel_msg = Twist()
        # rate = rospy.Rate(10)
        
        # while not rospy.is_shutdown():
        if direct == 'up' :
            print('up')
            vel_msg.linear.x = 2
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            velocity_publisher.publish(vel_msg)
        elif direct == 'down' : 
            print('down')
            vel_msg.linear.x = -2
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            velocity_publisher.publish(vel_msg)            
        elif direct == 'left' :
            print('left')
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 2
            vel_msg.angular.y = 2
            vel_msg.angular.z = 2
            velocity_publisher.publish(vel_msg)            
        elif direct == 'right' :
            print('right')
            vel_msg.linear.x = 5
            vel_msg.linear.y = 10
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = -10
            velocity_publisher.publish(vel_msg)
        elif direct == 'stop' :
            print('stop')
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            velocity_publisher.publish(vel_msg)
        # rate.sleep()
           
    @staticmethod
    def talker2(direc,speed):
        rospy.init_node('dualshockPublisher', anonymous=False)
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1)
        vel_msg = Twist()
        # rate = rospy.Rate(10)
        
        # while not rospy.is_shutdown():
        if direc != 0 and speed != 0 :
            print('horiz:',direc,'verti',speed)
            vel_msg.linear.x = -10*speed
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = -10*direc
            velocity_publisher.publish(vel_msg)
        elif direc == 0 and speed == 0 :
            print('stop')
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            velocity_publisher.publish(vel_msg)
        # rate.sleep()
           
        
    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[str(event.axis)] = round(event.value,2)
                    self.talker2(self.axis_data.get('0',0.0),self.axis_data.get('1',0.0))
                    # if event.axis == 0 :
                    #     zero_val = round(event.value,2)
                    # elif event.axis == 1 :
                    #     one_val = round(event.value,2)
                    # print('zero value is : ',zero_val,'one value is : ',one_val)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                    # if event.button == 0 :
                    #     self.talker('down')
                    # elif event.button == 1 : 
                    #     self.talker('right')
                    # elif event.button == 2 :
                    #     self.talker('up')
                    # elif event.button == 3:
                    #     self.talker('left')
                elif event.type == pygame.JOYBUTTONUP:
                    self.talker('stop')
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
                
                # os.system('clear')
                # pprint.pprint(self.button_data)
                # pprint.pprint(self.axis_data)
                # pprint.pprint(self.hat_data)
                # print(self.axis_data.get('0',888))
                # zero_val = self.axis_data.get('0')
                # one_val = self.axis_data.get('0')
                # print('zero is : ',zero_val,' one is : ',one_val)
                

if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
    # try:
    ps4.talker()
    # except rospy.ROSInterruptException:
        # pass
