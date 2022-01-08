from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.utils import timezone, dateformat
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'aset'
now = timezone.localtime(timezone.now()).strftime("%d%m%Y%H%M%S")
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout',login_required(LogoutView.as_view(next_page='aset:login')), name='logout'),
    path('', login_required(views.Data_asetIndexView.as_view()), name='indexData_aset'),
    path('deleteData/<str:pk>', views.deleteData, name='deleteData'),
    path('editData/<str:pk>', views.editData, name='editData'),
    path('addData', views.addData, name='addData'),
    path('detailData/<str:pk>', views.Data_aset_DetailView, name='detailData'),
    path('printaset'+now, login_required(views.Print_aset.as_view()), name='printAset'),
    path('printasett'+now, views.Print_asett, name='printAsett'),

    path('printlabel', login_required(views.Print_label.as_view()), name='printLabel'),



    
    # PRINTKIB
    path('print_kiba'+now, views.Print_kiba, name='Print_kiba'),
    path('print_kibaF'+now, views.Print_kiba_F, name='Print_kibaF'),
    path('print_kibb'+now, views.Print_kibb, name='Print_kibb'),
    path('print_kibbF'+now, views.Print_kibb_F, name='Print_kibbF'),
    path('print_kibc'+now, views.Print_kibc, name='Print_kibc'),
    path('print_kibcF'+now, views.Print_kibc_F, name='Print_kibcF'),
    path('print_kibd'+now, views.Print_kibd, name='Print_kibd'),
    path('print_kibdF'+now, views.Print_kibd_F, name='Print_kibdF'),

    path('dahsboard1', views.Dashboard1, name='dashboard1'),

    path('jenis', login_required(views.JenisIndexView.as_view()), name='indexJenis'),
    path('addJenis', views.addJenis, name='addJenis'),
    path('deleteJenis/<str:pk>', views.deleteJenis, name='deleteJenis'),
    path('editJenis/<str:pk>', views.editJenis, name='editJenis'),

    path('klasifikasi', login_required(views.KlasifikasiIndexView.as_view()), name='indexKlasifikasi'),
    path('addKlasifikasi', views.addKlasifikasi, name='addKlasifikasi'),
    path('deleteKlasifikasi/<str:pk>', views.deleteKlasifikasi, name='deleteKlasifikasi'),
    path('editKlasifikasi/<str:pk>', views.editKlasifikasi, name='editKlasifikasi'),

    path('lokasi', login_required(views.LokasiIndexView.as_view()), name='indexLokasi'),
    path('addLokasi', views.addLokasi, name='addLokasi'),
    path('deleteLokasi/<str:pk>', views.deleteLokasi, name='deleteLokasi'),
    path('editLokasi/<str:pk>', views.editLokasi, name='editLokasi'),   

    path('kelompok', login_required(views.KelompokIndexView.as_view()), name='indexKelompok'),
    path('addKelompok', views.addKelompok, name='addKelompok'),
    path('deleteKelompok/<str:pk>', views.deleteKelompok, name='deleteKelompok'),
    path('editKelompok/<str:pk>', views.editKelompok, name='editKelompok'), 


    path('ruangan', login_required(views.RuanganIndexView.as_view()), name='indexRuangan'),
    path('addRuangan', views.addRuangan, name='addRuangan'),
    path('deleteRuangan/<str:pk>', views.deleteRuangan, name='deleteRuangan'),
    path('editRuangan/<str:pk>', views.editRuangan, name='editRuangan'), 

    path('addKiba', views.addKiba, name='addKiba'),
    path('kiba', views.KibaIndexView, name='indexKiba'),
    path('editKiba/<str:pk>', views.editKiba, name='editKiba'),

    path('addKibb', views.addKibb, name='addKibb'),
    path('kibb', views.KibbIndexView, name='indexKibb'),
    path('editKibb/<str:pk>', views.editKibb, name='editKibb'),
    
    path('addKibc', views.addKibc, name='addKibc'),
    path('kibc', views.KibcIndexView, name='indexKibc'),
    path('editKibc/<str:pk>', views.editKibc, name='editKibc'),

    path('addKibd', views.addKibd, name='addKibd'),
    path('kibd', views.KibdIndexView, name='indexKibd'),
    path('editKibd/<str:pk>', views.editKibd, name='editKibd'),

    

]

