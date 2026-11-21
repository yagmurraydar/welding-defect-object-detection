# 02 — Veri Seti ve Kaynağı

## 1. Kaynak

- Veri seti: **Weld Quality Inspection**
- Platform: Roboflow Universe
- Sürüm: Version 9
- Görev: Object Detection
- Kaynak sayfası: https://universe.roboflow.com/welding-2bplp/weld-quality-inspection-rei9l/dataset/9
- Lisans: CC BY 4.0

Kamuya açık depoda veri setinin kendisi yerine kaynak bağlantısı, sürüm ve lisans bilgisi tutulmalıdır. Veri setini kullanan kişi Roboflow kaynağından ilgili sürümü ve kullanım koşullarını yeniden kontrol etmelidir.

## 2. Yerel indirme ve bölümler

Bilgisayara indirilen YOLOv8 biçimindeki dışa aktarımın yerel klasör sayımları:

| Bölüm | Görüntü | Etiket dosyası |
|---|---:|---:|
| Train | 3.031 | 3.031 |
| Valid | 421 | 421 |
| Test | 205 | 205 |
| **Toplam** | **3.657** | **3.657** |

Bu değerler yerel olarak indirilen ve incelenen klasörlerdeki gerçek sayımlardır. Başka bir dışa aktarım veya veri seti sürümünde sayılar farklı olabilir.

## 3. Sınıf kimlikleri

| Class ID | Sınıf adı |
|---:|---|
| 0 | Bad Welding |
| 1 | Crack |
| 2 | Excess Reinforcement |
| 3 | Good Welding |
| 4 | Porosity |
| 5 | Spatters |

`data.yaml` dosyasında `nc: 6` ve yukarıdaki sıra ile `names` tanımlıdır. Etiketlerdeki sınıf ID sırası değiştirilmemelidir.

## 4. Başlangıçtaki anotasyon biçimleri

Etiket dosyaları incelendiğinde iki farklı satır biçimi tespit edilmiştir:

- Beş değerli satır: `class_id x_center y_center width height` — YOLO Detection bounding box.
- En az yedi değerli ve tek sayıda toplam değere sahip satır: `class_id` ve ardından X/Y koordinat çiftleri — polygon anotasyonu.

Yerel dışa aktarımda sayılan satırlar:

| Bölüm | Bounding Box satırı | Polygon satırı | Toplam |
|---|---:|---:|---:|
| Train | 1.888 | 38.251 | 40.139 |
| Valid | 225 | 3.412 | 3.637 |
| Test | 110 | 971 | 1.081 |
| **Toplam** | **2.223** | **42.634** | **44.857** |

Train bölümünde 693 dosyada yalnızca kutu, 2.156 dosyada yalnızca polygon ve 182 dosyada her iki biçim de bulunmuştur. Bu sayımlar, Detection eğitimine geçmeden önce anotasyon dönüşümünü gerekli kılmıştır.

## 5. Veri setinin sınırlılıkları

- Veri setindeki sınıflar hocanın nihai olarak istediği bütün kusur türlerini kapsamayabilir.
- `Good Welding` kusur değil, olumlu/normal örnek sınıfıdır.
- Mevcut veri setinde ayrı `burn-through` veya `dust/contamination` sınıfı tespit edilmemiştir.
- Görüntülerin gerçek üretim hattındaki kamera/ışık koşullarını ne ölçüde temsil ettiği ayrıca değerlendirilmelidir.
- Görüntülerde aynı kaynak parçasından türetilmiş bloklar/benzer görüntüler bulunabilir. Train/valid/test arasında kaynak görüntü sızıntısı olup olmadığı ayrıca denetlenmelidir.

## 6. Veri seti dizinleri

Orijinal dışa aktarım:

```text
Weld quality inspection.v9i.yolov8/
├── train/images/
├── train/labels/
├── valid/images/
├── valid/labels/
├── test/images/
├── test/labels/
└── data.yaml
```

Dönüştürülmüş Detection veri seti:

```text
Weld quality inspection.detection/
├── train/images/
├── train/labels/
├── valid/images/
├── valid/labels/
├── test/images/
├── test/labels/
└── data.yaml
```

Dönüştürülmüş `data.yaml`, `train`, `valid` ve `test` görüntü yollarını ve altı sınıfı tanımlar.
