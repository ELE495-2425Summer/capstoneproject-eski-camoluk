import 'dart:developer';

import 'package:mongo_dart/mongo_dart.dart';
import 'package:picar_mobile/dbHelper/constants.dart';

class MongoDatabase {
  static var db,
      JSONCollection,
      audioCollection,
      historyCollection,
      statusCollection,
      personCollection;

  static connect() async {
    try {
      db = await Db.create(MONGO_CONN_URL);
      await db.open();

      audioCollection = db.collection("ses_ciktisi");
      JSONCollection = db.collection("algilanan_json");
      historyCollection = db.collection("gorev_gecmisi");
      statusCollection = db.collection("arac_durumu");
      personCollection = db.collection("kullanici_kimliklendirme");

      log("✅ MongoDB bağlantısı başarılı");
    } catch (e) {
      log("❌ MongoDB bağlantısı başarısız: $e");
    }
  }

  static Future<String> getAudioData() async {
    try {
      final data = await audioCollection.findOne();
      if (data != null && data["ses"] != null) {
        return data["ses"];
      } else {
        return "Boş";
      }
    } catch (e) {
      return "Hata";
    }
  }

  static Future<String> getJSONData() async {
    try {
      final data = await JSONCollection.findOne();
      if (data != null && data["json"] != null) {
        return data["json"];
      } else {
        return "Boş";
      }
    } catch (e) {
      return "Hata";
    }
  }

  static Future<String> getStatusData() async {
    try {
      final data = await statusCollection.findOne();
      if (data != null && data["durum"] != null) {
        return data["durum"];
      } else {
        return "Boş";
      }
    } catch (e) {
      return "Hata";
    }
  }

  static Future<String> getSpeakerData() async {
    try {
      final data = await personCollection.findOne();
      if (data != null) {
        if (data["herkes"] == true) {
          return "Herkes";
        } else if (data["secilen_efe"] == true) {
          return "Efe";
        } else if (data["secilen_alperen"] == true) {
          return "Alperen";
        } else if (data["secilen_yagiz"] == true) {
          return "Yağız";
        } else if (data["secilen_yilmaz"] == true) {
          return "Yılmaz";
        } else {
          return "Boş"; // data var ama hiçbiri seçili değilse
        }
      } else {
        return "Boş";
      }
    } catch (e) {
      return "Hata";
    }
  }

  static Future<String> getFormattedLogs() async {
    try {
      final dataList = await historyCollection.find().toList();
      if (dataList.isNotEmpty) {
        String result = "";
        for (int i = 0; i < dataList.length; i++) {
          final gecmis = dataList[i]["gecmis"] ?? "Bilinmeyen";
          result += "[${i + 1}] $gecmis\n";
        }
        return result;
      } else {
        return "Boş";
      }
    } catch (e) {
      return "Hata";
    }
  }
}
