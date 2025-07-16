import 'package:flutter/material.dart';
import 'package:picar_mobile/data/constants.dart';
import 'package:picar_mobile/pages/about_page.dart';
import 'package:picar_mobile/pages/carInfo_page.dart';
import 'package:picar_mobile/pages/logs_page.dart';

class DrawerWidget extends StatelessWidget {
  const DrawerWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: Color(0xFF335C67),
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          Container(
            height: 143.0,
            child: DrawerHeader(
              decoration: BoxDecoration(color: Color(0xFF540B0E)),
              child: Center(
                child: Text(
                  'Menü',
                  style: KTextStyle(fontSize: 24).titleStyle,
                ),
              ),
            ),
          ),
          ListTile(
            leading: Icon(Icons.info, color: Colors.white),
            title: Text(
              'Hakkında',
              style: KTextStyle(fontSize: 20).titleStyle,
            ),
            onTap: () {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (context) {
                    return AboutPage();
                  },
                ),
              );
            },
          ),
          ListTile(
            leading: Icon(Icons.directions_car, color: Colors.white),
            title: Text(
              'Araba İzleme',
              style: KTextStyle(fontSize: 20).titleStyle,
            ),
            onTap: () {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (context) {
                    return CarInfoPage();
                  },
                ),
              );
            },
          ),
          ListTile(
            leading: Icon(Icons.history, color: Colors.white),
            title: Text(
              'Komut Geçmişi',
              style: KTextStyle(fontSize: 20).titleStyle,
            ),
            onTap: () {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (context) {
                    return LogsPage();
                  },
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}
