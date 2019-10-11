# -*- coding: utf-8 -*-
import datetime
import time

import rospy
import RPi.GPIO as GPIO
import pytz

from uoa_poc2_msgs.msg import r_emergency_command, r_emergency_result

from uoa_poc2_emgbtn.logging import getLogger
logger = getLogger(__name__)


class EmergencyButton(object):
    def __init__(self):
        self._setup_params()
        self._setup_rostopic()
        self._setup_gpio()
        rospy.on_shutdown(self._cleanup_gpio)

    def start(self):
        logger.infof('EmergencyButton start')
        rospy.spin()
        logger.infof('EmergencyButton stop')

    def _setup_params(self):
        params = rospy.get_param('~')
        self.entity_type = params['roboticbase']['entity_type']
        self.entity_id = params['roboticbase']['entity_id']
        self.emg_name = params['roboticbase']['emg_name']
        self.pub_topic = params['ros']['topic']['emg']
        self.sub_topic = params['ros']['topic']['emgexe']
        self.btn_pin = int(params['gpio']['btn_pin'])
        self.tz = pytz.timezone(params['common']['timezone'])

    def _setup_rostopic(self):
        logger.infof('setup rostopic')
        self._emg_pub = rospy.Publisher(self.pub_topic, r_emergency_command, queue_size=1)
        rospy.Subscriber(self.sub_topic, r_emergency_result, self.subscribe_emgexe, queue_size=1)

    def _setup_gpio(self):
        logger.infof('setup GPIO, btn_pin={}', self.btn_pin)
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
            self.publish_emg()

    def publish_emg(self):
        emg_cmd = r_emergency_command()
        emg_cmd.id = self.entity_id
        emg_cmd.type = self.entity_type
        emg_cmd.time = datetime.datetime.now(self.tz).isoformat()
        emg_cmd.emergency_cmd = self.emg_name

        self._emg_pub.publish(emg_cmd)
        logger.infof("published emergency, cmd='{}'", str(emg_cmd).replace('\n', ', '))

    def subscribe_emgexe(self, result):
        logger.infof("notified emergency result='{}'", str(result).replace('\n', ', '))
