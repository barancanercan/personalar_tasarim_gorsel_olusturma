# Türk Seçmen Personaları Analiz Platformu

Bu proje, Türk seçmenlerinin farklı profillerini analiz eden ve görselleştiren interaktif bir web uygulamasıdır. Kümeleme analizi sonucunda ortaya çıkan dört belirgin seçmen profili üzerine odaklanmaktadır.

## Özellikler

- **Persona Kartları**: Her bir seçmen profili için detaylı bilgi kartları
- **Analizler**: Seçmen profillerinin metriklerini görselleştiren analiz araçları
- **PersonaGPT**: Seçilen persona ile sohbet etme imkanı
- **Sesli Sohbet**: Metin ve sesli sohbet seçenekleri
- **Detaylı Metrikler**: Sosyal medya kullanımı, politik ilgi, ekonomik endişe ve kültürel değerler üzerine analizler

## Kurulum

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

## Kullanım

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

## Teknik Detaylar

- **Frontend**: Streamlit
- **Veri Görselleştirme**: Plotly
- **AI Modeli**: Google Gemini
- **Ses İşleme**: gTTS, SpeechRecognition
- **Veri İşleme**: Pandas, NumPy

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## İletişim

Baran Can Ercan - [@barancanercan](https://github.com/barancanercan)

Proje Linki: [https://github.com/barancanercan/turk-secmen-personalari](https://github.com/barancanercan/turk-secmen-personalari)

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