import 'dart:async';

import 'package:flutter/material.dart';
import 'package:picar_mobile/data/constants.dart';
import 'package:picar_mobile/dbHelper/mongodb.dart';
import 'package:picar_mobile/widgets/drawer_widget.dart';

class LogsPage extends StatefulWidget {
  const LogsPage({super.key});

  @override
  State<LogsPage> createState() => _LogsPageState();
}

class _LogsPageState extends State<LogsPage> {
  String logs = "";
  Timer? timerLog;

  @override
  void initState() {
    super.initState();
    timerLog = Timer.periodic(Duration(seconds: 1), (timer) {
      fetchLogs();
    });
  }

  void fetchLogs() async {
    String newLogs = await MongoDatabase.getFormattedLogs();
    setState(() {
      logs = newLogs;
    });
  }

  @override
  void dispose() {
    timerLog?.cancel(); // sayfa kapanırken timer'ı iptal et
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text(
          "Komut Geçmişi",
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
        padding: EdgeInsets.symmetric(
          vertical: 30.0,
          horizontal: 10.0,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.all(15.0),
              child: Text(
                "Geçmiş Komutlar",
                style: KTextStyle(fontSize: 16).titleStyle,
              ),
            ),
            Container(
              height: 500,
              width: double.infinity,
              decoration: BoxDecoration(
                color: const Color(0xFF2F4F4F), // Koyu arka plan tonu
                borderRadius: BorderRadius.circular(10.0),
                border: Border.all(
                  color: Colors.grey.shade400,
                  width: 1.0,
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black,
                    offset: Offset(0, 2),
                    blurRadius: 4.0,
                  ),
                ],
              ),
              child: Padding(
                padding: const EdgeInsets.all(10.0),
                child: SingleChildScrollView(
                  scrollDirection: Axis.vertical,
                  child: Text(
                    logs,
                    style: TextStyle(color: Colors.white),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
      drawer: DrawerWidget(),
    );
  }
}
