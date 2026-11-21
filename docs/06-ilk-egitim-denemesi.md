# 06 — İlk Eğitim Denemesi (Smoke Test)

## 1. Amaç

İlk denemenin amacı model başarısını ölçmek değildir. Amaç, Python sanal ortamı, PyTorch, Ultralytics, YOLO ağırlıkları ve veri setinin eğitim kodu üzerinden birlikte çalışabildiğini doğrulamaktır.

Bu nedenle yalnızca train görüntülerinin %2'siyle, tek epoch ve küçük giriş boyutuyla kısa bir test yapılmıştır.

## 2. Model yükleme

`yolo26n.pt` önceden eğitilmiş ağırlıkları Ultralytics ile yüklenmiştir. Model görevi `detect` olarak doğrulanmıştır.

Model COCO ön eğitimindeki 80 sınıftan proje veri setinin altı sınıfına uyarlanmıştır. Logda:

```text
Overriding model.yaml nc=80 with nc=6
Transferred 696/708 items from pretrained weights
```

ifadeleri görülmüştür.

## 3. Smoke test ayarları

Kullanılan `smoke_test.py` ayarları:

| Parametre | Değer |
|---|---:|
| Model | YOLO26n |
| Epoch | 1 |
| Image size | 320 |
| Batch | 1 |
| Fraction | 0.02 |
| Workers | 0 |
| Device | CPU |
| Cache | False |
| AMP | False |
| Plots | False |
| Deney adı | `smoke_test` |

Fraction 0.02 nedeniyle train bölümünden yaklaşık 61 görüntü işlenmiştir. Valid bölümünde loglar 421 görüntünün tarandığını ve son değerlendirme tablosunun üretildiğini göstermiştir.

## 4. Gözlenen çalışma sonucu

- Eğitim epoch'u tamamlanmıştır.
- Eğitim adımı yaklaşık 10,3 saniye sürmüştür.
- Eğitim ve doğrulama için ağırlık dosyaları kaydedilmiştir.
- Son logda CPU inference süresi yaklaşık 18,3 ms/görüntü olarak raporlanmıştır.
- Çıktılar `runs/smoke_test/` altında oluşturulmuştur.

Önemli dosyalar:

```text
runs/smoke_test/
└── weights/
    ├── best.pt
    └── last.pt
```

## 5. Smoke test metrikleri

Logda tüm sınıflar için özet değerler şu şekilde raporlanmıştır:

| Metrik | Değer |
|---|---:|
| Precision | 0.343 |
| Recall | 0.0196 |
| mAP50 | 0.00482 |
| mAP50-95 | 0.00183 |

Bu metrikler çok düşük ve yalnızca 61 train görüntüsü ile tek epoch kullanılmıştır. Dolayısıyla modelin nihai başarısı olarak sunulmamalıdır. Bu değerler yalnızca smoke test kayıtlarıdır.

## 6. Loglarda görülen uyarılar ve notlar

### Duplicate labels

Valid taraması sırasında bazı dosyalarda `duplicate labels removed` uyarıları görülmüştür. Daha sonra tüm veri seti incelenmiş; toplam 82 tekrarın tamamının farklı polygon'ların aynı bounding box'a dönüşmesinden kaynaklandığı belirlenmiş ve temizlenmiştir. Smoke test, temizlikten önce çalıştırılmıştır.

### `val=False` parametresine rağmen doğrulama çıktısı

Smoke test betiğinde `val=False` verilmesine rağmen logda 421 valid görüntü için değerlendirme çıktısı görülmüştür. Bu davranış Ultralytics 8.4.215 sürümünde eğitim sonu doğrulama akışı açısından ayrıca kontrol edilmelidir. Ana deneyden önce kullanılan Ultralytics sürümü ve doğrulama ayarları tekrar doğrulanmalıdır.

## 7. Sonuç

Smoke test, eğitim hattının çalıştığını ve ağırlık dosyası üretebildiğini göstermiştir. Tam eğitim, hiperparametre seçimi, güvenilir başarı ölçümü ve hız benchmark'ı henüz yapılmamıştır.
