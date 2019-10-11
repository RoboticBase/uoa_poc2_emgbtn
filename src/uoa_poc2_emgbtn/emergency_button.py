# -*- coding: utf-8 -*-
import rospy

from uoa_poc2_emgbtn.logging import getLogger
logger = getLogger(__name__)


class EmergencyButton(object):
    def __init__(self):
        logger.infof('init')

    def start(self):
        logger.infof('EmergencyButton start')
        rospy.spin()
        logger.infof('EmergencyButton stop')

