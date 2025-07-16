import 'package:flutter/material.dart';
import 'package:picar_mobile/dbHelper/mongodb.dart';
import 'package:picar_mobile/pages/login_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await MongoDatabase.connect();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PiCar',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Color(0xFF335C67),
        ),
        useMaterial3: true,
        scaffoldBackgroundColor: Color(0xFF335C67),
      ),
      debugShowCheckedModeBanner: false,
      home: LoginPage(),
    );
  }
}
