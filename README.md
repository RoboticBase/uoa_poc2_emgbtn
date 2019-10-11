# uoa_poc2_emgbtn
This ROS project detects the GPIO input and send an emergency message to a ROS topic

## requirements
* [uoa_poc2_msgs](https://github.com/RoboticBase/uoa_poc2_msgs)
* RPi.GPIO (WiringPi)
* pytz

### install dependency
```
rosdep install --from-paths src --ignore-src -r -y
```

## environment variables

|environment variable|description|
|:--|:--|
|ENTITY\_TYPE|Type of RoboticBase's Entity|
|ENTITY\_ID|ID of RoboticBase's Entity|

## launch
```
$ roslaunch uoa_poc2_emgbtn uoa_poc2_emgbtn.launch
```
