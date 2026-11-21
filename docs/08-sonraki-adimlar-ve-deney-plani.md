# 08 — Sonraki Adımlar ve Deney Planı

## Mevcut durum

- Veri hazırlama, format dönüşümü, tekrar temizliği ve son biçimsel doğrulama tamamlandı.
- PyTorch ve Ultralytics ortamı kuruldu.
- YOLO26n ağırlıkları yüklendi.
- Bir epoch ve train verisinin %2'siyle smoke test başarıyla çalıştı.
- **Tam eğitim henüz yapılmadı.**

## Aşama 1 — Eğitim öncesi son hazırlık

1. Bounding box'ların kusurları doğru kapsayıp kapsamadığını daha fazla örnek üzerinde görsel olarak kontrol et.
2. Özellikle Crack, Porosity ve küçük Spatters kutularını incele.
3. Aynı fiziksel kaynak görüntüsünden üretilmiş kırpımların farklı veri bölümlerine dağılmadığını kontrol et. Kaynak görüntü seviyesinde veri sızıntısı varsa bölme stratejisini düzelt.
4. `Good Welding` sınıfının dahil edilmesi konusunu danışmanla netleştir.
5. YOLO26n, giriş boyutu, batch, epoch ve erken durdurma ayarlarını bilgisayarın RAM/CPU kapasitesine göre belirle.

## Aşama 2 — Temel model eğitimi

İlk tam deney, temizlenmiş veri setiyle YOLO26n kullanılarak yapılacaktır. Eğitim parametreleri deney başlamadan önce kaydedilmelidir:

- model ağırlığı ve sürümü
- `imgsz`
- `batch`
- `epochs`
- `workers`
- optimizer ve learning rate ayarları
- random seed
- kullanılan veri seti sürümü ve etiket temizliği

Sınırlı donanım nedeniyle eğitim küçük bir ayarla başlatılmalı ve RAM/disk/CPU tüketimi izlenmelidir. Gerekirse `imgsz` veya batch düşürülebilir; ancak küçük kusurların görünürlüğüne etkisi dikkate alınmalıdır.

## Aşama 3 — Model değerlendirmesi

Validation ve test sonuçları birbirine karıştırılmamalıdır:

- Validation: eğitim/hiperparametre seçimi sırasında izleme.
- Test: model seçimi tamamlandıktan sonra nihai ve mümkün olduğunca tek seferlik değerlendirme.

Raporlanacak metrikler:

- Precision
- Recall
- mAP50
- mAP50-95
- Sınıf bazlı AP ve Recall
- Confusion matrix ve PR eğrileri (mevcutsa)

Sınıf dengesizliği nedeniyle yalnızca genel ortalama metrik verilmemelidir.

## Aşama 4 — Hız ölçümü

Aynı donanım ve aynı test görüntüleriyle ölçüm yap. Modeli önceden ısıt (warm-up), tekrar sayısını ve ölçülen görüntü sayısını kaydet. Ön işleme, inference ve post-processing sürelerini mümkün olduğunca ayrı raporla.

İlk smoke testteki 18,3 ms/görüntü değeri, 320 giriş boyutundaki tek kısa deneyin logundan alınmıştır; nihai benchmark değildir ve farklı deneylerle doğrudan karşılaştırılmamalıdır.

## Aşama 5 — Optimizasyon deneyleri

Aday yöntemler:

- ONNX dışa aktarma ve uygun runtime ile CPU inference
- OpenVINO dışa aktarma/çalıştırma ve Intel donanımında ölçüm
- Gerekirse quantization (ör. INT8) ve doğruluk kaybının ölçülmesi
- Gerekirse daha küçük giriş boyutu veya farklı model ölçeği

Her optimizasyonda aynı test kümesi, aynı ölçüm prosedürü ve aynı güven eşiği kullanılmalıdır. Hız kazanımı tek başına yeterli değildir; mAP/Recall kaybı da raporlanmalıdır.

## Aşama 6 — Deney sonuçlarının raporlanması

Önerilen karşılaştırma tablosu:

| Deney | Model / Runtime | Image size | Precision | Recall | mAP50 | mAP50-95 | Latency (ms) | FPS |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | YOLO26n / PyTorch CPU | | | | | | | |
| Optimize 1 | ONNX Runtime | | | | | | | |
| Optimize 2 | OpenVINO | | | | | | | |

Boş hücreler deneyler yapıldıkça doldurulmalıdır; ölçülmemiş değerler tahmin edilmemelidir.

## Akademik rapor için ek notlar

- Veri kaynağı ve CC BY 4.0 atfı eklenmelidir.
- Polygon→Bounding Box dönüşümünün sınırlılıkları açıklanmalıdır.
- Sınıf dengesizliği tartışılmalıdır.
- Smoke test metrikleri tam eğitim sonucu gibi gösterilmemelidir.
- Gerçek zamanlılık iddiası yalnızca ölçümle desteklenirse kullanılmalıdır.
