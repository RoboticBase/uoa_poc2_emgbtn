# -*- coding: utf-8 -*-
import time

import rospy
import RPi.GPIO as GPIO

from uoa_poc2_emgbtn.logging import getLogger
logger = getLogger(__name__)


class EmergencyButton(object):
    def __init__(self):
        params = rospy.get_param('~')
        self.btn_pin = int(params['gpio']['btn_pin'])
        self._setup_gpio()
        rospy.on_shutdown(self._cleanup_gpio)

    def start(self):
        logger.infof('EmergencyButton start')
        rospy.spin()
        logger.infof('EmergencyButton stop')

    def _setup_gpio(self):
        logger.infof('setup GPIO, btn_pin={}'.format(self.btn_pin))
        #GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.btn_pin, GPIO.IN)
        GPIO.add_event_detect(self.btn_pin, GPIO.FALLING, callback=self._detect_event, bouncetime=100)

    def _cleanup_gpio(self):
        logger.infof('cleanup GPIO')
        GPIO.remove_event_detect(self.btn_pin)
        GPIO.cleanup()

    def _detect_event(self, pin):
        time.sleep(0.1)
        if GPIO.input(pin) == GPIO.HIGH:
            logger.infof('button pressed')
