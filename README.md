# 🖨️ Dijital Baskı Hesaplama Sistemi

Dijital baskı maliyetini makine ve kağıt parametrelerine göre hesaplayan Python uygulaması.

## 🚀 Başlamak İçin

### 🖥️ İnteraktif Mod (Local)

```bash
python3 dijital_baski_hesaplama.py
```

### 🐧 Server Mod (Linux Sunucu - JSON Input)

```bash
echo '{"kağıt_türü": "A4", "adet": 1000}' | python3 dijital_baski_hesaplama_server.py
```

### 📦 Batch İşleme (Birden Fazla Hesaplama)

```bash
python3 dijital_baski_batch.py hesaplamalar.json
# veya sonuçları dosyaya yaz
python3 dijital_baski_batch.py hesaplamalar.json sonuçlar.json
```

## 📋 Program Akışı

1. **Kağıt Türünü Seçin** (1-6)
   - 1: A4
   - 2: A3
   - 3: A2
   - 4: A1
   - 5: Poster 60x90
   - 6: Poster 80x120

2. **Baskı Adetini Giriniz** (pozitif tam sayı)

3. **Kar Marjı Yüzdesini Giriniz** (varsayılan %30)
   - Boş bırakıp Enter'a basarsanız %30 uygulanır

4. **Raporunuz Görüntülenir**
   - Kağıt maliyeti
   - Baskı süresi
   - Makine maliyeti
   - Toplam maliyet ve kar hesaplaması

5. **Tekrar Hesaplama?**
   - E: Başka hesaplama yap
   - H: Çık

## 📊 Örnek Kullanım

```
Kağıt türünü seçiniz (1-6): 1
A4 için kaç adet baskı yapılacak? 1000
Kar marjı yüzdesi (varsayılan %30): 30
```

**Sonuç:**
- Toplam Maliyet: 370 TL
- Birim Maliyet: 0.37 TL
- Satış Fiyatı: 481 TL
- Kar: 111 TL

## ⚙️ Yapılandırma

`dijital_baski_hesaplama.py` dosyasında şu parametreleri değiştirebilirsiniz:

```python
hesap = DiastalBaskiHesaplama(
    makine_saati_maliyeti=500,  # TL/saat
    kurulum_zamani=30            # dakika
)
```

## 📈 Kağıt Fiyatları (Birim Fiyat)

| Kağıt Türü | Fiyat |
|-----------|-------|
| A4 | 0.05 TL |
| A3 | 0.15 TL |
| A2 | 0.35 TL |
| A1 | 0.75 TL |
| Poster 60x90 | 1.50 TL |
| Poster 80x120 | 2.80 TL |

## 🏭 Baskı Hızları

| Kağıt Türü | Hız |
|-----------|-----|
| A4 | 120 adet/dakika |
| A3 | 80 adet/dakika |
| A2 | 40 adet/dakika |
| A1 | 25 adet/dakika |
| Poster 60x90 | 15 adet/dakika |
| Poster 80x120 | 10 adet/dakika |

---

💡 **İpucu:** Farklı ebat ve adetler için hızlı hesaplama yapabilirsiniz!

## 🔧 Server Modu Detayları

### JSON Input Formatı

```json
{
  "kağıt_türü": "A4",
  "adet": 1000,
  "kar_oranı": 30,
  "makine_saati_maliyeti": 500,
  "kurulum_zamani": 30
}
```

**Alanlar:**
- `kağıt_türü` *(gerekli)*: A4, A3, A2, A1, poster_60x90, poster_80x120
- `adet` *(gerekli)*: Baskı adet sayısı
- `kar_oranı` *(opsiyonel)*: Kar marjı (varsayılan: 30)
- `makine_saati_maliyeti` *(opsiyonel)*: Saatlik makine maliyeti (varsayılan: 500 TL)
- `kurulum_zamani` *(opsiyonel)*: Kurulum süresi dakika (varsayılan: 30)

### Server Modu Kullanım Örnekleri

**Örnek 1: Basit Hesaplama**
```bash
echo '{"kağıt_türü": "A4", "adet": 1000}' | python3 dijital_baski_hesaplama_server.py
```

**Örnek 2: Kar Oranı Belirterek**
```bash
echo '{"kağıt_türü": "A3", "adet": 500, "kar_oranı": 35}' | python3 dijital_baski_hesaplama_server.py
```

**Örnek 3: Dosyadan Okumak**
```bash
cat hesaplamalar.json | python3 dijital_baski_hesaplama_server.py
```

**Örnek 4: Curl ile HTTP POST (eğer server kurulu ise)**
```bash
curl -X POST -d '{"kağıt_türü": "A4", "adet": 1000}' http://localhost:5000/hesapla
```

### Server Modu Çıktı Formatı

```json
{
  "status": "success",
  "data": {
    "kağıt_türü": "A4",
    "adet": 1000,
    "kağıt_birim_fiyatı": 0.05,
    "toplam_kağıt_maliyeti": 50.0,
    "baskı_süresi": {
      "kurulum_dakika": 30.0,
      "baskı_dakika": 8.33,
      "toplam_dakika": 38.33,
      "toplam_saat": 0.64
    },
    "toplam_makine_maliyeti": 320.0,
    "toplam_maliyet": 370.0,
    "birim_maliyet": 0.37,
    "kar_oranı": "%30.0",
    "birim_satış_fiyatı": 0.481,
    "toplam_satış_fiyatı": 481.0,
    "toplam_kar": 111.0
  }
}
```

## 📋 Batch Mode Detayları

### Batch Dosya Formatı

Her satırda bir JSON hesaplama isteği:

```json
{"kağıt_türü": "A4", "adet": 1000}
{"kağıt_türü": "A3", "adet": 500, "kar_oranı": 35}
# Bu satır yorum - atlanır
{"kağıt_türü": "poster_60x90", "adet": 100}
```

### Batch Modu Kullanım Örnekleri

**Örnek 1: Sonuçları Ekrana Yaz**
```bash
python3 dijital_baski_batch.py hesaplamalar.json
```

**Örnek 2: Sonuçları Dosyaya Yaz**
```bash
python3 dijital_baski_batch.py hesaplamalar.json sonuçlar.json
```

**Örnek 3: Pipe ile Kullanma**
```bash
cat hesaplamalar.json | python3 dijital_baski_batch.py /dev/stdin
```

### Batch Modu Çıktı Formatı

```json
{
  "toplam_işlem": 3,
  "başarılı": 3,
  "başarısız": 0,
  "sonuçlar": [
    { "status": "success", "data": {...} },
    { "status": "success", "data": {...} }
  ],
  "hatalar": null
}
```

## 🐳 Docker İle Kullanım (Linux Sunucu)

`Dockerfile` oluşturun:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY dijital_baski_hesaplama.py .
COPY dijital_baski_hesaplama_server.py .
ENTRYPOINT ["python3", "dijital_baski_hesaplama_server.py"]
```

Build ve çalıştırma:
```bash
docker build -t dijital-baski .
echo '{"kağıt_türü": "A4", "adet": 1000}' | docker run -i dijital-baski
```
