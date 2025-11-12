#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch İşleme Script'i
Birden fazla hesaplama isteğini dosyadan okuyup işler
"""

import json
import subprocess
import sys
from pathlib import Path


def batch_hesapla(input_file, output_file=None):
    """
    Batch dosyasından hesaplamaları oku ve işle
    
    input_file: JSON satırları içeren dosya (her satır bir hesaplama)
    output_file: Sonuçları yazmak için dosya (varsayılan: stdout)
    """
    
    script_path = Path(__file__).parent / "dijital_baski_hesaplama_server.py"
    
    if not script_path.exists():
        print(f"Hata: {script_path} bulunamadı!", file=sys.stderr)
        sys.exit(1)
    
    sonuçlar = []
    hatalar = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for satır_no, satır in enumerate(f, 1):
                satır = satır.strip()
                
                # Boş satırları atla
                if not satır:
                    continue
                
                # Yorum satırlarını atla (# ile başlayanlar)
                if satır.startswith('#'):
                    continue
                
                try:
                    # Server script'ini çağır
                    process = subprocess.Popen(
                        ['python3', str(script_path)],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    stdout, stderr = process.communicate(input=satır, timeout=10)
                    
                    if process.returncode == 0:
                        sonuç = json.loads(stdout)
                        sonuç['girdi_satırı'] = satır_no
                        sonuçlar.append(sonuç)
                    else:
                        hatalar.append({
                            'satır': satır_no,
                            'girdi': satır,
                            'hata': stderr or stdout
                        })
                
                except subprocess.TimeoutExpired:
                    process.kill()
                    hatalar.append({
                        'satır': satır_no,
                        'girdi': satır,
                        'hata': 'İşlem Timeout'
                    })
                except json.JSONDecodeError:
                    hatalar.append({
                        'satır': satır_no,
                        'girdi': satır,
                        'hata': 'JSON Parse Hatası'
                    })
                except Exception as e:
                    hatalar.append({
                        'satır': satır_no,
                        'girdi': satır,
                        'hata': str(e)
                    })
    
    except FileNotFoundError:
        print(f"Hata: {input_file} dosyası bulunamadı!", file=sys.stderr)
        sys.exit(1)
    
    # Sonuçları hazırla
    output_data = {
        "toplam_işlem": satır_no if 'satır_no' in locals() else 0,
        "başarılı": len(sonuçlar),
        "başarısız": len(hatalar),
        "sonuçlar": sonuçlar,
        "hatalar": hatalar if hatalar else None
    }
    
    # Çıktı yap
    output_json = json.dumps(output_data, ensure_ascii=False, indent=2)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"✅ Sonuçlar {output_file} dosyasına yazıldı")
    else:
        print(output_json)
    
    return len(hatalar) == 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
Batch İşleme Script'i

Kullanım:
  python3 dijital_baski_batch.py <input_file> [output_file]

Input Dosya Formatı (her satır bir JSON):
  {"kağıt_türü": "A4", "adet": 1000}
  {"kağıt_türü": "A3", "adet": 500, "kar_oranı": 35}
  # Bu satır yorum ve atlanır
  {"kağıt_türü": "poster_60x90", "adet": 100}

Örnek:
  # Sonuçları stdout'a yaz
  python3 dijital_baski_batch.py hesaplamalar.json

  # Sonuçları dosyaya yaz
  python3 dijital_baski_batch.py hesaplamalar.json sonuçlar.json
        """)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    başarılı = batch_hesapla(input_file, output_file)
    sys.exit(0 if başarılı else 1)
