import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:picar_mobile/data/constants.dart';
import 'package:picar_mobile/dbHelper/mongodb.dart';
import 'package:picar_mobile/widgets/drawer_widget.dart';

class CarInfoPage extends StatefulWidget {
  const CarInfoPage({super.key});

  @override
  State<CarInfoPage> createState() => _CarInfoPageState();
}

class _CarInfoPageState extends State<CarInfoPage> {
  String commandText = "";
  String json = "";
  String speaker = "";
  String status = "";
  Timer? timerCommand;
  Timer? timerJSON;
  Timer? timerSpeaker;
  Timer? timerStatus;

  @override
  void initState() {
    super.initState();
    timerCommand = Timer.periodic(Duration(seconds: 1), (timer) {
      getCommandFromAPI();
    });
    timerJSON = Timer.periodic(Duration(seconds: 1), (timer) {
      getJSONFromAPI();
    });
    timerSpeaker = Timer.periodic(Duration(seconds: 1), (timer) {
      getSpeakerFromAPI();
    });
    timerStatus = Timer.periodic(Duration(seconds: 1), (timer) {
      getStatusFromAPI();
    });
  }

  Future<void> getCommandFromAPI() async {
    String data = await MongoDatabase.getAudioData();
    if (commandText != data) {
      setState(() {
        commandText = data;
      });
    }
  }

  Future<void> getStatusFromAPI() async {
    String data =
        await MongoDatabase.getStatusData(); // doğru fonksiyon bu!
    if (status != data) {
      setState(() {
        status = data;
      });
    }
  }

  Future<void> getJSONFromAPI() async {
    String data =
        await MongoDatabase.getJSONData(); // doğru fonksiyon bu!
    if (json != data) {
      setState(() {
        json = data;
      });
    }
  }

  Future<void> getSpeakerFromAPI() async {
    String data =
        await MongoDatabase.getSpeakerData(); // doğru fonksiyon bu!
    speaker = data;
  }

  @override
  void dispose() {
    timerCommand?.cancel();
    timerJSON?.cancel();
    timerSpeaker?.cancel(); // sayfa kapanırken timer'ı iptal et
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text(
          "Araba İzleme",
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
          horizontal: 10.0,
          vertical: 30.0,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: Text(
                "Kim konuşuyor:  $speaker",
                style: KTextStyle(fontSize: 20).titleStyle,
              ),
            ),
            SizedBox(height: 10),
            Divider(),
            SizedBox(height: 20),
            SizedBox(
              height: 300.0,
              child: Row(
                children: [
                  // Söylenen Komut
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Center(
                          child: Text(
                            "SÖYLENEN KOMUT:",
                            style:
                                KTextStyle(fontSize: 16).titleStyle,
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          commandText.isNotEmpty ? commandText : "",
                          style: TextStyle(color: Colors.white),
                        ),
                      ],
                    ),
                  ),
                  VerticalDivider(),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Center(
                          child: Text(
                            "JSON KOMUTU:",
                            style:
                                KTextStyle(fontSize: 16).titleStyle,
                          ),
                        ),
                        SizedBox(height: 8),
                        Container(
                          height: 269,
                          width: 300,
                          decoration: BoxDecoration(
                            color: const Color(
                              0xFF2F4F4F,
                            ), // Koyu arka plan tonu
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
                          child: SingleChildScrollView(
                            scrollDirection: Axis.vertical,
                            child: SingleChildScrollView(
                              scrollDirection: Axis.horizontal,
                              child: Text(
                                json,
                                style: TextStyle(color: Colors.white),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            // Araba ve açıklama
            Container(
              margin: EdgeInsets.only(top: 50),
              child: Stack(
                children: [
                  Center(
                    child: Padding(
                      padding: const EdgeInsets.all(15.0),
                      child: Text(
                        status,
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  SizedBox(
                    height: 200,
                    child: Center(
                      child: Lottie.asset('assets/lotties/car.json'),
                    ),
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
