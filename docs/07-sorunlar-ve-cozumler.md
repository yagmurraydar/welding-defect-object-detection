# 07 — Karşılaşılan Sorunlar ve Çözümler

Bu belge geliştirme sırasında karşılaşılan teknik sorunları, nedenlerini ve uygulanan çözümleri kaydeder. Terminaldeki küçük yazım/sözdizimi sorunları ile veri/model açısından önemli sorunlar birbirinden ayrılmıştır.

## 1. Karışık anotasyon biçimleri

**Belirti:** Bazı etiket satırlarında 5 değer, bazılarında ise çok sayıda koordinat değeri bulunması.

**Neden:** Veri dışa aktarımında Detection bounding box satırları ve polygon anotasyonları bir arada bulunuyordu.

**Çözüm:** Polygon koordinatlarından min/max X/Y sınırları hesaplanarak çevreleyen bounding box üretildi. Orijinal veri seti korunarak ayrı Detection kopyası oluşturuldu.

## 2. Polygon doğrulayıcısının 5 sütunlu satırları hatalı sayması

**Belirti:** Polygon-only kontrolünde 1.888 hatalı satır sonucu.

**Neden:** İlk kontrol betiği bütün satırların polygon olmasını bekliyordu; ancak geçerli beş sütunlu Detection satırları da vardı.

**Çözüm:** İki biçimi de tanıyan kontrol geliştirildi. Sonraki doğrulama bütün dönüştürülmüş satırların beş sütunlu olmasını kontrol etti.

## 3. PowerShell komutlarının birleşmesi

**Belirti:** `else is not recognized`, `Unexpected token 'in'`, `Empty pipe element` veya `Missing property name` gibi hatalar.

**Neden:** Çok satırlı `if/else`, `foreach` ve pipeline komutlarının ayrı ayrı gönderilmesi ya da iki komutun aynı satıra birleşmesi.

**Çözüm:** İlgili kod blokları tek parça olarak gönderildi. Gerekli durumlarda önce sonuç bir değişkene atanıp sonra `Format-Table` ile gösterildi.

**Öğrenilen:** PowerShell'de blok yapıları (`if/else`, `foreach`) ve bunlara bağlı pipeline ifadeleri bütün olarak çalıştırılmalıdır.

## 4. `Copy-Item -File` parametresi

**Belirti:** `A parameter cannot be found that matches parameter name 'File'`.

**Neden:** `-File`, `Get-ChildItem` parametresidir; `Copy-Item` için geçerli değildir.

**Çözüm:** Dosyalar `Get-ChildItem -File` ile seçilip `Copy-Item` komutuna aktarılmıştır. Sonrasında 3.031 train, 421 valid ve 205 test görüntüsünün kopyalandığı doğrulanmıştır.

## 5. PowerShell değişkeninin null olması

**Belirti:** `$workspacePath` veya `$originalFile` için `path is null` hatası.

**Neden:** PowerShell oturumu yenilendiğinde önceki oturumda tanımlı değişkenler kaybolur veya değişken atama komutu başka bir komutla birleşerek çalışmaz.

**Çözüm:** Mutlak klasör yolu değişkene yeniden atanmış veya doğrudan `-LiteralPath` ile kullanılmıştır.

**Öğrenilen:** Önemli komutlar için yerel değişkenlerin o oturumda tanımlı olduğu doğrulanmalıdır. Uzun vadeli Python betiklerinde sabit ve kişiye özel mutlak yollar yerine yapılandırılabilir göreli yollar tercih edilmelidir.

## 6. Polygon → Bounding Box dönüşümünden doğan tekrarlar

**Belirti:** Ultralytics valid taramasında `duplicate labels removed` uyarıları.

**Analiz:** 3.657 etiket dosyasının tümü tarandı. 42 dosyada 80 tekrar grubu ve toplam 82 fazla satır bulundu. Orijinal anotasyonlarda birebir tekrar yoktu; 82 fazla satırın tamamı farklı polygon'ların aynı kutuya dönüşmesinden kaynaklandı.

**Çözüm:** Dönüştürülmüş veri setinde yalnızca birebir aynı satırların fazlası temizlendi. Önce etiket yedeği alındı. Orijinal Roboflow dosyaları değiştirilmedi.

## 7. İlk eğitim testinde düşük metrikler

**Belirti:** Smoke test Precision 0.343, Recall 0.0196, mAP50 0.00482 ve mAP50-95 0.00183.

**Neden / yorum:** Yalnızca yaklaşık 61 train görüntüsü ve tek epoch kullanıldı. Bu metrikler nihai performans için yeterli değildir.

**Çözüm:** Sonuçlar model başarısı olarak yorumlanmadı. Önce veri temizliği tamamlandı; tam eğitim ve sistematik değerlendirme sonraki aşamaya bırakıldı.

## 8. GitHub'a taşırken dikkat edilecek yol sorunu

**Durum:** Bazı geliştirme betiklerinde `C:\Users\<username>\...` biçiminde yerel mutlak yollar kullanılmıştır.

**Risk:** Bu yollar başka bilgisayarda çalışmaz ve kişisel kullanıcı klasör yapısını açığa çıkarabilir.

**Çözüm:** GitHub'a yüklemeden önce veri kökü komut satırı argümanı, ayar dosyası veya depo dışı yerel konfigürasyon üzerinden alınmalıdır. Veri seti ve sanal ortam depoya eklenmemelidir.

## 9. Henüz çözülmesi gereken teknik/araştırma konuları

- Altı örnek görüntüde kutular çizdirildi; ancak bütün etiketlerin kusurları doğru kapsadığı sistematik olarak incelenmedi.
- Polygon'dan kutuya dönüşümün ince çatlaklar ve çok yakın kusurlar üzerindeki bilgi kaybı değerlendirilmelidir.
- Aynı kaynak parçalarından türetilmiş görsellerin train/valid/test arasında veri sızıntısı oluşturup oluşturmadığı kontrol edilmelidir.
- `Good Welding` sınıfının proje kapsamındaki yeri danışmanla netleştirilmelidir.
- Smoke test sırasında `val=False` verilmesine rağmen doğrulama çıktısı üretilmesi, Ultralytics 8.4.215 davranışıyla ilgili tekrar incelenmelidir.
