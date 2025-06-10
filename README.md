# Türk Seçmen Personaları Analizi ve Görsel Oluşturma

Bu proje, Türk toplumundaki seçmen profillerini analiz eden ve yapay zeka destekli görsel oluşturma özelliği sunan interaktif bir Streamlit uygulamasıdır.

## Özellikler

- **Dört Farklı Seçmen Profili Analizi**
  - Geleneksel Muhafazakar Çekirdek
  - Kentli Laik Modernler
  - Ekonomik Kaygılı Milliyetçiler
  - Kararsız ve Sisteme Mesafeli Gençler

- **Detaylı Analiz Araçları**
  - Genel Bakış
  - Detaylı Analiz
  - Karşılaştırmalı Analiz
  - Metrik ve Trend Görselleştirmeleri

- **Yapay Zeka Destekli Görsel Oluşturma**
  - Google Gemini API entegrasyonu
  - Her persona için özelleştirilmiş görsel üretimi
  - Modern ve kullanıcı dostu arayüz

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/barancanercan/personalar_tasarim_gorsel_olusturma.git
cd personalar_tasarim_gorsel_olusturma
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac için
# veya
.\venv\Scripts\activate  # Windows için
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

## Kullanım

1. Sol menüden analiz türünü seçin:
   - Genel Bakış
   - Detaylı Analiz
   - Karşılaştırma

2. Persona Görsel Oluşturucu modülünü kullanmak için:
   - Sol menüden "Persona Görsel Oluşturucu"yü seçin
   - Persona seçin
   - "Görsel Oluştur" butonuna tıklayın

## Teknolojiler

- Streamlit
- Plotly
- Pandas
- Google Gemini AI
- Python 3.8+

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: X'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## İletişim

Baran Can Ercan - [@barancanercan](https://github.com/barancanercan)

Proje Linki: [https://github.com/barancanercan/personalar_tasarim_gorsel_olusturma](https://github.com/barancanercan/personalar_tasarim_gorsel_olusturma) 