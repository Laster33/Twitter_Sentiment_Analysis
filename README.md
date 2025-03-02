```markdown
# Twitter Duygu Analizi Aracı

Python tabanlı bu araç, Twitter verileri üzerinde Doğal Dil İşleme (NLP) kullanarak duygu analizi yapar ve görselleştirmeler oluşturur.

![Duygu Analizi Sonuç Örneği](https://github.com/Laster33/Twitter_Sentiment_Analysis/blob/main/sentiment_analysis_results.png?raw=true)

## Özellikler

- 🧠 NLTK'nın VADER (Valence Aware Dictionary and sEntiment Reasoner) ile duygu analizi
- 📊 Otomatik 4 farklı görselleştirme:
  - Duygu dağılımı pasta grafiği
  - Duygu sayıları çubuk grafiği
  - Bileşik skor dağılım histogramı
  - Ortalama duygu bileşen skorları
- 📥 CSV giriş/çıkış desteği
- 📈 Detaylı duygu skorlaması (bileşik, pozitif, nötr, negatif)
- 📋 Otomatik duygu sınıflandırması (pozitif/nötr/negatif)
- 🚀 Analiz sırasında ilerleme takibi

## Gereksinimler

- Python 3.x
- pandas
- nltk
- matplotlib
- seaborn

## Kurulum

1. Depoyu klonlayın:
```bash
git clone https://github.com/kullaniciadiniz/twitter-duygu-analizi.git
cd twitter-duygu-analizi
```

2. Gerekli paketleri yükleyin:
```bash
pip install pandas nltk matplotlib seaborn
```

3. NLTK VADER sözlüğünü indirin:
```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

## Kullanım

### Temel Komut Satırı Kullanımı
```bash
python tweet_sentiment.py <giris_csv_dosyasi> [metin_sutun_adi]
```

- `giris_csv_dosyasi`: Tweetlerin bulunduğu CSV dosyasının yolu (zorunlu)
- `metin_sutun_adi`: Metin içeren sütunun adı (varsayılan: 'text')

Örnekler:
```bash
python tweet_sentiment.py data.csv
python tweet_sentiment.py data.csv text
```

### Çıktılar
Betik şunları oluşturacak:
1. `_with_sentiment` ekli yeni bir CSV dosyası:
   - Orijinal veri
   - 4 yeni sütun: `compound`, `positive`, `neutral`, `negative`
   - `sentiment` sınıflandırma sütunu
2. Görselleştirmeleri içeren `sentiment_analysis_results.png`

### Programatik Kullanım
```python
from tweet_sentiment import analyze_tweet_sentiment, visualize_sentiment

# Tweetleri analiz et
df = analyze_tweet_sentiment("tweetler.csv", text_column="text")

# Görselleştirmeleri oluştur
if df is not None:
    visualize_sentiment(df)
```

## Duygu Sınıflandırma Kriterleri
- **Pozitif**: Bileşik skor ≥ 0.05
- **Nötr**: Bileşik skor -0.05 ile 0.05 arası
- **Negatif**: Bileşik skor ≤ -0.05
