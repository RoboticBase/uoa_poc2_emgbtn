#!/usr/bin/python
# -*- coding: utf-8 -*-
import rospy

from uoa_poc2_emgbtn.emergency_button import EmergencyButton


def main():
    try:
        rospy.init_node('emgbtn')
        EmergencyButton().start()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()
