import 'package:flutter/material.dart';
import 'package:picar_mobile/data/constants.dart';
import 'package:picar_mobile/widgets/drawer_widget.dart';

class AboutPage extends StatelessWidget {
  const AboutPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text(
          "Hakkında",
          style: KTextStyle(fontSize: 24).titleStyle,
        ),
        toolbarHeight: 80,
        backgroundColor: Color(0xFF540B0E),
        leading: Builder(
          builder: (context) {
            return IconButton(
              onPressed: () {
                Scaffold.of(context).openDrawer();
              },
              icon: Icon(Icons.menu, color: Colors.white),
            );
          },
        ),
        actions: [
          Hero(
            tag: "hero1",
            child: Container(
              margin: EdgeInsets.only(right: 10.0),
              child: Image.asset(
                "assets/images/tobblogosu.png",
                height: 60.0,
              ),
            ),
          ),
        ],
      ),
      body: Container(
        margin: EdgeInsets.only(top: 50.0, left: 20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "Uygulama Hakkında",
              style: KTextStyle(fontSize: 24).titleStyle,
            ),
            SizedBox(height: 10),
            Padding(
              padding: const EdgeInsets.only(left: 10.0),
              child: Text(
                "Türkçe doğal dil ile verilen sesli komutları algılayarak bu komutları temel hareket talimatlarına dönüştürüp uygulayabilen tekerlekli, otonom bir mini araç tasarlanmıştır. Sistem, sesli komutları önce yazıya çevirir, ardından bir dil modeli kullanarak bu metni analiz eder ve temel hareket komutlarına dönüştürür. Araç, sensörler ve motor kontrol birimleri aracılığıyla bu komutları otonom şekilde gerçekleştirir. Kullanıcıya Türkçe olarak sesli geri bildirim verir. Proje kapsamında mikrodenetleyici/mikrobilgisayar tabanlı bir gömülü sistem tasarımı yapılmıştır. Konuşma tanıma, doğal dil işleme, hareket kontrolü gibi özellikler eklenmiştir. Aracın mevcut durumu kullanıcı arayüzü aracılığıyla bildirilmektedir.",
                style: KTextStyle.descriptionStyle,
              ),
            ),
            SizedBox(height: 150),
            Text(
              "Üyeler",
              style: KTextStyle(fontSize: 24).titleStyle,
            ),
            SizedBox(height: 10),
            Padding(
              padding: const EdgeInsets.only(left: 10.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Alperen Çağrı BARIŞ",
                    style: KTextStyle.descriptionStyle,
                  ),
                  Text(
                    "Yılmaz DUMAN",
                    style: KTextStyle.descriptionStyle,
                  ),
                  Text(
                    "Efe HAYLAZ",
                    style: KTextStyle.descriptionStyle,
                  ),
                  Text(
                    "Fatih Kerem MAZLUM",
                    style: KTextStyle.descriptionStyle,
                  ),
                  Text(
                    "Yağız ZENGİN",
                    style: KTextStyle.descriptionStyle,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      drawer: DrawerWidget(),
    );
  }
}
