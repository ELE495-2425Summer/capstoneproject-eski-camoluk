# TOBB ETÜ ELE495 - Capstone Project

# Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Acknowledgements](#acknowledgements)

## Introduction
This Project focuses on developing autonomous vehicle prototype capable of running with Turkish voice commands. Raspberry pi 4 is used for operation. The vehicle acquires voice commands through microphone, these commands are converted to text commands through Google cloud. Text commands are sent to Open AI API for jason formatting for our system. Movement commands are executed using DC motors, motor controllers and gyroscope.

## Features
List the key features and functionalities of the project.
- Hardware: The hardware components used (should be listed with links)
- Operating System and packages
- Applications 
- Services 

## Hardware
- Raspberry Pi 4
- MPU6050 Gyroscope Accelerometer
- SG90 RC Mini (9gr) Servo Motor
- L298N Motor Driver
- DC Motor
- Power Supply

## Installation
Describe the steps required to install and set up the project. Include any prerequisites, dependencies, and commands needed to get the project running.

"Arayuz_Uygulama" klasöründe build ve dist klasörleri bulunmaktadır. Burada bulunan dosyanın indirilmesi ile bilgisayarda çalışacak bir uygulama indirilebilir. Herhangi bir kütüphane indirilmesine gerek yoktur.

Benzer bir şekilde "Arayuz_BitirmeProje" klasöründe .exe haline getirilmemiş uygulama çalıştırılabilir. Bu kodun çalıştırılabilmesi için "vlc", "PyQT 5", "paramiko", "pymongo" kütüphanelerinin indirilmiş olması gerekmektedir. 



```bash
# Example commands
git clone https://github.com/username/project-name.git
cd project-name
```

## Usage
Provide instructions and examples on how to use the project. Include code snippets or screenshots where applicable.

## Screenshots
Include screenshots of the project in action to give a visual representation of its functionality. You can also add videos of running project to YouTube and give a reference to it here.

Aşağıda bilgisayar uygulamasına ait görseller eklenmiştir.

![Bilgisayar Uygulaması - 1](image.png)
![Bilgisayar Uygulaması - 2](image-1.png)

Aynı zamanda bir mobil uygulama tasarımı da yapılmıştır. Aşağıda mobil uygulamaya ait görseller bulunmaktadır.

![Mobil Uygulama -1](image-2.png)
![Mobil Uygulama -2](image-3.png)
![Mobil Uygulama -3](image-4.png)
![Mobil Uygulama -4](image-5.png)
## Acknowledgements
Give credit to those who have contributed to the project or provided inspiration. Include links to any resources or tools used in the project.

[Contributor 1](https://github.com/user1)
[Resource or Tool](https://www.nvidia.com)
