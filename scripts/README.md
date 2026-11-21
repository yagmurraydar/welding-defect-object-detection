

\# Scripts — Veri Hazırlama ve Eğitim Araçları



Bu klasör, kaynak kalite kontrolü projesinde kullanılan veri hazırlama, anotasyon dönüşümü, doğrulama ve ilk model eğitim denemesi betiklerini içerir.



\## 1. Betiklerin listesi



| Dosya | Görevi |

|---|---|

| `convert\_to\_detection.py` | Polygon anotasyonlarını YOLO Bounding Box formatına dönüştürür. |

| `analyze\_duplicate\_collisions.py` | Polygon dönüşümünden kaynaklanan aynı Bounding Box çakışmalarını analiz eder. |

| `deduplicate\_detection\_labels.py` | Birebir aynı etiket satırlarını güvenli şekilde temizler. |

| `preview\_labels.py` | Bounding Box etiketlerini görüntüler üzerine çizer. |

| `validate\_detection\_dataset.py` | Görüntü-etiquet eşleşmesini, sınıf ID'lerini ve koordinatları kontrol eder. |

| `smoke\_test.py` | YOLO eğitim altyapısını küçük bir veri örneğiyle test eder. |



\## 2. Kullanılan ortam



Geliştirme sırasında kullanılan ortam:



\- Python 3.14.3

\- PyTorch 2.15.0+cpu

\- TorchVision 0.29.2+cpu

\- Ultralytics 8.4.215



Betikler, gerekli paketlerin kurulu olduğu bir Python sanal ortamıyla çalıştırılmalıdır.



`preview\_labels.py` için Pillow gereklidir. Pillow'un kullanılacak sanal ortamda kurulu olduğu ayrıca doğrulanmalıdır.



\## 3. Beklenen veri seti yapısı



Betikler veri setinin aşağıdaki yapıda olmasını bekler:



```text

dataset/

├── train/

│   ├── images/

│   └── labels/

├── valid/

│   ├── images/

│   └── labels/

├── test/

│   ├── images/

│   └── labels/

└── data.yaml

```



\## 4. Betiklerin kullanımı



Komutlarda `python` yerine gerekli paketlerin kurulu olduğu sanal ortamın Python yorumlayıcısı kullanılmalıdır.



\### 4.1. Anotasyon dönüşümü



```powershell

python scripts/convert\_to\_detection.py `

&#x20;   --source-root "PATH\_TO\_ORIGINAL\_DATASET" `

&#x20;   --output-root "PATH\_TO\_DETECTION\_DATASET"

```



Orijinal veri setindeki Polygon anotasyonlarını Bounding Box biçimine dönüştürür.



Mevcut Bounding Box etiketlerini korur. Kaynak ve hedef klasörleri birbirinden farklı olmalıdır.



\### 4.2. Dönüşüm çakışmalarını analiz etme



```powershell

python scripts/analyze\_duplicate\_collisions.py `

&#x20;   --source-root "PATH\_TO\_ORIGINAL\_DATASET" `

&#x20;   --converted-root "PATH\_TO\_DETECTION\_DATASET"

```



Farklı Polygon anotasyonlarının aynı Bounding Box'a dönüşüp dönüşmediğini inceler.



Dosyaları değiştirmez.



\### 4.3. Tekrarlı etiketleri temizleme



Önce yalnızca analiz:



```powershell

python scripts/deduplicate\_detection\_labels.py `

&#x20;   --dataset-root "PATH\_TO\_DETECTION\_DATASET" `

&#x20;   --backup-root "PATH\_TO\_LABEL\_BACKUP"

```



Gerçek temizleme için ayrıca `--apply` parametresi eklenmelidir:



```powershell

python scripts/deduplicate\_detection\_labels.py `

&#x20;   --dataset-root "PATH\_TO\_DETECTION\_DATASET" `

&#x20;   --backup-root "PATH\_TO\_LABEL\_BACKUP" `

&#x20;   --apply

```



Temizleme öncesinde etiket dosyalarının yedeğini oluşturur.



\### 4.4. Etiketleri görselleştirme



```powershell

python scripts/preview\_labels.py `

&#x20;   --dataset-root "PATH\_TO\_DETECTION\_DATASET" `

&#x20;   --output-dir "PATH\_TO\_PREVIEW"

```



Train bölümünden her sınıf için ayrı örnek görüntü oluşturur ve Bounding Box etiketlerini çizer.



\### 4.5. Veri setini doğrulama



```powershell

python scripts/validate\_detection\_dataset.py `

&#x20;   --dataset-root "PATH\_TO\_DETECTION\_DATASET"

```



Aşağıdaki kontrolleri gerçekleştirir:



\- Görüntü ve etiket dosyalarının eşleşmesi

\- Beş sütunlu YOLO Detection biçimi

\- Sınıf ID aralığı

\- Normalize koordinatlar

\- Bounding Box genişliği ve yüksekliği

\- Görüntü sınırlarının aşılmaması

\- Tekrarlı etiketler

\- Boş etiket dosyaları



\### 4.6. İlk eğitim testi



```powershell

python scripts/smoke\_test.py `

&#x20;   --dataset-root "PATH\_TO\_DETECTION\_DATASET" `

&#x20;   --weights "yolo26n.pt" `

&#x20;   --project "runs"

```



Bu betik, YOLO26n modelinin eğitim altyapısını sınırlı sayıda görüntü ve tek epoch ile test eder.



Smoke test, modelin nihai başarısını ölçmek için kullanılmaz.



\## 5. Önemli kullanım notları



\- Orijinal veri seti üzerinde doğrudan değişiklik yapılmamalıdır.

\- Dönüştürme ve temizleme işlemleri ayrı çıktı klasörlerinde gerçekleştirilmelidir.

\- Gerçek temizlik öncesinde etiket yedeği alınmalıdır.

\- Eğitim ağırlıkları ve deney çıktıları GitHub deposuna eklenmemelidir.

\- Bu betikler veri hazırlama ve ilk deney aşamasını kapsar. Tam eğitim ve performans değerlendirme kodları proje geliştikçe eklenecektir.
