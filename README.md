# Türk Seçmen Personaları Analiz Uygulaması

Bu uygulama, Türk seçmenlerinin farklı demografik ve psikografik özelliklerini analiz eden, görselleştiren ve yapay zeka destekli görsel oluşturma özellikleri sunan bir Streamlit uygulamasıdır.

## Özellikler

- 4 farklı seçmen personanın detaylı analizi
- Demografik ve psikografik metriklerin görselleştirilmesi
- Seçim geçmişi ve trend analizleri
- Yapay zeka destekli persona görseli oluşturma
- Karşılaştırmalı analiz araçları

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/barancanercan/turk-secmen-personalari.git
cd turk-secmen-personalari
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

4. API anahtarlarını ayarlayın:
- `.streamlit/secrets.toml` dosyasını oluşturun
- Gerekli API anahtarlarını ekleyin:
```toml
GOOGLE_API_KEY = "your-google-api-key"
HUGGINGFACE_API_KEY = "your-huggingface-api-key"
```

## Kullanım

Uygulamayı başlatmak için:
```bash
streamlit run app.py
```

Uygulama http://localhost:8501 adresinde çalışacaktır.

## Persona Tipleri

1. **Geleneksel Muhafazakar Çekirdek**
   - Değerlerine bağlı, sadık seçmen
   - Dindar ve muhafazakar değerlere sahip
   - Anadolu'da yaşayan orta yaş ve üzeri kadınlar

2. **Kentli Laik Modernler**
   - Eğitimli, eleştirel düşünür
   - Modern ve laik değerlere sahip
   - Büyükşehirlerde yaşayan genç-orta yaş grubu

3. **Ekonomik Kaygılı Milliyetçiler**
   - Ulusal değerlere bağlı, ekonomi odaklı
   - Ekonomik kaygıları yüksek
   - Milliyetçi değerlere sahip

4. **Kararsız ve Sisteme Mesafeli Gençler**
   - Gelecek kaygılı, sistem eleştirisi
   - Ekonomik sıkıntılar ve gelecek endişesi
   - Sisteme mesafeli genç kesim

## Teknolojiler

- Python 3.12
- Streamlit
- Plotly
- Google Gemini API
- Hugging Face API

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## İletişim

Baran Can Ercan - [@barancanercan](https://github.com/barancanercan)

Proje Linki: [https://github.com/barancanercan/turk-secmen-personalari](https://github.com/barancanercan/turk-secmen-personalari) 