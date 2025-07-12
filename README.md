# TOBB ETÜ ELE495 - Capstone Project

# Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Acknowledgements](#acknowledgements)

## Introduction
Türkçe doğal dil ile verilen sesli komutları algılayarak bu komutları temel hareket talimatlarına dönüştürüp uygulayabilen tekerlekli, otonom bir mini araç tasarlanmıştır. Sistem, sesli komutları önce yazıya çevirir, ardından bir dil modeli kullanarak bu metni analiz eder ve temel hareket komutlarına dönüştürür. Araç, sensörler ve motor kontrol birimleri aracılığıyla bu komutları otonom şekilde gerçekleştirir. Kullanıcıya Türkçe olarak sesli geri bildirim verir. Proje kapsamında mikrodenetleyici/mikrobilgisayar tabanlı bir gömülü sistem tasarımı yapılmıştır. Konuşma tanıma, doğal dil işleme, hareket kontrolü gibi özellikler eklenmiştir. Aracın mevcut durumu kullanıcı arayüzü aracılığıyla bildirilmektedir. Kullanıcı arayüzü aynı zamanda aracın algıladığı sesleri, görev geçmişini ve hareket komutlarını içermektedir. Arayüz üzerinden belirli kullanıcıların seslerinin algılanabilmesi için kullanıcı kimliklendirmesi bölümü eklenmiştir. Kullanıcı kimliklendirme açılıp kapatılabilir ve kimlerin seslerinin algılanacağı seçilebilir. Ayrıca aracın bu arayüz aracılığıyla başlatılabilmesi sağlanmıştır. 

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

## Operating System and Packages
Bilgisayar uygulaması Windows işletim sistemi için tasarlanmıştır.

Mobil uygulama ise Android işletim sistemine sahip telefonlar için tasarlanmıştır.

Gereklilikler "Installation" bölümünde anlatılmıştır.

## Aplications
Bilgisayar uygulaması ve mobil uygulama tasarlanmıştır. Bilgisayar uygulaması aracılığıyla aracın başlatılabilmesi sağlanmıştır.

## Services
Uygulamada ve Raspberry Pi'ın içerisindeki kodda bir takım servis sağlayıcılarından faydalanılmıştır.

1- Eleven Labs
2- OpenAI
3- Google Cloud
4- Mongo DB
5- Porcupine

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

Aracı çalıştırmak için öncelikle arayüz üzerinden "Başlat" butonuna basılmalıdır. Ardından arayüz sizi bilgilendirdiğinde "Hey Pi Car" denmelidir. Bu cümle algılandığında araç kullanıcıyı dinlemeye başlayacaktır. Kullanıcı araçtan yapmasını beklediği komutları bu noktada söylemelidir.

Örneğin "5 metre ileri git" gibi bir komut verildiğinde. Bu komut bir JSON dosyasında gerekli değişkenlere uygun değerler verilerek oluşturulur. Program JSON'dan aldığı verilerle bilgisayar komutlarını fiziksel hareketlere çevirir ve araç hareket etmeye başlar.

Örneğin "Pizza sipariş et" gibi gerçekleştiremeyeceği bir komut verildiğinde ise araç, kullancının istediği komutu yerine getiremeyeceğini söyler ve kullanıcıdan yeni bir komut vermesini bekler.


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

Hazırlayanlar:
Yağız Zengin
Efe Haylaz
Yılmaz Duman
Alperen Çağrı Barış
Fatih Kerem Mazlum

[Contributor 1](https://github.com/user1)
[Resource or Tool](https://www.nvidia.com)
