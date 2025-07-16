import 'package:flutter/material.dart';

class KTextStyle {
  const KTextStyle({this.fontSize});

  final double? fontSize;

  TextStyle get titleStyle => TextStyle(
    color: const Color(0xFFFFF2B0),
    fontWeight: FontWeight.bold,
    fontSize: fontSize ?? 16, // <- null ise 16 kullan
  );

  static const TextStyle descriptionStyle = TextStyle(
    color: Color(0x80FFF2B0),
    fontSize: 15,
  );
}
