## Lynxmotion PETE
Known for their **high-quality** components and ease of use, [Lynxmotion](https://www.lynxmotion.com/) caters to both educational and hobbyist markets. Their products are designed for versatility, allowing for numerous configurations and expansions, making them a favorite in STEM education and robotics competitions. Their lineup includes robotic arms, walking robots, rovers, and more, all built with the versatile Servo Erector Set (SES) system.

The **Lynxmotion SES-V1 humanoid robot [PETE](https://www.lynxmotion.com/driver.aspx?Topic=assem02#pete)** is part of the Lynxmotion large robots lineup. PETE is a 22 DoF R/C servo based biped walker with gripper hands: 14x Hitec HS-645 high-torque servos for the foot, ankle, knee, hip, "waist" and 2DoF shoulder.
6x Hitec HS-422 servos for the wrist, gripper, neck and head and elbow.

![alt text](https://eu.robotshop.com/cdn/shop/files/lynxmotion-pete-humanoid-development-platform-no-electronics-1.webp?v=1720508194&width=500)

The robot is made from black anodized aluminum servo brackets and ultra-tough laser-cut Lexan structural components. Since the kit is based on the Servo Erector Set (S.E.S.), the parts can be easily used (in conjunction with a few other parts sold separately) to make a variety of other robots such as quadrupeds, hexapods, robot arms and more.
##### First steps
The first step for this project is building the robot using the parts provided and the [documentation](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-v1/ses-v1-robots/ses-v1-bipeds/pete/) and before putting the motors in you need to calibrate them using [LynxTerm](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-software/lynxterm/), a program provided by the Lynxmotion team. On another point, the documentation doesn't specify the right screw type when mounting the motors, and the horn of the motor should be made of metal.
##### Running the program
The Lynxmotion hardware [SSC-32U](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/servo-erector-set-system/ses-electronics/ses-modules/ssc-32u/) servo controller is a dedicated RC servo controller with some big features. It has high resolution (1uS) for accurate positioning, and extremely smooth moves. The range is 0.50mS to 2.50mS for a range of about 180°. The board's baudrate can be changed manually by pressing a combination of buttons and as a servo controller it only acts as a translator between an inteligent board or an computer. All details about programming it and functions can be foun on their [user guide pdf](https://wiki.lynxmotion.com/info/wiki/lynxmotion/download/servo-erector-set-system/ses-electronics/ses-modules/ssc-32u/WebHome/lynxmotion_ssc-32u_usb_user_guide.pdf), the sequence of the commands has a simple rule `#<ch>P<position>T<time>`. It is recomended that the user doesn't try to initiate all the motors in a single secvence, the voltage may be to strong for the board to handle.
##### The missing head
After following all the instruction the user may see that there is a missing piece in the components and also in the documentation. The head of the robot is missing, for this build to be completed it is required a creative mind; either design in CAD or Blender a head to 3d print or to mage an handmade head. This '_freedom of head_' is a good test for creativity, the user may even add additional sensors on his head, the SSC32U board can read sensor data.
---
#### The program
This build also has been run on a self-made python code. Using the [json](https://en.wikipedia.org/wiki/JSON) file for reading configuration the program can read multiple poses and also save them. Has an manual and automatic calibration and control, every function having a description in the code.

Things to add:
* an urdf file + simulation
* an XBee bluetooth driver for easier control
* more gestures
