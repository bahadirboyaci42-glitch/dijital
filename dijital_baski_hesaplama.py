"""
Dijital Baskı Hesaplama Sistemi
Makine ve kağıt parametrelerine göre baskı maliyetini hesaplar
"""

class DiastalBaskiHesaplama:
    """Dijital baskı maliyeti hesaplamak için sınıf"""
    
    def __init__(self, makine_saati_maliyeti=500, kurulum_zamani=30):
        """
        Parametreler:
        - makine_saati_maliyeti: Saatlik makine maliyeti (TL)
        - kurulum_zamani: Kurulum süresi (dakika)
        """
        self.makine_saati_maliyeti = makine_saati_maliyeti
        self.kurulum_zamani = kurulum_zamani
        self.kağıt_fiyatları = {
            'A4': 0.05,           # TL/adet
            'A3': 0.15,           # TL/adet
            'A2': 0.35,           # TL/adet
            'A1': 0.75,           # TL/adet
            'poster_60x90': 1.50, # TL/adet
            'poster_80x120': 2.80 # TL/adet
        }
        self.baskı_hızları = {
            'A4': 120,            # adet/dakika
            'A3': 80,             # adet/dakika
            'A2': 40,             # adet/dakika
            'A1': 25,             # adet/dakika
            'poster_60x90': 15,   # adet/dakika
            'poster_80x120': 10   # adet/dakika
        }
    
    def kağıt_maliyeti_hesapla(self, kağıt_türü, adet):
        """Kağıt maliyetini hesapla"""
        if kağıt_türü not in self.kağıt_fiyatları:
            raise ValueError(f"Bilinmeyen kağıt türü: {kağıt_türü}")
        
        fiyat = self.kağıt_fiyatları[kağıt_türü]
        toplam_maliyet = fiyat * adet
        return toplam_maliyet
    
    def baskı_süresi_hesapla(self, kağıt_türü, adet):
        """Baskı süresini hesapla (dakika)"""
        if kağıt_türü not in self.baskı_hızları:
            raise ValueError(f"Bilinmeyen kağıt türü: {kağıt_türü}")
        
        hız = self.baskı_hızları[kağıt_türü]
        baskı_süresi = adet / hız
        toplam_süre = self.kurulum_zamani + baskı_süresi
        
        return {
            'kurulum_dakika': self.kurulum_zamani,
            'baskı_dakika': round(baskı_süresi, 2),
            'toplam_dakika': round(toplam_süre, 2),
            'toplam_saat': round(toplam_süre / 60, 2)
        }
    
    def makine_maliyeti_hesapla(self, kağıt_türü, adet):
        """Makine maliyetini hesapla"""
        süre_bilgisi = self.baskı_süresi_hesapla(kağıt_türü, adet)
        toplam_saat = süre_bilgisi['toplam_saat']
        makine_maliyeti = toplam_saat * self.makine_saati_maliyeti
        return makine_maliyeti
    
    def toplam_birim_maliyet_hesapla(self, kağıt_türü, adet):
        """Toplam birim maliyeti hesapla"""
        kağıt_maliyeti = self.kağıt_maliyeti_hesapla(kağıt_türü, adet)
        makine_maliyeti = self.makine_maliyeti_hesapla(kağıt_türü, adet)
        toplam_maliyet = kağıt_maliyeti + makine_maliyeti
        birim_maliyet = toplam_maliyet / adet
        
        return {
            'kağıt_maliyeti': round(kağıt_maliyeti, 2),
            'makine_maliyeti': round(makine_maliyeti, 2),
            'toplam_maliyet': round(toplam_maliyet, 2),
            'birim_maliyet': round(birim_maliyet, 4)
        }
    
    def detaylı_hesapla(self, kağıt_türü, adet, kar_oranı=30):
        """Detaylı hesaplama (maliyet + kar marjı)"""
        maliyet_detayı = self.toplam_birim_maliyet_hesapla(kağıt_türü, adet)
        süre_detayı = self.baskı_süresi_hesapla(kağıt_türü, adet)
        
        birim_maliyet = maliyet_detayı['birim_maliyet']
        birim_satış_fiyatı = birim_maliyet * (1 + kar_oranı / 100)
        toplam_satış_fiyatı = birim_satış_fiyatı * adet
        
        return {
            'kağıt_türü': kağıt_türü,
            'adet': adet,
            'kağıt_birim_fiyatı': round(self.kağıt_fiyatları[kağıt_türü], 4),
            'toplam_kağıt_maliyeti': maliyet_detayı['kağıt_maliyeti'],
            'baskı_süresi': süre_detayı,
            'toplam_makine_maliyeti': maliyet_detayı['makine_maliyeti'],
            'toplam_maliyet': maliyet_detayı['toplam_maliyet'],
            'birim_maliyet': birim_maliyet,
            'kar_oranı': f"%{kar_oranı}",
            'birim_satış_fiyatı': round(birim_satış_fiyatı, 4),
            'toplam_satış_fiyatı': round(toplam_satış_fiyatı, 2),
            'toplam_kar': round(toplam_satış_fiyatı - maliyet_detayı['toplam_maliyet'], 2)
        }


def print_rapor(hesapla_sonucu):
    """Hesaplama sonuçlarını güzel formatta yazdır"""
    print("\n" + "="*60)
    print("DİJİTAL BASKI MALİYET HESAPLAMA RAPORU")
    print("="*60)
    print(f"\nKağıt Türü: {hesapla_sonucu['kağıt_türü']}")
    print(f"Adet: {hesapla_sonucu['adet']:,}")
    
    print("\n--- KAĞIT MALİYETİ ---")
    print(f"Birim Kağıt Fiyatı: {hesapla_sonucu['kağıt_birim_fiyatı']} TL")
    print(f"Toplam Kağıt Maliyeti: {hesapla_sonucu['toplam_kağıt_maliyeti']} TL")
    
    print("\n--- BASKI SÜRESİ ---")
    süre = hesapla_sonucu['baskı_süresi']
    print(f"Kurulum Süresi: {süre['kurulum_dakika']} dakika")
    print(f"Baskı Süresi: {süre['baskı_dakika']} dakika")
    print(f"Toplam Süre: {süre['toplam_dakika']} dakika ({süre['toplam_saat']} saat)")
    
    print("\n--- MAKİNE MALİYETİ ---")
    print(f"Toplam Makine Maliyeti: {hesapla_sonucu['toplam_makine_maliyeti']} TL")
    
    print("\n--- TOPLAM MALİYET ---")
    print(f"Toplam Maliyet: {hesapla_sonucu['toplam_maliyet']} TL")
    print(f"Birim Maliyet: {hesapla_sonucu['birim_maliyet']} TL")
    
    print("\n--- SATIR FİYAT HESAPLAMASI ---")
    print(f"Kar Marjı: {hesapla_sonucu['kar_oranı']}")
    print(f"Birim Satış Fiyatı: {hesapla_sonucu['birim_satış_fiyatı']} TL")
    print(f"Toplam Satış Fiyatı: {hesapla_sonucu['toplam_satış_fiyatı']} TL")
    print(f"Toplam Kar: {hesapla_sonucu['toplam_kar']} TL")
    print("="*60 + "\n")


def kullanıcı_girişi_al():
    """Kullanıcıdan gerekli bilgileri al"""
    print("\n" + "="*60)
    print("DİJİTAL BASKI MALİYET HESAPLAMA SISTEMI")
    print("="*60)
    
    # Kağıt türü seçimi
    print("\n📄 Kullanılabilir Kağıt Türleri:")
    kağıt_türleri = ['A4', 'A3', 'A2', 'A1', 'poster_60x90', 'poster_80x120']
    for i, tür in enumerate(kağıt_türleri, 1):
        print(f"  {i}. {tür}")
    
    while True:
        try:
            seçim = int(input("\nKağıt türünü seçiniz (1-6): "))
            if 1 <= seçim <= 6:
                kağıt_türü = kağıt_türleri[seçim - 1]
                break
            else:
                print("❌ Lütfen 1-6 arasında bir sayı giriniz!")
        except ValueError:
            print("❌ Geçersiz giriş! Lütfen sayı giriniz!")
    
    # Adet girişi
    while True:
        try:
            adet = int(input(f"\n{kağıt_türü} için kaç adet baskı yapılacak? "))
            if adet > 0:
                break
            else:
                print("❌ Lütfen 0'dan büyük bir sayı giriniz!")
        except ValueError:
            print("❌ Geçersiz giriş! Lütfen sayı giriniz!")
    
    # Kar marjı girişi
    while True:
        try:
            kar_oranı = float(input("\nKar marjı yüzdesi (varsayılan %30): ") or "30")
            if kar_oranı >= 0:
                break
            else:
                print("❌ Lütfen 0 veya daha büyük bir sayı giriniz!")
        except ValueError:
            print("❌ Geçersiz giriş! Lütfen sayı giriniz!")
    
    return kağıt_türü, adet, kar_oranı


# Kullanım Örneği
if __name__ == "__main__":
    # Hesaplama sistemini oluştur
    hesap = DiastalBaskiHesaplama(
        makine_saati_maliyeti=500,  # TL/saat
        kurulum_zamani=30            # dakika
    )
    
    while True:
        # Kullanıcıdan girişi al
        kağıt_türü, adet, kar_oranı = kullanıcı_girişi_al()
        
        # Hesapla ve raporla
        sonuc = hesap.detaylı_hesapla(kağıt_türü, adet, kar_oranı=kar_oranı)
        print_rapor(sonuc)
        
        # Tekrar sormak isteyip istemediğini sor
        devam = input("Başka bir hesaplama yapmak ister misiniz? (E/H): ").upper()
        if devam != 'E':
            print("\n👋 Hoşça kalınız!\n")
            break
