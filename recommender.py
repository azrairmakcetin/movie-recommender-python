import pandas as pd
import os
import sys

class FilmOneriSistemi:
    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu
        self.df = self.veri_yukle()

    def veri_yukle(self):
        """
        Veri setini okur ve temizler.
        """
        if not os.path.exists(self.dosya_yolu):
            print(f"\n❌ HATA: Dosya bulunamadı!")
            print(f"Kontrol edilen yol: {os.path.abspath(self.dosya_yolu)}")
            print("Lütfen 'movies' klasörünün ve 'movies.csv' dosyasının doğru yerde olduğundan emin olun.")
            sys.exit()

        try:
            
            df = pd.read_csv(self.dosya_yolu, sep=';', encoding='utf-8-sig')
            
           
            df.columns = df.columns.str.strip()
            
            
            metin_sutunlari = ['Başlık', 'Türler', 'Tip']
            for col in metin_sutunlari:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
            
            return df
        except Exception as e:
            print(f"\n❌ Veri okunurken kritik hata oluştu: {e}")
            sys.exit()

    def listele(self, sonuclar):
        if sonuclar.empty:
            print("\n⚠️  Kriterlere uygun film/dizi bulunamadı.")
        else:
            sayi = len(sonuclar)
            print(f"\n✅ {sayi} içerik bulundu. İşte en iyiler:\n")
            
            
            gosterim = sonuclar[['Başlık', 'Puan', 'Yıl', 'Tip', 'Türler']].head(10)
            print(gosterim.to_string(index=False))
            
            if sayi > 10:
                print(f"\n... ve {sayi - 10} adet daha içerik var.")
            print("-" * 60)

    def puan_ile_ara(self):
        try:
            girdi = input("Minimum puan kaç olsun? (Örn: 8.5): ").replace(',', '.')
            min_puan = float(girdi)
            sonuc = self.df[self.df['Puan'] >= min_puan].sort_values(by='Puan', ascending=False)
            self.listele(sonuc)
        except ValueError:
            print("❗ Lütfen geçerli bir sayı giriniz.")

    def yil_ile_ara(self):
        try:
            yil = int(input("Hangi yılı arıyorsunuz? (Örn: 2014): "))
            sonuc = self.df[self.df['Yıl'] == yil]
            self.listele(sonuc)
        except ValueError:
            print("❗ Lütfen geçerli bir yıl giriniz.")

    def kategori_ile_ara(self):
        kategori = input("Hangi türü arıyorsunuz? (Dram, Bilim Kurgu, Suç vb.): ").strip()
        
        sonuc = self.df[self.df['Türler'].str.contains(kategori, case=False, na=False)]
        self.listele(sonuc.sort_values(by='Puan', ascending=False))

    def gecmis_ve_oneri(self):
        print("\nLütfen izlediğiniz ve beğendiğiniz filmleri/dizileri virgülle ayırarak yazın.")
        print("Örnek: Inception, Breaking Bad, Joker")
        girdi = input("İzledikleriniz: ")
        
        if not girdi.strip():
            print("Boş giriş yaptınız.")
            return

        kullanici_listesi = [x.strip().lower() for x in girdi.split(',')]
        
        
        bulunanlar = self.df[self.df['Başlık'].str.lower().isin(kullanici_listesi)]
        
        if bulunanlar.empty:
            print("\n⚠️ Yazdığınız filmler veri setinde bulunamadı. İsimleri doğru yazdığınızdan emin olun.")
            return

        print(f"\n📋 Veritabanında eşleşenler: {', '.join(bulunanlar['Başlık'].values)}")

        
        tum_turler = []
        for tur_satiri in bulunanlar['Türler']:
           
            turler = [t.strip() for t in tur_satiri.split(',')]
            tum_turler.extend(turler)

        if not tum_turler:
            print("Tür bilgisi alınamadı.")
            return

        
        from collections import Counter
        en_cok_izlenen_tur = Counter(tum_turler).most_common(1)[0][0]
        
        print(f"\n💡 Analiz: **{en_cok_izlenen_tur}** türünü sevdiğinizi fark ettik.")
        print(f"🎬 Sizin için {en_cok_izlenen_tur} türünde seçtiğimiz öneriler:")

       
        oneriler = self.df[
            (self.df['Türler'].str.contains(en_cok_izlenen_tur, case=False, na=False)) &
            (~self.df['Başlık'].str.lower().isin(kullanici_listesi))
        ].sort_values(by='Puan', ascending=False)

        self.listele(oneriler.head(5))

    def calistir(self):
        print("\n" + "="*40)
        print("   FİLM & DİZİ ÖNERİ SİSTEMİ   ")
        print("="*40)
        
        while True:
            print("\n[1] Puan ile Ara")
            print("[2] Yıl ile Ara")
            print("[3] Kategori (Tür) ile Ara")
            print("[4] İzleme Geçmişine Göre Öneri Al")
            print("[5] Çıkış")
            
            secim = input("Seçiminiz: ")
            
            if secim == '1':
                self.puan_ile_ara()
            elif secim == '2':
                self.yil_ile_ara()
            elif secim == '3':
                self.kategori_ile_ara()
            elif secim == '4':
                self.gecmis_ve_oneri()
            elif secim == '5':
                print("Çıkış yapılıyor. İyi seyirler!")
                break
            else:
                print("Geçersiz seçim, tekrar deneyin.")

if __name__ == "__main__":
   
    program_dizini = os.path.dirname(os.path.abspath(__file__))
    
    
    csv_yolu = os.path.join(program_dizini, "movies.csv")
    
    app = FilmOneriSistemi(csv_yolu)
    app.calistir()