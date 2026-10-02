from fastapi.responses import FileResponse
import sqlite3
from pathlib import Path
import os
import cachecontrol
import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(title="Benim Kütüphanem")

VERITABANI = Path(__file__).parent / "kutuphane.db"
# Kimlik doğrulama ve yönetici yetkisi sunucuda kontrol edilir.
# Authentication and administrator permissions are checked on the server.
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "sena-kutuphane")
ADMIN_UIDS = set(filter(None, (uid.strip() for uid in os.environ.get(
    "KUTUPHANE_ADMIN_UIDS", ""
).split(","))))
izinli_adresler = list(filter(None, (adres.strip() for adres in os.environ.get(
    "KUTUPHANE_ALLOWED_ORIGINS", ""
).split(","))))
if izinli_adresler:
    app.add_middleware(
        CORSMiddleware, allow_origins=izinli_adresler,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

guvenlik = HTTPBearer(auto_error=False)
# Google imza sertifikalarını önbelleğe al.
# Cache Google's signing certificates.
token_istegi = Request(session=cachecontrol.CacheControl(requests.Session()))


def kullanici_kontrol(
    kimlik: HTTPAuthorizationCredentials | None = Depends(guvenlik)
):
    if kimlik is None:
        raise HTTPException(status_code=401, detail="Giriş yapmalısın.")
    try:
        kullanici = id_token.verify_firebase_token(
            kimlik.credentials, token_istegi, audience=FIREBASE_PROJECT_ID
        )
        if kullanici.get("iss") != f"https://securetoken.google.com/{FIREBASE_PROJECT_ID}":
            raise ValueError("Yanlış token kaynağı.")
        uid = kullanici.get("sub")
        if not isinstance(uid, str) or not uid or len(uid) > 128:
            raise ValueError("Geçersiz kullanıcı kimliği.")
        return kullanici
    except ValueError:
        raise HTTPException(status_code=401, detail="Oturum geçersiz. Yeniden giriş yap.")
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Giriş doğrulama servisine ulaşılamadı.")


def yonetici_kontrol(kullanici: dict = Depends(kullanici_kontrol)):
    if kullanici["sub"] not in ADMIN_UIDS:
        raise HTTPException(status_code=403, detail="Bu işlem için yönetici yetkisi gerekli.")
    return kullanici


@app.get("/oturum")
def oturum(kullanici: dict = Depends(kullanici_kontrol)):
    return {"uid": kullanici["sub"], "yonetici": kullanici["sub"] in ADMIN_UIDS}

@app.get(
    "/yonetici-kontrol",
    dependencies=[Depends(yonetici_kontrol)]
)
def yonetici_dogrula():
    return {"mesaj": "Yönetici girişi başarılı."}
 
@app.get("/kitaplar")
def kitaplari_getir():
    # Dosya yanlış yerdeyse boş bir veritabanı oluşturmamak
    if not VERITABANI.is_file():
        raise RuntimeError("kutuphane.db dosyası bulunamadı.")

    baglanti = sqlite3.connect(VERITABANI)
    baglanti.row_factory = sqlite3.Row

    try:
        kitaplar = baglanti.execute("""
            SELECT id, kitap_adi, yazar, durum
            FROM kitaplar
            ORDER BY kitap_adi ASC
        """).fetchall()

        return [dict(kitap) for kitap in kitaplar]

    finally:
        baglanti.close()

@app.get("/")
def ana_sayfa():
    dosya = Path(__file__).parent / "index.html"
    return FileResponse(dosya)

class DurumGuncelleme(BaseModel):
    durum: Literal[
        "Okundu",
        "Okunmadı",
        "Okunuyor",
        "Yarıda bırakıldı"
    ]


@app.patch(
    "/kitaplar/{kitap_id}/durum",
    dependencies=[Depends(yonetici_kontrol)]
)
def durum_guncelle(kitap_id: int, veri: DurumGuncelleme):
    if not VERITABANI.is_file():
        raise HTTPException(
            status_code=500,
            detail="Veritabanı bulunamadı."
        )

    baglanti = sqlite3.connect(VERITABANI)

    try:
        sonuc = baglanti.execute("""
            UPDATE kitaplar
            SET durum = ?
            WHERE id = ?
        """, (veri.durum, kitap_id))

        if sonuc.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Kitap bulunamadı."
            )

        baglanti.commit()

        return {
            "id": kitap_id,
            "durum": veri.durum,
            "mesaj": "Durum kaydedildi."
        }

    finally:
        baglanti.close()

class KitapEkleme(BaseModel):
    kitap_adi: str = Field(min_length=1, max_length=300)
    yazar: str = Field(min_length=1, max_length=200)
    durum: Literal[
        "Okundu",
        "Okunmadı",
        "Okunuyor",
        "Yarıda bırakıldı"
    ]


@app.post(
    "/kitaplar",
    status_code=201,
    dependencies=[Depends(yonetici_kontrol)]
)
def kitap_ekle(veri: KitapEkleme):
    kitap_adi = veri.kitap_adi.strip()
    yazar = veri.yazar.strip()

    if not kitap_adi or not yazar:
        raise HTTPException(
            status_code=422,
            detail="Kitap adı ve yazar boş bırakılamaz."
        )

    if not VERITABANI.is_file():
        raise HTTPException(
            status_code=500,
            detail="Veritabanı bulunamadı."
        )

    baglanti = sqlite3.connect(VERITABANI)

    try:
        sonuc = baglanti.execute("""
            INSERT INTO kitaplar (kitap_adi, yazar, durum)
            VALUES (?, ?, ?)
            ON CONFLICT (kitap_adi, yazar) DO NOTHING
        """, (kitap_adi, yazar, veri.durum))

        if sonuc.rowcount == 0:
            raise HTTPException(
                status_code=409,
                detail="Bu kitap adı ve yazar zaten kayıtlı."
            )

        baglanti.commit()

        return {
            "id": sonuc.lastrowid,
            "kitap_adi": kitap_adi,
            "yazar": yazar,
            "durum": veri.durum
        }

    finally:
        baglanti.close()

class KitapDuzenleme(BaseModel):
    kitap_adi: str = Field(min_length=1, max_length=300)
    yazar: str = Field(min_length=1, max_length=200)


@app.patch(
    "/kitaplar/{kitap_id}",
    dependencies=[Depends(yonetici_kontrol)]
)
def kitap_duzenle(kitap_id: int, veri: KitapDuzenleme):
    kitap_adi = veri.kitap_adi.strip()
    yazar = veri.yazar.strip()

    if not kitap_adi or not yazar:
        raise HTTPException(
            status_code=422,
            detail="Kitap adı ve yazar boş bırakılamaz."
        )

    if not VERITABANI.is_file():
        raise HTTPException(
            status_code=500,
            detail="Veritabanı bulunamadı."
        )

    baglanti = sqlite3.connect(VERITABANI)

    try:
        sonuc = baglanti.execute("""
            UPDATE kitaplar
            SET kitap_adi = ?, yazar = ?
            WHERE id = ?
        """, (kitap_adi, yazar, kitap_id))

        if sonuc.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Kitap bulunamadı."
            )

        baglanti.commit()

        return {
            "id": kitap_id,
            "kitap_adi": kitap_adi,
            "yazar": yazar
        }

    except sqlite3.IntegrityError:
        baglanti.rollback()

        raise HTTPException(
            status_code=409,
            detail="Bu kitap adı ve yazar zaten kayıtlı."
        )

    finally:
        baglanti.close()

@app.delete(
    "/kitaplar/{kitap_id}",
    dependencies=[Depends(yonetici_kontrol)]
)
def kitap_sil(kitap_id: int):
    if not VERITABANI.is_file():
        raise HTTPException(
            status_code=500,
            detail="Veritabanı bulunamadı."
        )

    baglanti = sqlite3.connect(VERITABANI)

    try:
        sonuc = baglanti.execute("""
            DELETE FROM kitaplar
            WHERE id = ?
        """, (kitap_id,))

        if sonuc.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Kitap bulunamadı."
            )

        baglanti.commit()

        return {"mesaj": "Kitap silindi.", "id": kitap_id}

    finally:
        baglanti.close()