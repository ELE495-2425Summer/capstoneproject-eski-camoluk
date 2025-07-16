import 'package:flutter/material.dart';
import 'package:picar_mobile/data/constants.dart';
import 'package:picar_mobile/pages/about_page.dart';
import 'package:picar_mobile/widgets/user_input.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  TextEditingController controllerUserName = TextEditingController();

  TextEditingController controllerPw = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              SizedBox(height: 90.0),
              Text(
                "Hoşgeldiniz",
                style: KTextStyle(fontSize: 32).titleStyle,
              ),
              SizedBox(height: 15.0),
              Text(
                "Giriş yapmak için lütfen kullanıcı adınızı ve şifrenizi girin",
                style: KTextStyle.descriptionStyle,
              ),
              SizedBox(height: 30.0),
              Hero(
                tag: "hero1",
                child: Image.asset("assets/images/tobblogosu.png"),
              ),
              Container(
                margin: EdgeInsets.only(top: 30),
                width: 318,
                child: Column(
                  children: [
                    UserInput(
                      hintText: "Kullanıcı Adı",
                      controller: controllerUserName,
                    ),
                    SizedBox(height: 5.0),
                    UserInput(
                      hintText: "Şifre",
                      controller: controllerPw,
                    ),
                    SizedBox(height: 5.0),
                    SizedBox(
                      width: double.infinity,
                      child: FilledButton(
                        onPressed: () {
                          Navigator.pushReplacement(
                            context,
                            MaterialPageRoute(
                              builder: (context) {
                                return AboutPage();
                              },
                            ),
                          );
                        },
                        style: FilledButton.styleFrom(
                          backgroundColor: Color(0xFF540B0E),
                        ),
                        child: Text(
                          "Giriş",
                          style: TextStyle(color: Color(0xFFE09F3E)),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
