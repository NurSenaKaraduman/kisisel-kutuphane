import sqlite3
from pathlib import Path

# Veritabanı dosyası, bu Python dosyasıyla aynı klasörde oluşur.
VERITABANI = Path(__file__).parent / "kutuphane.db"
#Bu Python dosyasının bulunduğu klasördeki kutuphane.db dosyasının adresini oluştur ve VERITABANI değişkeninde tut.”

def main():
    baglanti = sqlite3.connect(VERITABANI)

    try:
        # Tablo yoksa oluştur; varsa mevcut kitapları koru.
        baglanti.execute("""
            CREATE TABLE IF NOT EXISTS kitaplar (
                id INTEGER PRIMARY KEY,
                kitap_adi TEXT NOT NULL,
                yazar TEXT NOT NULL,
                durum TEXT NOT NULL DEFAULT 'Okunmadı'
                    CHECK (
                        durum IN (
                            'Okundu',
                            'Okunmadı',
                            'Okunuyor',
                            'Yarıda bırakıldı'
                        )
                    ),
                UNIQUE (kitap_adi, yazar)
            )
        """)

        ilk_kitaplar = [
            ("Cesur Yeni Dünya", "Aldous Huxley", "Okundu"),
            ("Veba", "Albert Camus", "Okundu"),
            ("Yabancı", "Albert Camus", "Okundu"),
            ("Düşüş", "Albert Camus", "Okundu"),
            ("Olağanüstü Bir Gece", "Stefan Zweig", "Okundu"),
            ("Satranç", "Stefan Zweig", "Okundu"),
            ("Kendime Düşünceler", "Marcus Aurelius", "Okundu"),
            ("Doğum Lekesi", "Nathaniel Hawthorne", "Okundu"),
            ("Candide ya da İyimserlik", "Voltaire", "Okundu"),
            ("Dönüştüren Zihin", "Joseph Murphy", "Okundu"),
            ("Seyahatname’den Seçmeler", "Evliya Çelebi", "Okundu"),
            ("Düşündüğün Gibi Değil", "Joseph Nguyen", "Okundu"),
            ("Kumarbaz", "Fyodor Dostoyevski", "Okundu"),
            ("Beyaz Geceler", "Fyodor Dostoyevski", "Okundu"),
            ("Köleler Adası", "Pierre de Marivaux", "Okundu"),
            ("Nasıl Ölünür", "Émile Zola", "Okundu"),
            ("Önemsiz Bir Kadın", "Oscar Wilde", "Okundu"),
            ("Devlet", "Platon", "Okundu"),
            ("Üç Ölüm", "Lev Tolstoy", "Okundu"),
            ("İtiraflarım", "Lev Tolstoy", "Okundu"),
            ("Dönüşüm", "Franz Kafka", "Okundu"),
            ("Toprak Ana", "Cengiz Aytmatov", "Okundu"),
            ("Bir İdam Mahkûmunun Son Günü", "Victor Hugo", "Okundu"),
            ("Genç Werther’in Istırapları", "Johann Wolfgang von Goethe", "Okundu"),
            ("Yeraltından Notlar", "Fyodor Dostoyevski", "Okundu"),
            ("Goriot Baba", "Honoré de Balzac", "Yarıda bırakıldı"),
            ("Mutlu Olma Sanatı", "Arthur Schopenhauer", "Okunmadı"),
            ("Nutuk", "Mustafa Kemal Atatürk", "Okunmadı"),
            ("Eylül", "Mehmet Rauf", "Okunmadı"),
            ("Felâtun Bey ile Râkım Efendi", "Ahmet Mithat Efendi", "Okunmadı"),
            ("Sergüzeşt", "Samipaşazade Sezai", "Okunmadı"),
            ("Vatan Yahut Silistre", "Namık Kemal", "Okunmadı"),
            ("Mahalle Kahvesi", "Sait Faik Abasıyanık", "Okunmadı"),
            ("Sen Varsın Gecede", "Cemal Süreyya", "Okunmadı"),
            ("Tutunamayanlar", "Oğuz Atay", "Okunmadı"),
            ("Hiçbir Karşılaşma Tesadüf Değildir", "Hakan Mengüç", "Okunmadı"),
            ("Her Şey Zihinde Başlar", "Jack Addington", "Okunmadı"),
            ("İrade Terbiyesi", "Jules Payot", "Okunmadı"),
            ("Ateşten Gömlek", "Halide Edib Adıvar", "Okunmadı"),
            ("İnsancıklar", "Fyodor Dostoyevski", "Okunmadı"),
            ("Babalar ve Oğullar", "İvan Turgenyev", "Okunmadı"),
            ("Vadideki Zambak", "Honoré de Balzac", "Okunmadı"),
            ("Mutlu Olma sanatı", "Arthur Schopenhauer", "Okunmadı"),
            ("İdeal Devlet", "Fârâbî", "Okunmadı"),
            ("Mutluluğun Kazanılması", "Fârâbî", "Okunmadı"),
            ("İvan İlyiç’in Ölümü", "Lev Tolstoy", "Okunmadı"),
            ("İtiraflarım", "Jean-Jacques Rousseau", "Okunmadı"),
            ("Dorian Gray’in Portresi", "Oscar Wilde", "Okunmadı"),
            ("Dr. Jekyll ve Bay Hyde’ın Tuhaf Hikâyesi", "Robert Louis Stevenson", "Okunmadı"),
            ("Ermiş", "Halil Cibran", "Okunmadı"),
            ("Babaya Mektup", "Franz Kafka", "Okunmadı"),
            ("Uğultulu Tepeler", "Emily Brontë", "Okunmadı"),
            ("Dava", "Franz Kafka", "Okunmadı"),
            ("Aforizmalar", "Franz Kafka", "Okunmadı"),
            ("Savaş ve Barış", "Lev Tolstoy", "Okunmadı"),
            ("Düşünme ve Konuşma Özgürlüğü", "John Bagnell Bury", "Okunmadı"),
            ("Tavuk Suyuna Çorba", "Jack Canfield", "Okunmadı"),
            ("Kendine Ait Bir Oda", "Virginia Woolf", "Okunmadı"),
            ("Cinsellik Üzerine", "Sigmund Freud", "Okunmadı"),
            ("Dora", "Sigmund Freud", "Okunmadı"),
            ("Kış Masalı", "William Shakespeare", "Okunmadı"),
            ("Julius Caesar", "William Shakespeare", "Okunmadı"),
            ("Hamlet", "William Shakespeare", "Okunmadı"),
            ("Romeo ve Juliet", "William Shakespeare", "Okunmadı"),
            ("Venedik Taciri", "William Shakespeare", "Okunmadı"),
            ("Bir Yaz Gecesi Rüyası", "William Shakespeare", "Okunmadı"),
            ("Martin Eden", "Jack London", "Okunmadı"),
            ("Kadınlar Ülkesi", "Charlotte Perkins Gilman", "Okunmadı"),
            ("Bulantı", "Jean-Paul Sartre", "Okunmadı"),
            ("Bilinmeyen Bir Kadının Mektubu", "Stefan Zweig", "Okunmadı"),
            ("İnsan Nedir?", "Mark Twain", "Okunmadı"),
            ("Prens", "Niccolò Machiavelli", "Okunmadı"),
            ("Siddhartha", "Hermann Hesse", "Okunmadı"),
            ("İnsanlığımı Yitirirken", "Osamu Dazai", "Okunmadı"),
            ("Kürk Mantolu Madonna", "Sabahattin Ali", "Okunmadı"),
            ("Biz", "Yevgeni Zamyatin", "Okunmadı"),
            ("1984", "George Orwell", "Okunmadı"),
            ("Beş Çember Kitabı", "Miyamoto Musashi", "Okunmadı"),
            ("On İki Öğrenci", "Sakae Tsuboi", "Okunmadı"),

            ("The Sphinx Without a Secret / The Young King", "Oscar Wilde", "Okunmadı"),
            ("A New England Nun", "Mary E. Wilkins Freeman", "Okunmadı"),
            ("Silas Marner", "George Eliot", "Okunmadı"),
            ("A Midsummer Night’s Dream", "William Shakespeare", "Okunmadı"),
        ]

        # İlk kurulum dışında False olarak kalacak.
        ILK_AKTARIM = False

        if ILK_AKTARIM:
            baglanti.executemany("""
                INSERT INTO kitaplar (kitap_adi, yazar, durum)
                VALUES (?, ?, ?)
                ON CONFLICT (kitap_adi, yazar) DO NOTHING
            """, ilk_kitaplar)

            baglanti.commit()
            print("Başlangıç kitapları aktarıldı.")

        sonuc = baglanti.execute("""
    SELECT kitap_adi, yazar, durum
    FROM kitaplar
    ORDER BY kitap_adi ASC
""")

        while True:
            print("\nSENA'NIN KÜTÜPHANESİ")
            print("1 - Tüm kitaplar")
            print("2 - Okunan kitaplar")
            print("3 - Okunmayan kitaplar")
            print("4 - Okunuyor")
            print("5 - Yarıda bırakılan kitaplar")
            print("6 - Kitap ekle")
            print("0 - Çıkış")

            secim = input("Seçimin: ").strip()

            if secim == "0":
                print("Görüşürüz Sena!")
                break

            if secim == "6":
                kitap_adi = input("Kitap adı: ").strip()
                yazar = input("Yazar: ").strip()

                if not kitap_adi or not yazar:
                    print("Kitap adı ve yazar boş bırakılamaz.")
                    continue

                print("\n1 - Okundu")
                print("2 - Okunmadı")
                print("3 - Okunuyor")
                print("4 - Yarıda bırakıldı")

                durum_secimi = input("Kitabın durumu: ").strip()

                ekleme_durumlari = {
                    "1": "Okundu",
                    "2": "Okunmadı",
                    "3": "Okunuyor",
                    "4": "Yarıda bırakıldı"
                }

                if durum_secimi not in ekleme_durumlari:
                    print("Geçersiz durum seçimi. Kitap eklenmedi.")
                    continue

                durum = ekleme_durumlari[durum_secimi]

                sonuc = baglanti.execute("""
                    INSERT INTO kitaplar (kitap_adi, yazar, durum)
                    VALUES (?, ?, ?)
                    ON CONFLICT (kitap_adi, yazar) DO NOTHING
                """, (kitap_adi, yazar, durum))

                baglanti.commit()

                if sonuc.rowcount == 1:
                    print(f"Kitap eklendi: {kitap_adi}")
                else:
                    print("Bu kitap adı ve yazar zaten kayıtlı.")

                continue

            if secim == "1":
                kitaplar = baglanti.execute("""
                    SELECT kitap_adi, yazar, durum
                    FROM kitaplar
                    ORDER BY kitap_adi ASC
                """).fetchall()

            elif secim in ("2", "3", "4", "5"):
                durumlar = {
                    "2": "Okundu",
                    "3": "Okunmadı",
                    "4": "Okunuyor",
                    "5": "Yarıda bırakıldı"
                }

                secilen_durum = durumlar[secim]

                kitaplar = baglanti.execute("""
                    SELECT kitap_adi, yazar, durum
                    FROM kitaplar
                    WHERE durum = ?
                    ORDER BY kitap_adi ASC
                """, (secilen_durum,)).fetchall()

            else:
                print("Lütfen menüdeki numaralardan birini gir.")
                continue

            print()

            if not kitaplar:
                print("Bu durumda kayıtlı kitap yok.")
            else:
                for kitap_adi, yazar, durum in kitaplar:
                    print(f"{kitap_adi} — {yazar} | {durum}")

            print(f"\nListelenen kitap sayısı: {len(kitaplar)}")

    finally:
        baglanti.close()


if __name__ == "__main__":
    main()