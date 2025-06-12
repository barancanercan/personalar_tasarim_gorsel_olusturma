# Türk Seçmen Personaları Analiz Platformu

![Proje Banner](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/persona_profil_fotoğrafları/banner.png)

Bu proje, Türk seçmenlerinin farklı profillerini analiz eden ve görselleştiren interaktif bir web uygulamasıdır. Kümeleme analizi sonucunda ortaya çıkan dört belirgin seçmen profili üzerine odaklanmaktadır. Modern ve kullanıcı dostu arayüzü ile seçmen profillerini detaylı bir şekilde incelemenize olanak sağlar.

## 🌟 Öne Çıkan Özellikler

- **Persona Kartları**: Her bir seçmen profili için detaylı bilgi kartları
- **Analizler**: Seçmen profillerinin metriklerini görselleştiren analiz araçları
- **PersonaGPT**: Seçilen persona ile sohbet etme imkanı
- **Sesli Sohbet**: Metin ve sesli sohbet seçenekleri
- **Detaylı Metrikler**: Sosyal medya kullanımı, politik ilgi, ekonomik endişe ve kültürel değerler üzerine analizler

## 👥 Seçmen Personaları

### 1. Geleneksel Muhafazakar Çekirdek
![Geleneksel Muhafazakar Çekirdek](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/persona_profil_fotoğrafları/geleneksel_muhafazakar_cekirdek.png)

**Demografik Özellikler:**
- 61 yaşında, evli, 4 kişilik aile
- Ortaokul mezunu
- Ev hanımı
- Düşük gelir seviyesi
- Anadolu'da yaşayan

**Değerler ve İnançlar:**
- Sünni, Hanefi İslam geleneğine bağlı
- Yüksek dindarlık endeksi
- Milliyetçi ve muhafazakar değerlere sahip
- Güçlü parti bağlılığı
- Lider odaklı siyasi yaklaşım

**Sosyal Medya Kullanımı:**
- Facebook
- TikTok
- WhatsApp

### 2. Kentli Laik Modernler
![Kentli Laik Modernler](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/persona_profil_fotoğrafları/kentli_laik_modernler.png)

**Demografik Özellikler:**
- 35-45 yaş arası
- Yüksek eğitim seviyesi
- Büyükşehirlerde yaşayan
- Orta-üst gelir seviyesi
- Aktif çalışan

**Değerler ve İnançlar:**
- Laik ve modern değerlere sahip
- Eleştirel düşünce yapısı
- Demokratik değerlere bağlı
- Çevre ve insan hakları hassasiyeti
- Sivil toplum örgütlerine aktif katılım

### 3. Ekonomik Kaygılı Milliyetçiler
![Ekonomik Kaygılı Milliyetçiler](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/persona_profil_fotoğrafları/ekonomik_kaygili_milliyetciler.png)

**Demografik Özellikler:**
- 40-55 yaş arası
- Orta eğitim seviyesi
- Esnaf/serbest meslek
- Orta gelir seviyesi
- Anadolu'da yaşayan

**Değerler ve İnançlar:**
- Ulusal değerlere bağlı
- Ekonomik kaygıları yüksek
- Devletçi yaklaşım
- Güçlü aile bağları
- Geleneksel değerlere saygılı

### 4. Kararsız ve Sisteme Mesafeli Gençler
![Kararsız ve Sisteme Mesafeli Gençler](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/persona_profil_fotoğrafları/kararsiz_ve_sisteme_mesafeli_gencler.png)

**Demografik Özellikler:**
- 18-30 yaş arası
- Üniversite öğrencisi/mezunu
- Büyükşehirlerde yaşayan
- Düşük-orta gelir seviyesi
- İş arayan/geçici işlerde çalışan

**Değerler ve İnançlar:**
- Sisteme mesafeli
- Gelecek kaygısı yüksek
- Ekonomik sıkıntılar
- Sosyal medya bağımlılığı
- Politik kararsızlık

## 🛠️ Teknik Özellikler

### Frontend
- **Streamlit**: Modern ve interaktif web arayüzü
- **Plotly**: Gelişmiş veri görselleştirme
- **Custom CSS**: Özelleştirilmiş tasarım ve animasyonlar

### Backend
- **Python**: Ana programlama dili
- **Google Gemini API**: Yapay zeka entegrasyonu
- **gTTS**: Metin-ses dönüşümü
- **SpeechRecognition**: Ses tanıma

### Veri Analizi
- **Pandas**: Veri manipülasyonu
- **NumPy**: Matematiksel işlemler
- **Plotly**: İnteraktif grafikler

## 🚀 Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. `.env` dosyası oluşturun ve gerekli API anahtarlarını ekleyin:
```
GEMINI_API_KEY=your_gemini_api_key
```

3. Uygulamayı başlatın:
```bash
streamlit run app.py
```

## 📊 Kullanım

1. Sol menüden bir modül seçin:
   - PersonaGPT: Persona ile sohbet
   - Analizler: Seçmen profillerinin analizi
   - Persona Kartları: Detaylı persona bilgileri

2. Persona seçin ve analiz türünü belirleyin:
   - Genel Bakış
   - Detaylı Analiz
   - Karşılaştırma

3. PersonaGPT'de:
   - Yazılı veya sesli sohbet seçeneğini kullanın
   - Persona ile etkileşime geçin
   - Yanıtları sesli olarak dinleyin

## 📱 Ekran Görüntüleri

### Persona Kartları
![Persona Kartları](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/screenshots/persona_cards.png)

### Analizler
![Analizler](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/screenshots/analytics.png)

### PersonaGPT
![PersonaGPT](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/screenshots/personagpt.png)

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 👨‍💻 İletişim

Baran Can Ercan - [@barancanercan](https://github.com/barancanercan)

Proje Linki: [https://github.com/barancanercan/personalar_tasarim_gorsel_olusturma](https://github.com/barancanercan/personalar_tasarim_gorsel_olusturma)

# Persona Kartı Uygulaması

Bu uygulama, seçilen persona ile etkileşimli bir sohbet deneyimi sunar ve metin-konuşma dönüşümü için Google Cloud TTS kullanır.

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

2. Google Cloud TTS Kurulumu:
   - [Google Cloud Console](https://console.cloud.google.com)'a gidin
   - Yeni bir proje oluşturun veya mevcut bir projeyi seçin
   - Cloud Text-to-Speech API'yi etkinleştirin
   - Servis hesabı oluşturun:
     - "IAM ve Yönetim" > "Servis Hesapları" bölümüne gidin
     - "Servis Hesabı Oluştur" butonuna tıklayın
     - Servis hesabına "Cloud Text-to-Speech API Kullanıcısı" rolünü atayın
     - JSON anahtar dosyasını indirin
   - İndirilen JSON anahtar dosyasını güvenli bir konuma kaydedin
   - Aşağıdaki ortam değişkenini ayarlayın:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
     ```

3. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

## Özellikler

- Persona seçimi ve etkileşimli sohbet
- Google Cloud TTS ile yüksek kaliteli ses sentezi
- Türkçe dil desteği
- Farklı persona sesleri

## Persona Sesleri

Uygulama aşağıdaki persona seslerini destekler:
- Hatice Teyze: tr-TR-Wavenet-A (Kadın sesi)
- Kenan Bey: tr-TR-Wavenet-B (Erkek sesi)
- Tuğrul Bey: tr-TR-Wavenet-C (Erkek sesi)
- Elif: tr-TR-Wavenet-D (Kadın sesi)
- Koray: tr-TR-Wavenet-E (Erkek sesi)

## Notlar

- Google Cloud TTS ücretsiz katmanı ayda 1-4 milyon karakter içerir
- Ses kalitesi WaveNet teknolojisi ile optimize edilmiştir
- Tüm sesler Türkçe dil desteğine sahiptir 