# 04 — Veri Kalitesi ve Doğrulama Kayıtları

## 1. Görüntü / etiket eşleşmesi

İlk kontrol, her görüntü dosyasının aynı ada sahip bir `.txt` etiket dosyasıyla eşleşip eşleşmediğini doğrulamıştır.

| Bölüm | Görüntü | Etiket dosyası | Eksik etiket | Karşılıksız etiket |
|---|---:|---:|---:|---:|
| Train | 3.031 | 3.031 | 0 | 0 |
| Valid | 421 | 421 | 0 | 0 |
| Test | 205 | 205 | 0 | 0 |
| **Toplam** | **3.657** | **3.657** | **0** | **0** |

## 2. Dönüşüm öncesi koordinat kontrolleri

Orijinal etiketler iki biçimde bulunduğu için ayrı format kontrolleri yazılmıştır:

- Beş sütunlu kutu satırları.
- Sınıf kimliği ve koordinat çiftlerinden oluşan polygon satırları.

Train, valid ve test bölümlerinde sınıf kimliği ve normalize koordinat kontrollerinde hata görülmemiştir.

## 3. Dönüşüm sonrası tekrar denetimi

İlk doğrulamada bütün satırların beş sütunlu olduğu, sınıf ID'sinin 0–5 aralığında bulunduğu, koordinatların 0–1 aralığında kaldığı ve kutu genişlik/yüksekliğinin pozitif olduğu doğrulanmıştır.

İlk doğrulama sonucu, temizlik öncesi:

| Bölüm | Etiket satırı | Geçersiz satır | Boş dosya | Eksik / karşılıksız dosya |
|---|---:|---:|---:|---:|
| Train | 40.139 | 0 | 0 | 0 |
| Valid | 3.637 | 0 | 0 | 0 |
| Test | 1.081 | 0 | 0 | 0 |

Daha sonra 82 birebir dönüştürülmüş kutu tekrarı bulundu ve temizlendi.

## 4. Temizlik ve son doğrulama

Temizlenen fazla satırlar:

| Bölüm | Temizlik öncesi | Temizlenen tekrar | Son durum |
|---|---:|---:|---:|
| Train | 40.139 | 72 | 40.067 |
| Valid | 3.637 | 8 | 3.629 |
| Test | 1.081 | 2 | 1.079 |
| **Toplam** | **44.857** | **82** | **44.775** |

Temizlik öncesindeki dönüştürülmüş etiketlerin yedeği:

```text
Weld quality inspection.detection_labels_backup/
├── train/labels/
├── valid/labels/
└── test/labels/
```

### Son doğrulama

`validate_detection_dataset.py` betiğiyle son durumda şu sonuçlar elde edilmiştir:

| Kontrol | Train | Valid | Test |
|---|---:|---:|---:|
| Görüntü | 3.031 | 421 | 205 |
| Etiket dosyası | 3.031 | 421 | 205 |
| Etiket satırı | 40.067 | 3.629 | 1.079 |
| Geçersiz satır | 0 | 0 | 0 |
| Tekrarlı satır | 0 | 0 | 0 |
| Boş etiket dosyası | 0 | 0 | 0 |
| Eksik etiket | 0 | 0 | 0 |
| Karşılıksız etiket | 0 | 0 | 0 |

**Sonuç:** Betiğin kontrol ettiği biçimsel veri kalitesi koşullarına göre son doğrulama başarılıdır. Bu, anotasyonların görsel olarak doğru olduğunu tek başına garanti etmez; nesne kutularının gerçek kusurları doğru kapsaması ayrıca insan tarafından incelenmelidir.

## 5. Son sınıf dağılımı

Temizlik sonrasındaki etiket sayımları:

| Sınıf | Train | Valid | Test | Toplam |
|---|---:|---:|---:|---:|
| Bad Welding | 769 | 111 | 53 | 933 |
| Crack | 700 | 94 | 67 | 861 |
| Excess Reinforcement | 3.591 | 273 | 37 | 3.901 |
| Good Welding | 1.184 | 207 | 90 | 1.481 |
| Porosity | 9.432 | 1.132 | 213 | 10.777 |
| Spatters | 24.391 | 1.812 | 619 | 26.822 |
| **Toplam** | **40.067** | **3.629** | **1.079** | **44.775** |

Sınıf dengesizliği belirgindir. Spatters toplam etiketlerin yaklaşık %60'ını, Crack ise yaklaşık %1,9'unu oluşturur. Bu nedenle genel mAP tek başına yeterli değildir; sınıf bazlı AP ve Recall sonuçları da raporlanmalıdır.

## 6. Görsel kontrol

`preview_labels.py` ile train bölümünden her sınıfı temsil eden altı örnek görüntüye bounding box ve sınıf adı çizilmiştir. Görüntüler `preview_samples/` altında oluşturulmuştur.

Bu kontrol çizim mekanizmasının çalıştığını göstermiştir. Kutu sınırlarının kusurları doğru kapsayıp kapsamadığının, özellikle Crack ve küçük Porosity/Spatters örneklerinde, sistematik insan incelemesi henüz tamamlanmamıştır.

## 7. Kontrol betikleri

- `analyze_duplicate_collisions.py` — kaynak polygon satırları ile dönüştürülmüş kutuları karşılaştırır.
- `deduplicate_detection_labels.py` — yalnızca birebir aynı dönüştürülmüş satırların fazlasını temizler ve yedek alır.
- `validate_detection_dataset.py` — son Detection etiketlerini doğrular.
