#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dijital Baskı Hesaplama Sistemi - Server Versiyonu
Linux sunucuda stdin üzerinden veri alır
"""

import sys
import json
from dijital_baski_hesaplama import DiastalBaskiHesaplama


def parse_input():
    """Stdin'den JSON formatında veri oku"""
    try:
        data = json.loads(sys.stdin.read())
        return data
    except json.JSONDecodeError as e:
        print(json.dumps({
            "error": f"JSON Parse Hatası: {str(e)}",
            "status": "error"
        }), file=sys.stdout)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "error": f"Veri Okuma Hatası: {str(e)}",
            "status": "error"
        }), file=sys.stdout)
        sys.exit(1)


def validate_input(data):
    """Gelen verileri doğrula"""
    required_fields = ['kağıt_türü', 'adet']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Gerekli alan eksik: {field}")
    
    kağıt_türü = str(data['kağıt_türü']).strip()
    adet = int(data['adet'])
    kar_oranı = float(data.get('kar_oranı', 30))
    
    valid_kağıtlar = ['A4', 'A3', 'A2', 'A1', 'poster_60x90', 'poster_80x120']
    if kağıt_türü not in valid_kağıtlar:
        raise ValueError(f"Geçersiz kağıt türü: {kağıt_türü}. Geçerli türler: {', '.join(valid_kağıtlar)}")
    
    if adet <= 0:
        raise ValueError(f"Adet 0'dan büyük olmalıdır: {adet}")
    
    if kar_oranı < 0:
        raise ValueError(f"Kar oranı negatif olamaz: {kar_oranı}")
    
    return kağıt_türü, adet, kar_oranı


def hesapla_ve_çıkış(kağıt_türü, adet, kar_oranı, 
                     makine_saati_maliyeti=500, kurulum_zamani=30):
    """Hesapla ve JSON formatında çıktı ver"""
    
    hesap = DiastalBaskiHesaplama(
        makine_saati_maliyeti=makine_saati_maliyeti,
        kurulum_zamani=kurulum_zamani
    )
    
    try:
        sonuc = hesap.detaylı_hesapla(kağıt_türü, adet, kar_oranı=kar_oranı)
        
        # Sonucu JSON formatına dönüştür
        çıktı = {
            "status": "success",
            "data": {
                "kağıt_türü": sonuc['kağıt_türü'],
                "adet": sonuc['adet'],
                "kağıt_birim_fiyatı": sonuc['kağıt_birim_fiyatı'],
                "toplam_kağıt_maliyeti": sonuc['toplam_kağıt_maliyeti'],
                "baskı_süresi": sonuc['baskı_süresi'],
                "toplam_makine_maliyeti": sonuc['toplam_makine_maliyeti'],
                "toplam_maliyet": sonuc['toplam_maliyet'],
                "birim_maliyet": sonuc['birim_maliyet'],
                "kar_oranı": sonuc['kar_oranı'],
                "birim_satış_fiyatı": sonuc['birim_satış_fiyatı'],
                "toplam_satış_fiyatı": sonuc['toplam_satış_fiyatı'],
                "toplam_kar": sonuc['toplam_kar']
            }
        }
        
        return çıktı
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def main():
    """Ana program"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
Dijital Baskı Hesaplama - Server Versiyonu

Kullanım:
  echo '{"kağıt_türü": "A4", "adet": 1000, "kar_oranı": 30}' | python3 dijital_baski_hesaplama_server.py

JSON Giriş Formatı:
  {
    "kağıt_türü": "A4|A3|A2|A1|poster_60x90|poster_80x120",
    "adet": 1000,
    "kar_oranı": 30  (opsiyonel, varsayılan: 30)
  }

Örnek Kullanımlar:
  # Basit hesaplama
  echo '{"kağıt_türü": "A4", "adet": 1000}' | python3 dijital_baski_hesaplama_server.py

  # Kar oranı belirterek
  echo '{"kağıt_türü": "A3", "adet": 500, "kar_oranı": 35}' | python3 dijital_baski_hesaplama_server.py

  # Dosyadan okumak
  cat hesaplamalar.json | python3 dijital_baski_hesaplama_server.py

Çıkış Formatı:
  {
    "status": "success|error",
    "data": {...},
    "error": "error mesajı (hata durumunda)"
  }
        """)
        sys.exit(0)
    
    # Stdin'den veri oku
    input_data = parse_input()
    
    try:
        # Verileri doğrula
        kağıt_türü, adet, kar_oranı = validate_input(input_data)
        
        # Makine parametreleri (opsiyonel)
        makine_saati_maliyeti = float(input_data.get('makine_saati_maliyeti', 500))
        kurulum_zamani = float(input_data.get('kurulum_zamani', 30))
        
        # Hesapla
        sonuc = hesapla_ve_çıkış(kağıt_türü, adet, kar_oranı,
                                makine_saati_maliyeti, kurulum_zamani)
        
        # JSON olarak yazdır
        print(json.dumps(sonuc, ensure_ascii=False, indent=2))
        
        # Hata varsa exit code'unu ayarla
        if sonuc["status"] == "error":
            sys.exit(1)
        
    except ValueError as e:
        çıktı = {
            "status": "error",
            "error": f"Girdi Hatası: {str(e)}"
        }
        print(json.dumps(çıktı, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        çıktı = {
            "status": "error",
            "error": f"Beklenmedik Hata: {str(e)}"
        }
        print(json.dumps(çıktı, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
