# 01 — Proje Amacı ve Kapsamı

## 1. Problem tanımı

Kaynaklı imalat süreçlerinde kaynak dikişlerinin görsel olarak incelenmesi kalite kontrolün bir parçasıdır. Görüntülerde çatlak, gözeneklilik veya kaynak sıçrantısı gibi kusurların tespit edilmesi zaman ve uzman değerlendirmesi gerektirebilir.

Bu bitirme projesinde, kaynak görüntülerini analiz ederek belirlenmiş kaynak kalite kategorilerini ve kusurlarını görüntü üzerinde konumlandırabilen bir bilgisayarlı görü modeli geliştirilmesi hedeflenmektedir.

## 2. Projenin ana hedefleri

### Hedef A — Kusur tespiti

Bir kaynak görüntüsünde yer alan nesnelerin/kusurların sınıfını ve konumunu tespit etmek. Çıktı, sınıf adı, güven skoru ve bounding box koordinatlarını içerecektir.

### Hedef B — Çıkarım hızının değerlendirilmesi

Eğitilmiş modelin tek görüntü veya görüntü grubu üzerinde tahmin süresi ölçülecek; uygun model dışa aktarma veya çalışma zamanı optimizasyonları denenerek başlangıç modeliyle karşılaştırılacaktır.

## 3. Mevcut veri sınıfları

1. Bad Welding
2. Crack
3. Excess Reinforcement
4. Good Welding
5. Porosity
6. Spatters

Bu sınıf listesi seçilen Roboflow veri setinin anotasyonlarından gelmektedir. `Good Welding` normal/iyi kaynak sınıfıdır; kusur sınıfı değildir. Proje kapsamındaki rolü danışman öğretim üyesiyle netleştirilmelidir. Veri setinde şu anda ayrı `burn-through`, `dust/contamination` gibi sınıflar bulunmamaktadır. Bu nedenle veri setinde olmayan kusurların tespit edildiği iddia edilmeyecektir.

## 4. Araştırma soruları

- YOLO26n, seçilen veri setinde altı anotasyon sınıfını ne ölçüde tespit edebilmektedir?
- Sınıf dengesizliği, özellikle az örnekli sınıfların Precision, Recall ve mAP değerlerini nasıl etkilemektedir?
- Modelin CPU üzerindeki çıkarım süresi nedir?
- ONNX veya OpenVINO gibi alternatif çıkarım yolları aynı modelin performans/hız dengesini nasıl değiştirmektedir?

## 5. Kapsam dışı / henüz doğrulanmamış iddialar

- Gerçek zamanlı üretim hattı performansı henüz ölçülmemiştir.
- Endüstriyel kamera, aydınlatma ve üretim hattı koşullarında saha doğrulaması henüz yapılmamıştır.
- Veri setinde bulunmayan kusur türleri için model başarısı iddia edilmeyecektir.
- Tam eğitim ve nihai test sonuçları henüz mevcut değildir.

## 6. Başarı ölçütleri

Tespit başarısı için en az aşağıdaki ölçütler raporlanacaktır:

- Precision
- Recall
- mAP@0.50
- mAP@0.50:0.95
- Sınıf bazlı Precision / Recall / AP

Hız için ölçümler aynı donanım, aynı görüntü boyutu, aynı batch büyüklüğü ve aynı test görüntüleriyle yapılmalıdır. Ön işleme, model inference ve son işleme süreleri mümkün olduğunda ayrı raporlanmalıdır.

## 7. Mevcut durum

Veri seti hazırlanmış, etiket formatı dönüştürülmüş ve doğrulanmıştır. YOLO26n üzerinde yalnızca eğitim akışını kontrol etmek amacıyla küçük bir smoke test yapılmıştır. Tam model eğitimi ve hız optimizasyonu sonraki aşamalardır.
