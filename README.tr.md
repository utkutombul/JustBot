# JustBot
*Diğer diller:* [English](https://github.com/utkutombul/JustBot/blob/master/README.md)

JustBot, Python programlama dili ile kolayca Discord botu yazmak isteyenlere yardımcı olmak ve bir temel oluşturmak üzere hazırlanmış yeni başlayanlara yönelik bir Discord botudur. İçerisinde SQLAlchemy ile sağlanmış basit bir veritabanı bağlantısı (SQLite, ama kolayca MySQL'e çevrilebilir), kolayca komut yazma ve Discord eventlerine örnek teşkil edecek bir temel vardır.

## Gereksinimler
Python 3.6 veya üstüne sahip (sanal olması tavsiye edilen) bir kurulum.

## Kurulum
`requirements.txt` dosyasından gerekli paketleri kurmak için pip'i kullanmalısınız.

```
pip install -r requirements.txt
```

İşlem tamamlandığında `config.py` dosyasını kendi ayarlarınız için düzenlemeyi unutmayın! Botu şu şekilde çalıştırabilirsiniz;

```
python manage.py runbot
```

## Ayarlar
JustBot tüm ayarlarınızı tek bir dosya içerisinde tutar. `config.py` dosyasından tüm değişiklikleri yapabilirsiniz.

## SSS
### Neden botun dili İngilizce?
Tüm kodlamalarımı İngilizce olarak yapıyorum. Just Roleplay Discord kanalı üzerinde kullandığım bot için hazırladığım Türkçe çeviri dosyaları mevcut, `locale/tr_TR/LC_MESSAGES` klasörü içerisinde bulabilirsiniz. Türkçe dilini aktif etmek için ise `config.py` dosyasına gidip `BOT_LANGUAGE` değişkenini `tr_TR` olarak ayarlamanız gerekli.

### Çoklu dil desteği nasıl sağlanıyor?
Çoklu dil desteği (localization) Python'un gettext kütüphaneleriyle eklenmiş durumda. Çevirileri içerisinde barındıran .po ve .mo dosyalarını oluşturmak için Babel'in extractor ve compiler'ından faydalandım. Eğer siz de kendi kodunuzu veya bota eklediklerinize dil desteği eklemek istiyorsanız aynı yolu kullanabilirsiniz.

Bunu yapabilmek için öncelikle Python kurulumunuza Babel kütüphanelerini indirmeniz gerekiyor.

```
pip install babel
```

gettext() veya _() fonksiyonu ile stringlerinizi çevirilmek üzere işaretleyebilirsiniz. Bunu yaparken önce İngilizce olarak eklemeniz, daha sonra Türkçe'ye çevirmeniz kod bütünlüğü açısından daha sağlıklı olacaktır. Sonra, kodunuz içerisindeki tüm işaretli stringleri ayıklamanız gerekiyor. 

```
pybabel extract . -o locale/base.pot
```

Eğer kodda büyük değişiklikler yaptıysanız veya temelin üzerine sıfırdan kendi komutlarınızı oluşturduysanız, herşeyi en baştan çevirmeniz en iyisi. Burada çeviri dili olarak `tr_TR` belirttim, hangi dile çevirecekseniz o dilin kodunu girmeniz gerekli.

```
pybabel init -l tr_TR -i locale/base.pot -d locale
```

Eğer büyük değişiklikler yapmadıysanız veya mevcut çevirilerin üstüne eklemek istiyorsanız, `init` argümanını `update`'e çevirmeniz gerekecek.

```
pybabel update -l tr_TR -i locale/base.pot -d locale
```

Sonra, `locale/(dil_kodu)/LC_MESSAGES` dizinine gidip `messages.pot` dosyasından çeviri yapmaya başlayabilirsiniz. Bu dosyayı herhangi bir metin editörü veya Poedit gibi bir programla açabilirsiniz, tercih sizin. Çevirilerinizi tamamladıktan sonra, compile etmeniz gerekiyor ki sistem tanıyabilsin.

```
pybabel compile -d locale
```

Başardınız! `config.py` dosyası içerisinde kullanacağınız dilin kodunu `BOT_LANGUAGE` değişkenine yazmayı unutmayın.

### Komutları nasıl çevireceğim?
Komutların bot içerisinde ayıklanması ve işlenmesi farklı olduğundan, yukarıda anlattığım yöntemin içerisinde değiller. `commands.py` dosyasına giderseniz her fonksiyonun adının aslında komut olduğunu göreceksiniz, tek yapmanız gereken fonksiyon isimlerini değiştirmek. Fonksiyon isimlerini değiştirdiğinizde başka bir yerden tanıtmanız gerekmiyor, yapmanız gereken tek değişiklik bu.