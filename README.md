# Lynxmotion PETE

Known for their **high-quality** components and ease of use, [Lynxmotion](https://www.lynxmotion.com/) caters to both educational and hobbyist markets. Their products are designed for versatility, allowing for numerous configurations and expansions, making them a favorite in STEM education and robotics competitions. Their lineup includes robotic arms, walking robots, rovers and more, all built with the versatile Servo Erector Set (SES) system.

The **Lynxmotion SES-V1 humanoid robot [PETE](https://www.lynxmotion.com/driver.aspx?Topic=assem02#pete)** is part of the Lynxmotion large robots lineup. PETE is a 20 DoF RC servo based biped walker with gripper hands: 14x Hitec HS-645 high-torque servos for the feet, ankles, knees, hips, waist and 2 DoF shoulder, alongside 6x Hitec HS-422 servos for the wrists, grippers, neck, head and elbows.

![robot image](https://eu.robotshop.com/cdn/shop/files/lynxmotion-pete-humanoid-development-platform-no-electronics-1.webp?v=1720508194&width=300)

The robot is made from black anodized aluminium servo brackets and ultra-tough laser-cut Lexan structural components. Since the kit is based on the SES, the parts can be easily used (in conjunction with a few other parts sold separately) to make a variety of other robots such as quadrupeds, hexapods, robot arms and more.

##### First steps

The first steps for this project are building the robot with the provided parts and using the [documentation](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-v1/ses-v1-robots/ses-v1-bipeds/pete/). Before attaching the motors, they need to be calibrated using [LynxTerm](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-software/lynxterm/), a program provided by the Lynxmotion team.

> **Note:** the documentation doesn't specify the right screw type when mounting the motors, and the horn of the motor should be made of metal.

##### Running the program

The Lynxmotion hardware [SSC-32U](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/servo-erector-set-system/ses-electronics/ses-modules/ssc-32u/) servo controller is a dedicated RC servo controller with some big features. It has high resolution (1uS) for accurate positioning, and extremely smooth moves. The range is 0.50mS to 2.50mS for a range of about 180°. The board's baudrate can be changed manually by pressing a combination of buttons and, as a servo controller, it only acts as a translator between an intelligent board or computer and the servos. All details about programming it and utility functions can be found on their [user guide (pdf)](https://wiki.lynxmotion.com/info/wiki/lynxmotion/download/servo-erector-set-system/ses-electronics/ses-modules/ssc-32u/WebHome/lynxmotion_ssc-32u_usb_user_guide.pdf). It is recommended that the user doesn't try to initialize all the motors in a single sequence, the current draw may be too high for the board to handle.

> **Note:** the sequence of the commands has a simple rule `#<ch>P<position>T<time>`.

##### The missing head

After following all the instructions the user may see that there is a missing piece in the components and also in the documentation. The head of the robot is missing. For this build to be completed, a creative mind is required: either design in CAD or Blender a head to 3D print or to make a handmade head. This '_freedom of head_' is a good test for creativity, the user may even add additional sensors on the head, the SSC32U board can read additional sensor data if required.

---

#### The program

The code reads a configuration file in [yaml](https://en.wikipedia.org/wiki/YAML) format, which describes the details of the system. Using it, the program can read multiple poses and also save them. In addition, it has a manual and automatic calibration and control, every function being well documented. Example of the configuration file:

```yaml
system:
  baud_rate: 115200
  port: COM3
common:
  timeout: 1000
servos:
  right_arm:
    motor_ids:
    - 0
    - 1
    - 2
    - 3
    home_positions:
    - 1530
    - 1530
    - 1490
    - 1420
    joint_names:
    - shoulder
    - elbow
    - wrist
    - hand
```

#### TODO (there is always something to do)

* an urdf file + simulation
* an XBee bluetooth driver for easier control
* more gestures
 
