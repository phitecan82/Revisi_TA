from typing import ClassVar, cast
from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from osm_field.fields import LatitudeField, LongitudeField, OSMField


class Lokasi_aset(models.Model):
    id_lokasi = models.CharField(max_length=2,primary_key=True)
    nama_lokasi = models.CharField(max_length=50)
    alamat = models.CharField(max_length=50)
    def __str__(self):
        return self.nama_lokasi

class Kode_kelompok(models.Model):
    id_kelompok = models.CharField(max_length=5,primary_key=True)
    nama_kelompok = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_kode_kelompok

class Ruangan(models.Model):
    id_ruang = models.CharField(max_length=5,primary_key=True)
    nama_ruang = models.CharField(max_length=50)
    id_kelompok = models.ForeignKey(Kode_kelompok,on_delete=models.CASCADE)
    id_lokasi = models.ForeignKey(Lokasi_aset,on_delete=models.CASCADE)

    def __str__(self):
        return self.nama_ruang


class Klasifikasi_aset(models.Model):
    id_klasifikasi = models.CharField(max_length=2,primary_key=True)
    nama_klasifikasi = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_klasifikasi
class Jenis_aset(models.Model):
    id_jenis = models.CharField(max_length=3,primary_key=True)
    id_klasifikasi = models.ForeignKey(
        Klasifikasi_aset,
        on_delete=models.CASCADE,
    )
    nama_jenis = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_jenis
class Aset(models.Model):
    id_aset = models.BigAutoField(primary_key=True,default=None)
    id_jenis = models.ForeignKey(
        Jenis_aset,
        on_delete=models.CASCADE)
    BKR = (
        ('B','Baik'),
        ('KB','Kurang Baik'),
        ('RB','Rusak Berat')
    )
    status_aset = models.CharField(max_length=2, choices=BKR,default='B')
    id_ruangan = models.ForeignKey(
        Ruangan,
        on_delete=CASCADE
    )  

    nama_aset = models.CharField(max_length=50)
    no = models.IntegerField()
    no_register = models.CharField(max_length=20)
    tahun_perolehan = models.IntegerField()
    harga = models.IntegerField()
    asal_usul = models.CharField(max_length=50)
    keterangan = models.TextField()

    class Meta:
        # db_table = 'riwayat_pendidikan'
        unique_together = (("id_jenis","id_ruangan","tahun_perolehan","no"),)

    def __str__(self):
        return self.nama_aset
class Kiba(models.Model):
    id_aset = models.OneToOneField(
        Aset,
        on_delete=models.CASCADE,primary_key=True,related_name='kiba')
    luas = models.FloatField(max_length=10)
    hak_tanah = models.CharField(max_length=50)
    tanggal_sertifikat = models.DateField(null=True)
    no_sertifikat = models.CharField(max_length=50)
    penggunaan = models.CharField(max_length=50)

class Kibb(models.Model):
    id_aset = models.OneToOneField(
        Aset,
        on_delete=models.CASCADE,primary_key=True,related_name='kibb')

    merek = models.CharField(max_length=100)
    ukuran = models.CharField(max_length=50)
    bahan = models.CharField(max_length=50)
    no_pabrik = models.CharField(max_length=50)
    no_rangka = models.CharField(max_length=50)
    no_mesin = models.CharField(max_length=50)
    no_polisi = models.CharField(max_length=30)
    no_bpkb = models.CharField(max_length=30)

class Kibc(models.Model):
    id_aset = models.OneToOneField(
        Aset,
        on_delete=models.CASCADE,primary_key=True,related_name='kibc')

    kontruksi_bertingkat = models.BooleanField()
    kontruksi_beton = models.BooleanField()
    luas_lantai = models.FloatField(max_length=10)
    tanggal_dokumen_gedung = models.DateField(null=True)
    no_dokumen_gedung = models.CharField(max_length=40)
    luas = models.FloatField(max_length=10)
    status_tanah = models.CharField(max_length=50)
    no_kode_tanah = models.CharField(max_length=50)
class Kibd(models.Model):
    id_aset = models.OneToOneField(
        Aset,
        on_delete=models.CASCADE,primary_key=True,related_name='kibd')  

    judul_buku = models.CharField(max_length=50)
    spesifikasi_buku = models.CharField(max_length=50)
    asal_daerah_kesenian = models.CharField(max_length=50)
    pencipta_kesenian = models.CharField(max_length=50)
    bahan_kesenian = models.CharField(max_length=70)
    jenis_hewan = models.CharField(max_length=50)
    ukuran_hewan = models.IntegerField()
    jumlah_hewan = models.IntegerField()
    tahun_cetak = models.IntegerField()
# Create your models here.
