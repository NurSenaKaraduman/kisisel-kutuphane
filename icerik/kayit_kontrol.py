import sqlite3
from datetime import datetime
from pathlib import Path

KLASOR = Path(__file__).parent
VERITABANI = KLASOR / "kutuphane.db"

if not VERITABANI.is_file():
    raise FileNotFoundError("kutuphane.db bulunamadı.")

zaman = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
yedek_yolu = KLASOR / f"kutuphane_yedek_{zaman}.db"

baglanti = sqlite3.connect(VERITABANI)

try:
    # Silmeden önce veritabanının yedeğini oluştur.
    yedek = sqlite3.connect(yedek_yolu)

    try:
        baglanti.backup(yedek)
    finally:
        yedek.close()

    print(f"Yedek oluşturuldu: {yedek_yolu.name}")

    # Kimliğin yanında ad ve yazarı da kontrol ederek sil.
    silinecekler = [
        (44, "Mutlu Olma sanatı", "Arthur Schopenhauer"),
        (5, "Yeraltından Notlar", "Fyodor Dosteyevski"),
    ]

    sonuc = baglanti.executemany("""
        DELETE FROM kitaplar
        WHERE id = ? AND kitap_adi = ? AND yazar = ?
    """, silinecekler)

    baglanti.commit()

    print(f"Silinen tekrar sayısı: {sonuc.rowcount}")

    toplam = baglanti.execute("""
        SELECT COUNT(*) FROM kitaplar
    """).fetchone()[0]

    print(f"Kalan kitap sayısı: {toplam}")

finally:
    baglanti.close()