# 03 — Anotasyon Biçimi ve Polygon → Bounding Box Dönüşümü

## 1. Dönüşümün nedeni

İndirilen veri setinde hem YOLO Detection bounding box satırları hem de polygon koordinatları bulunuyordu. Projede ilk yaklaşım olarak kutu tabanlı nesne tespiti seçildiği için bütün anotasyonların Detection biçimine getirilmesi gerekiyordu.

Orijinal Roboflow dosyaları korunmuş, dönüşüm ayrı bir `Weld quality inspection.detection` klasöründe yapılmıştır.

## 2. YOLO Detection biçimi

Her etiket satırı beş alandan oluşur:

```text
class_id x_center y_center width height
```

Koordinatlar görüntü genişliği ve yüksekliğine göre normalize edilir ve normal koşullarda 0–1 aralığındadır.

## 3. Polygon'dan kutu hesaplama

Polygon satırında ilk değer sınıf kimliği, devamında X/Y koordinat çiftleri bulunur.

Önce sınırlar bulunur:

```text
x_min = min(x_coordinates)
x_max = max(x_coordinates)
y_min = min(y_coordinates)
y_max = max(y_coordinates)
```

Sonra kutu parametreleri hesaplanır:

\[
x_c = \frac{x_{min}+x_{max}}{2}, \qquad y_c = \frac{y_{min}+y_{max}}{2}
\]

\[
w = x_{max}-x_{min}, \qquad h = y_{max}-y_{min}
\]

Sınıf kimliği korunur; çıktı beş sütunlu YOLO Detection satırı olur.

## 4. Dönüşüm sayımları

| Bölüm | Korunan mevcut kutu | Polygon'dan üretilen kutu | Dönüşüm öncesi toplam satır |
|---|---:|---:|---:|
| Train | 1.888 | 38.251 | 40.139 |
| Valid | 225 | 3.412 | 3.637 |
| Test | 110 | 971 | 1.081 |
| **Toplam** | **2.223** | **42.634** | **44.857** |

## 5. Dönüşümün bilgi kaybı

Polygon anotasyonu nesnenin çevresini ayrıntılı biçimde tanımlar. Çevreleyen dikdörtgen kutu ise yalnızca en dış X/Y sınırlarını korur. Bu nedenle polygon'un şekil bilgisi kaybolur ve kutu kusurun çevresindeki sağlam görüntü alanını da kapsayabilir.

Bu konu özellikle ince/uzun çatlaklar gibi şekli önemli kusurlarda görsel olarak incelenmelidir. Detection seçimi, projenin ilk deney yaklaşımıdır; ileride segmentasyon yaklaşımıyla karşılaştırılması da değerlendirilebilir.

## 6. Dönüşüm kaynaklı kutu çakışmaları

Dönüşümden sonra aynı etiket dosyasında birebir aynı sınıf ve kutu koordinatına sahip tekrarlar tespit edilmiştir. Kaynak polygon satırları birbirinin aynısı değildir; farklı polygon'lar aynı dış sınır kutusuna dönüşmüştür.

Tüm veri setindeki inceleme:

| Bölüm | Tekrarlı dosya | Fazla satır |
|---|---:|---:|
| Train | 36 | 72 |
| Valid | 4 | 8 |
| Test | 2 | 2 |
| **Toplam** | **42** | **82** |

Ayrıntılı karşılaştırmada kaynakta birebir tekrarlı satır sayısı **0**, dönüşüm kaynaklı çakışmalardan gelen fazla satır sayısı **82** bulunmuştur. Dönüşüm uyuşmazlığı bulunan dosya sayısı **0** olarak raporlanmıştır.

### Temizlik kararı

Detection veri setinde aynı sınıf ve aynı bounding box koordinatını iki kez saklamak yeni bir konum bilgisi sağlamadığından, birebir aynı dönüştürülmüş satırların fazlası yeni veri setinden kaldırılmıştır. Orijinal veri seti değiştirilmemiştir. Temizlik öncesi dönüştürülmüş etiketler ayrı bir yedek klasörüne kopyalanmıştır.

**Metodolojik uyarı:** Farklı polygon'ların aynı kutuya dönüşmesi, iki anotasyonun gerçekten tek bir fiziksel kusuru mu yoksa çok yakın/ayrı kusurları mı temsil ettiğini tek başına kanıtlamaz. Bu yüzden bu kararın görsel incelemeyle desteklenmesi gerekir. Kutu tabanlı temsilin bu tür ayrımları kaybedebileceği raporda belirtilmelidir.

## 7. Kullanılan yerel betik

Dönüşüm sırasında `convert_to_detection.py` kullanılmıştır. Betik orijinal klasördeki etiketleri okumuş, görüntüleri yeni veri setinde tutmuş ve dönüştürülmüş etiketleri ayrı hedef dizine yazmıştır.

Betik, dönüşüm sonrasında yeniden çalıştırılırsa tekrarları yeniden üretebilir. Temizlenmiş etiketleri korumak için dönüşüm betiği üzerinde çalışırken yedekleme ve tekrar doğrulama yapılmalıdır.
