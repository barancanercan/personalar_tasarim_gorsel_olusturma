# Türk Seçmen Personaları Analiz Platformu

Bu proje, Türk seçmenlerinin farklı profillerini analiz eden ve görselleştiren interaktif bir web uygulamasıdır. Kümeleme analizi sonucunda ortaya çıkan dört belirgin seçmen profili üzerine odaklanmaktadır. Modern ve kullanıcı dostu arayüzü ile seçmen profillerini detaylı bir şekilde incelemenize olanak sağlar.

## 🌟 Öne Çıkan Özellikler

- **Persona Kartları**: Her bir seçmen profili için detaylı bilgi kartları
- **Analizler**: Seçmen profillerinin metriklerini görselleştiren analiz araçları
- **PersonaGPT**: Seçilen persona ile sohbet etme imkanı
- **Sesli Sohbet**: Metin ve sesli sohbet seçenekleri
- **Detaylı Metrikler**: Sosyal medya kullanımı, politik ilgi, ekonomik endişe ve kültürel değerler üzerine analizler
- **Konuşma İndirme**: PersonaGPT sohbetlerini metin dosyası olarak indirme özelliği
- **Responsive Tasarım**: Tüm ekran boyutlarına uyumlu modern arayüz

## 👥 Seçmen Personaları

### 1. Geleneksel Muhafazakar Çekirdek (Hatice Teyze)
![Hatice Teyze](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/persona_profil_fotograflari/hatice_teyze.jpg)

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

### 2. Kentli Laik Modernler (Kenan Bey)
![Kenan Bey](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/persona_profil_fotograflari/kenan_bey.jpg)

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

### 3. Ekonomik Kaygılı Milliyetçiler (Tuğrul Bey)
![Tuğrul Bey](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/persona_profil_fotograflari/tugrul_bey.jpg)

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

### 4. Kararsız ve Sisteme Mesafeli Gençler (Elif)
![Elif](https://raw.githubusercontent.com/barancanercan/personalar_tasarim_gorsel_olusturma/main/persona_profil_fotograflari/elif.jpg)

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
- **Responsive Layout**: Container-based responsive tasarım

### Backend
- **Python**: Ana programlama dili
- **Google Gemini API**: Yapay zeka entegrasyonu
- **gTTS**: Metin-ses dönüşümü
- **SpeechRecognition**: Ses tanıma
- **Streamlit Chat**: Gelişmiş sohbet arayüzü

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
   - Persona Kartları: Detaylı persona bilgileri

2. PersonaGPT'de:
   - Yazılı veya sesli sohbet seçeneğini kullanın
   - Persona ile etkileşime geçin
   - Yanıtları sesli olarak dinleyin
   - Konuşma geçmişini indirin

3. Persona Kartlarında:
   - Detaylı persona bilgilerini görüntüleyin
   - Profil fotoğraflarını inceleyin
   - Biyografi, lore ve diğer detayları okuyun

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

Canlı Demo: [https://personagorsellestirme.streamlit.app/](https://personagorsellestirme.streamlit.app/) 