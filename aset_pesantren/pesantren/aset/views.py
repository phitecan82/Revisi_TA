from django import conf
from django.db.models.query import QuerySet, RawQuerySet
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect,request,HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
from .utils import render_to_pdf 
from django.db.models import Count,Sum
import folium
from django.conf import settings
from django.contrib.auth.decorators import login_required


from .models import *
# Aset

class Data_asetIndexView(generic.ListView):
    model = Aset
    template_name = 'data_aset/index.html'

    def get_context_data(self, **kwargs):
        context = super(Data_asetIndexView, self).get_context_data(**kwargs)
        context['jenis_list']=Jenis_aset.objects.all()
        context['ruang']=Ruangan.objects.all()
        return context
        
@login_required(login_url=settings.LOGIN_URL)     
def deleteData(request, pk):
    data = get_object_or_404(Aset, pk=pk)
    data.delete()
    messages.warning(request, 'Data Aset Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('aset:indexData_aset'))

@login_required(login_url=settings.LOGIN_URL)
def addData(request):
    if request.method == "POST" :
        try:
            savedata = Aset(nama_aset = request.POST['nama_aset'],no=request.POST['no'],
                            no_register = request.POST['no_register'],tahun_perolehan = request.POST['tahun_perolehan'],harga = request.POST['harga'],
                            asal_usul = request.POST['asal_usul'],keterangan = request.POST['keterangan'],id_jenis_id = request.POST['id_jenis'],
                            status_aset = request.POST['status_aset'],id_ruangan_id = request.POST['id_ruangan']
                            )
            savedata.save()
            messages.success(request, 'Data Aset Sudah Berhasil di Input.', extra_tags='primary')
            return HttpResponseRedirect(reverse('aset:indexData_aset'))
        except IntegrityError:
            messages.warning(request, 'Data Aset Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('aset:indexData_aset'))
        
    else:
        return HttpResponseRedirect(reverse('aset:indexData_aset'))

@login_required(login_url=settings.LOGIN_URL)
def editData(request,pk):
    data = get_object_or_404(Aset, pk=pk)
    jenis = Jenis_aset.objects.all()
    ruangan = Ruangan.objects.all()

    if request.method == "POST" :
            try:
                tes = Jenis_aset.objects.get(pk=request.POST['id_jenis'])
                ruang = Ruangan.objects.get(pk=request.POST['id_ruangan'])
                savedata = Aset(id_aset=data.id_aset,nama_aset = request.POST['nama_aset'],no=request.POST['no'],
                                no_register = request.POST['no_register'],tahun_perolehan = request.POST['tahun_perolehan'],harga = request.POST['harga'],
                                asal_usul = request.POST['asal_usul'],keterangan = request.POST['keterangan'],id_jenis_id = tes,
                                status_aset = request.POST['status_aset'],id_ruangan_id = ruang,
                                )
                savedata.save()
                messages.success(request, 'Data Aset Sudah Berhasil Diubah.', extra_tags='primary')
                return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            except IntegrityError:
                messages.warning(request, 'Data Aset Sudah Ada.', extra_tags='danger')
                return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
    else:
        return render(request,"data_aset/edit.html",{'data':data,'jenis':jenis,'ruangan':ruangan})

@login_required(login_url=settings.LOGIN_URL)
def Data_aset_DetailView(request,pk):
    data = get_object_or_404(Aset, pk=pk)
    kiba = Kiba.objects.filter(id_aset_id=pk)
    kibb = Kibb.objects.filter(id_aset_id=pk)
    kibc = Kibc.objects.filter(id_aset_id=pk)
    kibd = Kibd.objects.filter(id_aset_id=pk)
    kelompoks= Kode_kelompok.objects.all()
    return render(request,"data_aset/detail_view.html",{'data':data,'kelompoks':kelompoks,'kiba':kiba,'kibb':kibb,'kibc':kibc,'kibd':kibd})
        
class Print_aset(generic.View):
     def get(self, request, *args, **kwargs):
        data_aset = Aset.objects.select_related('kiba','kibb','kibc','kibd')
        today = timezone.now()
        params = {
            'data_aset':data_aset,
            'today': today,
            'request': request
        }

        pdf = render_to_pdf('data_aset/pdf.html',params) #getting the template
        return HttpResponse(pdf, content_type='application/pdf')  #rendering the template

@login_required(login_url=settings.LOGIN_URL)
def Print_asett (request):
            if request.method == "POST" :
                data_aset = Aset.objects.filter(Q(id_ruangan=request.POST['id_ruangan'])).order_by('id_aset')
                kibs = Ruangan.objects.filter(Q(id_ruang=request.POST['id_ruangan']))
                today = timezone.now()
                params = {
                    'data_aset':data_aset,
                    'today': today,
                    'request': request,
                    'kibs':kibs,

                }

                pdf = render_to_pdf('data_aset/pdff.html',params) #getting the template
                return HttpResponse(pdf, content_type='application/pdf')  #rendering the


# PRINT_KIB
# PRINT_KIBA
@login_required(login_url=settings.LOGIN_URL)
def Print_kiba (request):
            if request.method == "POST" :
                kiba = Kiba.objects.filter(Q(id_aset__id_ruangan_id__id_kelompok_id=request.POST['id_kelompok'])&Q(id_aset__id_ruangan_id__id_lokasi_id=request.POST['id_lokasi'])).order_by('id_aset_id')
                kibs = Ruangan.objects.filter(Q(id_kelompok_id=request.POST['id_kelompok'])&Q(id_lokasi_id=request.POST['id_lokasi']))[:1]
                today = timezone.now()
                params = {
                    'kiba':kiba,
                    'today': today,
                    'request': request,
                    'kibs':kibs,

                }

                pdf = render_to_pdf('kiba/pdf.html',params) #getting the template
                return HttpResponse(pdf, content_type='application/pdf')  #rendering the template

@login_required(login_url=settings.LOGIN_URL)
def Print_kiba_F (request):
                kiba = Kiba.objects.all().order_by('id_aset_id')
                today = timezone.now()
                params = {
                    'kiba':kiba,
                    'today': today,
                    'request': request
                    }

                pdf = render_to_pdf('kiba/pdf_full.html',params) #getting the template
                return HttpResponse(pdf, content_type='application/pdf')  #rendering the template

#PRINT_KIBB
@login_required(login_url=settings.LOGIN_URL)
def Print_kibb (request):
            if request.method == "POST" :
                kibb = Kibb.objects.filter(Q(id_aset__id_ruangan_id__id_kelompok_id=request.POST['id_ruangan'])).order_by('id_aset_id')
                kibs = Ruangan.objects.filter(Q(id_kelompok_id=request.POST['id_ruangan']))[:1]
                today = timezone.now()
                params = {
                    'kibb':kibb,
                    'today': today,
                    'request': request,
                    'kibs':kibs,

                }

                pdf = render_to_pdf('kibb/pdf.html',params) #getting the template
                return HttpResponse(pdf, content_type='application/pdf')  #rendering the template

@login_required(login_url=settings.LOGIN_URL)
def Print_kibb_F (request):
                kibb = Kibb.objects.all().order_by('id_aset_id')
                today = timezone.now()
                params = {
                    'kibb':kibb,
                    'today': today,
                    'request': request
                    }

                pdf = render_to_pdf('kibb/pdf_full.html',params) #getting the template
                return HttpResponse(pdf, content_type='application/pdf')  #rendering the template
#PRINT_KIBC
@login_required(login_url=settings.LOGIN_URL)
def Print_kibc (request):
            if request.method == "POST" :
                kibc = Kibc.objects.filter(Q(id_aset__id_ruangan_id=request.POST['id_ruangan'])).order_by('id_aset_id')
                kibs = Ruangan.objects.filter(Q(id_ruang=request.POST['id_ruangan']))
                today = timezone.now()
                params = {
                    'kibc':kibc,
                    'today': today,
                    'request': request,
                    'kibs':kibs,

                }

                pdf = render_to_pdf('kibc/pdf.html',params) #getting the template
                return HttpResponse(pdf, content_type='application/pdf')  #rendering the template

@login_required(login_url=settings.LOGIN_URL)
def Print_kibc_F (request):
                kibc = Kibc.objects.all().order_by('id_aset_id')
                today = timezone.now()
                params = {
                    'kibc':kibc,
                    'today': today,
                    'request': request
                    }

                pdf = render_to_pdf('kibc/pdf_full.html',params) #getting the template
                return HttpResponse(pdf, content_type='application/pdf')  #rendering the template
#PRINT_KIBD
@login_required(login_url=settings.LOGIN_URL)
def Print_kibd (request):
            if request.method == "POST" :
                kibd = Kibd.objects.filter(Q(id_aset__id_ruangan_id=request.POST['id_ruangan'])).order_by('id_aset_id')
                kibs = Ruangan.objects.filter(Q(id_ruang=request.POST['id_ruangan']))
                today = timezone.now()
                params = {
                    'kibd':kibd,
                    'today': today,
                    'request': request,
                    'kibs':kibs,

                }

                pdf = render_to_pdf('kibd/pdf.html',params) #getting the template
                return HttpResponse(pdf, content_type='application/pdf')  #rendering the template

@login_required(login_url=settings.LOGIN_URL)
def Print_kibd_F (request):
                kibd = Kibd.objects.all().order_by('id_aset_id')
                today = timezone.now()
                params = {
                    'kibd':kibd,
                    'today': today,
                    'request': request
                    }

                pdf = render_to_pdf('kibd/pdf_full.html',params) #getting the template
                return HttpResponse(pdf, content_type='application/pdf')  #rendering the template
# Kartu Inventaris Aset

@login_required(login_url=settings.LOGIN_URL)
def addKiba(request):
    if request.method == "POST" :
            id_aset = Aset.objects.get(id_aset = request.POST['id_aset'])   
            
            if Kiba.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibb.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibc.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibd.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            else : 
                    id_kib = id_aset.id_aset
                    saveaset = Kiba(id_aset_id=id_kib,luas=request.POST['luas'],hak_tanah=request.POST['hak'],tanggal_sertifikat=request.POST['tgl_sertifikat'],no_sertifikat=request.POST['no_sertifikat'],penggunaan=request.POST['penggunaan'])
                    saveaset.save()
                    messages.success(request, 'KIB A Sudah Berhasil di Input.', extra_tags='primary')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            
    else:
        return HttpResponseRedirect(reverse('aset:indexData'))

@login_required(login_url=settings.LOGIN_URL)
def addKibb(request):
    if request.method == "POST" :
            id_aset = Aset.objects.get(id_aset = request.POST['id_aset'])   
            
            if Kiba.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibb.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibc.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibd.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            
            else :
                    id_kib = id_aset.id_aset
                    saveaset = Kibb(id_aset_id=id_kib   ,merek=request.POST['merek'],ukuran=request.POST['ukuran'],bahan=request.POST['bahan'],no_pabrik=request.POST['no_pabrik'],no_rangka=request.POST['no_rangka'],no_mesin=request.POST['no_mesin'],no_polisi=request.POST['no_polisi'],no_bpkb=request.POST['no_bpkb'])
                    saveaset.save()
                    messages.success(request, 'KIB B Sudah Berhasil di Input.', extra_tags='primary')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
    else:
        return HttpResponseRedirect(reverse('aset:indexData'))

@login_required(login_url=settings.LOGIN_URL)
def addKibc(request):
    if request.method == "POST" :
            id_aset = Aset.objects.get(id_aset = request.POST['id_aset'])   
            
            if Kiba.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibb.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibc.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibd.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            
            else :
                    id_kib = id_aset.id_aset
                    saveaset = Kibc(id_aset_id=id_kib,kontruksi_bertingkat=request.POST['kober'],kontruksi_beton=request.POST['kobet'],luas_lantai=request.POST['lulan'],tanggal_dokumen_gedung=request.POST['tadoge'],no_dokumen_gedung=request.POST['nodoge'],luas=request.POST['luasg'],status_tanah=request.POST['sta'],no_kode_tanah=request.POST['nokota'])
                    saveaset.save()
                    messages.success(request, 'KIB C Sudah Berhasil di Input.', extra_tags='primary')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            
    else:
        return HttpResponseRedirect(reverse('aset:indexData'))

@login_required(login_url=settings.LOGIN_URL)
def addKibd(request):
    if request.method == "POST" :
            id_aset = Aset.objects.get(id_aset = request.POST['id_aset'])   
            
            if Kiba.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibb.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibc.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            elif Kibd.objects.filter(id_aset=id_aset.id_aset).exists():
                    messages.warning(request, 'ID Aset  Sudah Ada.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
            
            else :
                    id_kib = id_aset.id_aset
                    saveaset = Kibd(id_aset_id=id_kib,judul_buku=request.POST['judul'],spesifikasi_buku=request.POST['spek'],asal_daerah_kesenian=request.POST['asdake'],pencipta_kesenian=request.POST['peke'],bahan_kesenian=request.POST['bake'],jenis_hewan=request.POST['jehe'],ukuran_hewan=request.POST['uhe'],tahun_cetak=request.POST['tacebu'],jumlah_hewan=request.POST['jumlah'])
                    saveaset.save()
                    messages.success(request, 'KIB D Sudah Berhasil di Input.', extra_tags='primary')
                    return HttpResponseRedirect(reverse('aset:detailData', args=(request.POST['id_aset'],)))
    else:
        return HttpResponseRedirect(reverse('aset:indexData'))
#KIB A
@login_required(login_url=settings.LOGIN_URL)
def KibaIndexView(request):
    object_list = Kiba.objects.all()
    kiba = Lokasi_aset.objects.all()
    kibaa = Kode_kelompok.objects.all()
    konteks = {
        'object_list': object_list,
        'kiba' :kiba,
        'kibaa':kibaa,
    }
    return render(request,"kiba/index.html",konteks)

@login_required(login_url=settings.LOGIN_URL)
def editKiba(request, pk):
    aset = Aset.objects.all()
    kiba = get_object_or_404(Kiba, pk=pk)
    if request.method == "POST" :
        tes = Aset.objects.get(pk=request.POST['id_aset'])
        kiba = Kiba(id_aset = tes,luas=request.POST['luas'],hak_tanah=request.POST['hak'],tanggal_sertifikat=request.POST['tgl_sertifikat'],no_sertifikat=request.POST['no_sertifikat'],penggunaan=request.POST['penggunaan'])
        kiba.save()
        messages.success(request, 'KIB A Sudah Berhasil Diubah.', extra_tags='primary')
        return HttpResponseRedirect(reverse('aset:indexKiba'))
    else:
        return render(request,"kiba/edit.html",{'kiba':kiba,'aset':aset})
#KIB B
@login_required(login_url=settings.LOGIN_URL)
def KibbIndexView(request):
    object_list = Kibb.objects.all()
    kiba = Ruangan.objects.all()
    kibaa = Kode_kelompok.objects.all()
    konteks = {
        'object_list': object_list,
        'kiba' :kiba,
        'kibaa':kibaa,
    }
    return render(request,"kibb/index.html",konteks)

@login_required(login_url=settings.LOGIN_URL)
def editKibb(request, pk):
    aset = Aset.objects.all()
    kibb = get_object_or_404(Kibb, pk=pk)
    if request.method == "POST" :
        tes = Aset.objects.get(pk=request.POST['id_aset'])
        kibb = Kibb(id_aset = tes,merek=request.POST['merek'],ukuran=request.POST['ukuran'],bahan=request.POST['bahan'],no_pabrik=request.POST['no_pabrik'],no_rangka=request.POST['no_rangka'],no_mesin=request.POST['no_mesin'],no_polisi=request.POST['no_polisi'],no_bpkb=request.POST['no_bpkb'])
        kibb.save()
        messages.success(request, 'KIB  Sudah Berhasil Diubah.', extra_tags='primary')
        return HttpResponseRedirect(reverse('aset:indexKibb'))
    else:
        return render(request,"kibb/edit.html",{'kibb':kibb,'aset':aset})
#KIB C
@login_required(login_url=settings.LOGIN_URL)
def KibcIndexView(request):
    object_list = Kibc.objects.all()
    kiba = Ruangan.objects.all()
    kibaa = Kode_kelompok.objects.all()
    konteks = {
        'object_list': object_list,
        'kiba' :kiba,
        'kibaa':kibaa,
    }
    return render(request,"kibc/index.html",konteks)

@login_required(login_url=settings.LOGIN_URL)
def editKibc(request, pk):
    aset = Aset.objects.all()
    kibc = get_object_or_404(Kibc, pk=pk)
    if request.method == "POST" :
        tes = Aset.objects.get(pk=request.POST['id_aset'])
        kibc = Kibc(id_aset = tes,kontruksi_bertingkat=request.POST['kober'],kontruksi_beton=request.POST['kobet'],luas_lantai=request.POST['lulan'],tanggal_dokumen_gedung=request.POST['tadoge'],no_dokumen_gedung=request.POST['nodoge'],luas=request.POST['luasg'],status_tanah=request.POST['sta'],no_kode_tanah=request.POST['nokota'])
        kibc.save()
        messages.success(request, 'KIB C Sudah Berhasil Diubah.', extra_tags='primary')
        return HttpResponseRedirect(reverse('aset:indexKibc'))
    else:
        return render(request,"kibc/edit.html",{'kibc':kibc,'aset':aset})
#KIB D
@login_required(login_url=settings.LOGIN_URL)
def KibdIndexView(request):
    object_list = Kibd.objects.all()
    kiba = Ruangan.objects.all()
    kibaa = Kode_kelompok.objects.all()
    konteks = {
        'object_list': object_list,
        'kiba' :kiba,
        'kibaa':kibaa,
    }
    return render(request,"kibd/index.html",konteks)

@login_required(login_url=settings.LOGIN_URL)
def editKibd(request, pk):
    aset = Aset.objects.all()
    kibd = get_object_or_404(Kibd, pk=pk)
    if request.method == "POST" :
        tes = Aset.objects.get(pk=request.POST['id_aset'])
        kibd = Kibd(id_aset = tes,judul_buku=request.POST['judul'],spesifikasi_buku=request.POST['spek'],asal_daerah_kesenian=request.POST['asdake'],pencipta_kesenian=request.POST['peke'],bahan_kesenian=request.POST['bake'],jenis_hewan=request.POST['jehe'],ukuran_hewan=request.POST['uhe'],tahun_cetak=request.POST['tacebu'],jumlah_hewan=request.POST['jumlah'])
        kibd.save()
        messages.success(request, 'KIB D Sudah Berhasil Diubah.', extra_tags='primary')
        return HttpResponseRedirect(reverse('aset:indexKibd'))
    else:
        return render(request,"kibd/edit.html",{'kibd':kibd,'aset':aset})

@login_required(login_url=settings.LOGIN_URL)
def Dashboard1(request):
    result = (Aset.objects
            .values('status_aset')
            .annotate(tes=Count('status_aset'))
            .order_by('status_aset'))
    ruangan = (Aset.objects
              .values('id_ruangan_id__id_kelompok_id__nama_kelompok','id_ruangan_id__id_lokasi_id__nama_lokasi','id_ruangan_id','id_ruangan_id__nama_ruang')
              .annotate(tes=Count('id_ruangan_id')).order_by('id_ruangan_id'))

    kiba = Kiba.objects.count()
    kibb = Kibb.objects.count()
    kibc = Kibc.objects.count()
    kibd = Kibd.objects.count()

    total_aset = Aset.objects.count()
    total_harga = Aset.objects.aggregate(Sum('harga'))['harga__sum']
    luas_tanah = Kiba.objects.aggregate(Sum('luas'))['luas__sum']
    luas_bangunan = Kibc.objects.aggregate(Sum('luas'))['luas__sum']
    today = timezone.now()
    konteks = {
        'result':result,
        'ruangan':ruangan,
        'kiba':kiba,
        'kibb':kibb,
        'kibc':kibc,
        'kibd':kibd,
        'total_aset' : total_aset,
        'total_harga': total_harga,
        'today':today,
        'luas_tanah':luas_tanah,
        'luas_bangunan':luas_bangunan
    }
    return render(request,"dashboard1/map.html",konteks)

# Cetak Label Aset

class Print_label(generic.View):
     def get(self, request, *args, **kwargs):
        data_aset = Aset.objects.all()
        params = {
            'data_aset':data_aset,
            'request': request
        }

        pdf = render_to_pdf('data_aset/label.html',params) #getting the template
        return HttpResponse(pdf, content_type='application/pdf')  #rendering the template




# Master Data Aset
# Jenis Aset 
class JenisIndexView(generic.ListView):
    model = Jenis_aset
    template_name = 'jenis/index.html'

    def get_context_data(self, **kwargs):
        context = super(JenisIndexView, self).get_context_data(**kwargs)
        context['klasifikasi_list'] = Klasifikasi_aset.objects.all()
        return context

@login_required(login_url=settings.LOGIN_URL)
def addJenis(request):
    if request.method == "POST" :

        id_jenis = request.POST['id_jenis']
        savejenis = Jenis_aset(id_jenis = id_jenis,nama_jenis=request.POST['nama_jenis'],id_klasifikasi_id=request.POST['id_klasifikasi'])
        
        if Jenis_aset.objects.filter(id_jenis=id_jenis).exists():
                messages.warning(request, 'ID Klasifikasi Jenis Sudah Ada.', extra_tags='danger')
                return HttpResponseRedirect(reverse('aset:indexJenis'))
        else:
            savejenis.save()
            messages.success(request, 'Jenis Aset Sudah Berhasil di Input.', extra_tags='primary')
            return HttpResponseRedirect(reverse('aset:indexJenis'))
    else:
        return HttpResponseRedirect(reverse('aset:indexJenis'))

@login_required(login_url=settings.LOGIN_URL)
def deleteJenis(request, pk):
    jenis = get_object_or_404(Jenis_aset, pk=pk)
    jenis.delete()
    messages.warning(request, 'Jenis Aset Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('aset:indexJenis'))

@login_required(login_url=settings.LOGIN_URL)
def editJenis(request, pk):
    jenis = get_object_or_404(Jenis_aset, pk=pk)
    klasifikasi = Klasifikasi_aset.objects.all()
    
    if request.method == "POST" :
        jenis.nama_jenis = request.POST['nama_jenis']
        jenis.id_klasifikasi = Klasifikasi_aset.objects.get(pk=request.POST['id_klasifikasi'])
        jenis.save()
        messages.success(request, 'Jenis Aset Sudah Berhasil Diubah.', extra_tags='primary')
        return HttpResponseRedirect(reverse('aset:indexJenis'))
    else:
        return render(request,"jenis/edit.html",{'jenis':jenis,'klasifikasi':klasifikasi})

# Klasifikasi Aset
class KlasifikasiIndexView(generic.ListView):
    model = Klasifikasi_aset
    template_name = 'klasifikasi/index.html'

@login_required(login_url=settings.LOGIN_URL)
def addKlasifikasi(request):
    if request.method == "POST" :
        id_klasifikasi = request.POST['id_klasifikasi']
        saveklasifikasi = Klasifikasi_aset(id_klasifikasi=id_klasifikasi,nama_klasifikasi=request.POST['nama_klasifikasi'])
        
        if Klasifikasi_aset.objects.filter(id_klasifikasi=id_klasifikasi).exists():
                messages.warning(request, 'ID Klasifikasi  Sudah Ada.', extra_tags='danger')
                return HttpResponseRedirect(reverse('aset:indexKlasifikasi'))
        else:
            saveklasifikasi.save()
            messages.success(request, 'Klasifikasi Aset Sudah Berhasil di Input.', extra_tags='primary')
            return HttpResponseRedirect(reverse('aset:indexKlasifikasi'))
    else:
        return HttpResponseRedirect(reverse('aset:indexKlasifikasi'))

@login_required(login_url=settings.LOGIN_URL)
def deleteKlasifikasi(request, pk):
    klasifikasi = get_object_or_404(Klasifikasi_aset, pk=pk)
    klasifikasi.delete()
    messages.warning(request, 'Klasifikasi Aset Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('aset:indexKlasifikasi'))

@login_required(login_url=settings.LOGIN_URL)      
def editKlasifikasi(request, pk):
    klasifikasi = get_object_or_404(Klasifikasi_aset, pk=pk)
    if request.method == "POST" :
        klasifikasi.nama_klasifikasi = request.POST['nama_klasifikasi']
        klasifikasi.save()
        messages.success(request, 'Klasifikasi Aset Sudah Berhasil Diubah.', extra_tags='primary')
        return HttpResponseRedirect(reverse('aset:indexKlasifikasi'))
    else:
        return render(request,"klasifikasi/edit.html",{'klasifikasi':klasifikasi})

# Lokasi Aset
class LokasiIndexView(generic.ListView):
    model = Lokasi_aset
    template_name = 'lokasi/index.html'

@login_required(login_url=settings.LOGIN_URL)
def addLokasi(request):
    if request.method == "POST" :
        id_lokasi = request.POST['id_lokasi']
        savelokasi = Lokasi_aset(id_lokasi=id_lokasi,nama_lokasi=request.POST['nama_lokasi'],alamat=request.POST['alamat'])
        
        if Lokasi_aset.objects.filter(id_lokasi=id_lokasi).exists():
                messages.warning(request, 'ID Lokasi  Sudah Ada.', extra_tags='danger')
                return HttpResponseRedirect(reverse('aset:indexLokasi'))
        else:
            savelokasi.save()
            messages.success(request, 'Lokasi Aset Sudah Berhasil di Input.', extra_tags='primary')
            return HttpResponseRedirect(reverse('aset:indexLokasi'))
    else:
        return HttpResponseRedirect(reverse('aset:indexLokasi'))

@login_required(login_url=settings.LOGIN_URL)
def deleteLokasi(request, pk):
    lokasi = get_object_or_404(Lokasi_aset, pk=pk)
    lokasi.delete()
    messages.warning(request, 'Lokasi Aset Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('aset:indexLokasi'))  

@login_required(login_url=settings.LOGIN_URL)
def editLokasi(request, pk):
    lokasi = get_object_or_404(Lokasi_aset, pk=pk)
    if request.method == "POST" :
        lokasi = Lokasi_aset(id_lokasi =lokasi.id_lokasi,nama_lokasi=request.POST['nama_lokasi'],alamat=request.POST['alamat'])
        lokasi.save()
        messages.success(request, 'Lokasi Aset Sudah Berhasil Diubah.', extra_tags='primary')
        return HttpResponseRedirect(reverse('aset:indexLokasi'))
    else:
        return render(request,"lokasi/edit.html",{'lokasi':lokasi})

# Kelompok Aset
class KelompokIndexView(generic.ListView):
    model = Kode_kelompok
    template_name = 'kelompok/index.html'

@login_required(login_url=settings.LOGIN_URL)
def addKelompok(request):
    if request.method == "POST" :
        id_kelompok = request.POST['id_kelompok']
        savekelompok = Kode_kelompok(id_kelompok=id_kelompok,nama_kelompok=request.POST['nama_kelompok'])
        
        if Kode_kelompok.objects.filter(id_kelompok=id_kelompok).exists():
                messages.warning(request, 'ID Pelaksana Kegiatan Yayasan Sudah Ada.', extra_tags='danger')
                return HttpResponseRedirect(reverse('aset:indexKelompok'))
        else:
            savekelompok.save()
            messages.success(request, 'Pelaksana Kegiatan Yayasan Sudah Berhasil di Input.', extra_tags='primary')
            return HttpResponseRedirect(reverse('aset:indexKelompok'))
    else:
        return HttpResponseRedirect(reverse('aset:indexKelompok'))

@login_required(login_url=settings.LOGIN_URL)
def deleteKelompok(request, pk):
    kelompok = get_object_or_404(Kode_kelompok, pk=pk)
    kelompok.delete()
    messages.warning(request, ' Pelaksana Kegiatan Yayasan Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('aset:indexKelompok'))  

@login_required(login_url=settings.LOGIN_URL)
def editKelompok(request, pk):
    kelompok = get_object_or_404(Kode_kelompok, pk=pk)
    if request.method == "POST" :
        kelompok.nama_kelompok = request.POST['nama_kelompok']
        kelompok.save()
        messages.success(request, ' Pelaksana Kegiatan Yayasan Sudah Berhasil Diubah.', extra_tags='primary')
        return HttpResponseRedirect(reverse('aset:indexKelompok'))
    else:
        return render(request,"kelompok/edit.html",{'kelompok':kelompok})

# Ruangan Aset
class RuanganIndexView(generic.ListView):
    model = Ruangan
    template_name = 'ruangan/index.html'

    def get_context_data(self, **kwargs):
        context = super(RuanganIndexView, self).get_context_data(**kwargs)
        context['lokasi_list'] = Lokasi_aset.objects.all()
        context['kelompok_list'] = Kode_kelompok.objects.all()
        return context
@login_required(login_url=settings.LOGIN_URL)
def addRuangan(request):
    if request.method == "POST" :
        id_ruangan = request.POST['id_ruangan']
        saveruangan = Ruangan(id_ruang=id_ruangan,nama_ruang=request.POST['nama_ruangan'],id_kelompok_id = request.POST['id_kelompok'],id_lokasi_id=request.POST['id_lokasi'])
        
        if Ruangan.objects.filter(id_ruang=id_ruangan).exists():
                messages.warning(request, 'ID Ruangan   Sudah Ada.', extra_tags='danger')
                return HttpResponseRedirect(reverse('aset:indexRuangan'))
        else:
            saveruangan.save()
            messages.success(request, 'Ruangan Aset Sudah Berhasil di Input.', extra_tags='primary')
            return HttpResponseRedirect(reverse('aset:indexRuangan'))
    else:
        return HttpResponseRedirect(reverse('aset:indexRuangan'))

@login_required(login_url=settings.LOGIN_URL)
def deleteRuangan(request, pk):
    ruangan = get_object_or_404(Ruangan, pk=pk)
    ruangan.delete()
    messages.warning(request, 'Ruangan Aset Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('aset:indexRuangan')) 

@login_required(login_url=settings.LOGIN_URL)
def editRuangan(request, pk):
    kelompok = Kode_kelompok.objects.all()
    lokasi = Lokasi_aset.objects.all()
    ruangan = get_object_or_404(Ruangan, pk=pk) 
    if request.method == "POST" :
        ruangan.nama_ruang = request.POST['nama_ruangan']
        ruangan.id_lokasi = Lokasi_aset.objects.get(pk=request.POST['id_lokasi'])  
        ruangan.id_kelompok = Kode_kelompok.objects.get(pk=request.POST['id_kelompok']) 
        ruangan.save()
        messages.success(request, 'Ruangan Aset Sudah Berhasil Diubah', extra_tags='primary')
        return HttpResponseRedirect(reverse('aset:indexRuangan'))
    else:
        
        return render(request,"ruangan/edit.html",{'ruangan':ruangan,'lokasi':lokasi,'kelompok':kelompok})
