# 05 — Geliştirme Ortamı ve Teknoloji Seçimleri

## 1. Geliştirme bilgisayarı

| Bileşen | Bilgi |
|---|---|
| İşletim sistemi | Windows 11 |
| İşlemci | 11. Nesil Intel Core i5-1135G7 @ 2.40 GHz |
| Kullanılabilir RAM | 7,80 GB |
| Grafik | Intel Iris Xe Graphics |
| Eğitim aygıtı | CPU |

Mevcut PyTorch kurulumu CPU sürümüdür (`+cpu`). Çalışma sırasında `torch.cuda.is_available()` sonucu `False` olarak alınmıştır. Bu, NVIDIA CUDA kullanılmadığı anlamına gelir; tek başına Intel iGPU üzerinde başka hızlandırma yöntemlerinin gelecekte değerlendirilemeyeceği anlamına gelmez.

## 2. Python ve paketler

| Teknoloji | Sürüm / durum | Neden kullanılıyor? |
|---|---|---|
| Python | 3.14.3 | Veri işleme ve eğitim betikleri |
| pip | 26.3 | Python paket yönetimi |
| PyTorch | 2.15.0+cpu | Derin öğrenme hesaplamaları |
| TorchVision | 0.29.2+cpu | Bilgisayarlı görü yardımcı bileşenleri |
| Ultralytics | 8.4.215 | YOLO model yükleme, eğitim, doğrulama ve dışa aktarma |
| Pillow | 12.2.0 varsayılan `python` ile kontrol edildi; `.venv` içindeki varlığı ayrıca doğrulanmalı | Görüntü açma ve anotasyon görselleştirme |

Sürümler, geliştirme sırasında terminal çıktılarında görülen değerlerdir. Pillow kontrolü `python -c "from PIL import Image; ..."` komutuyla varsayılan Python yorumlayıcısında yapılmıştır; bunun proje `.venv` ortamı olduğu doğrulanmamıştır. Smoke testte Pillow kullanılmadığından bu durum eğitim testini etkilememiştir. Herkese açık depoda tekrarlanabilirlik için bağımlılıkları kesin sürümlerle sabitlemek ve temiz sanal ortamda yeniden kurulum testi yapmak gerekir.

## 3. Sanal ortam

Eğitim için diğer Python projelerinden bağımsız bir sanal ortam oluşturulmuştur:

```text
Weld quality inspection.training/.venv/
```

Sanal ortamın amacı, bu proje için gereken paketleri sistem Python'ından ve diğer projelerden ayırmaktır.

Temel kurulum komutları:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -U ultralytics
```

## 4. PyTorch kontrolü

Sanal ortam içinde aşağıdaki kontrol yapılmıştır:

```powershell
.\.venv\Scripts\python.exe -c "import torch, torchvision; print(torch.__version__); print(torchvision.__version__); print(torch.cuda.is_available()); print(torch.rand(2, 3))"
```

Sonuç:

```text
PyTorch: 2.15.0+cpu
TorchVision: 0.29.2+cpu
CUDA: False
CPU tensor işlemi başarılı
```

## 5. Neden YOLO26n?

YOLO26 ailesinin `n` (nano) ölçeği, sınırlı RAM ve CPU kaynaklarında ilk deney için küçük bir model seçeneği olarak tercih edilmiştir. Amaç nihai modelin kesinlikle bu olacağına karar vermek değil, kaynak kısıtlı bilgisayarda makul bir başlangıç yapmaktır.

Önceden eğitilmiş ağırlıklar `yolo26n.pt` adıyla indirilmiştir. İlk model özeti:

```text
260 layers
2,572,280 parameters
6.2 GFLOPs
```

Altı sınıfla eğitim mimarisi oluşturulurken modelin sınıf çıkışı 80'den 6'ya uyarlanmıştır. Smoke test sırasında uyarlanmış model özeti yaklaşık 2,506,140 parametre ve 5.9 GFLOPs olarak raporlanmıştır. Farklı özetlerin modelin farklı yapılandırma/aşama bilgilerini yansıttığı unutulmamalıdır.

## 6. Hızlandırma planı

Başlangıç ölçümü CPU üzerinde yapılacaktır. Daha sonra aynı ağırlıklar ve aynı test girdileriyle ONNX Runtime veya OpenVINO gibi çıkarım seçenekleri araştırılacaktır. Her optimizasyon için doğruluk kaybı ve gecikme birlikte karşılaştırılmalıdır.

OpenVINO henüz kurulmamış ve denenmemiştir. Intel Iris Xe üzerinde hızlanma elde edileceği şimdiden varsayılmamalıdır; ölçüm sonucu belirleyici olacaktır.
