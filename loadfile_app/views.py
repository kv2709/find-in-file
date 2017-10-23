from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import LoadFile
from .forms import LoadFileForm, StrInputForm
from .finderinfile import *
import ast
import os





# Create your views here.
def index(request):
    """Home page application"""
    return render(request, 'loadfile_app/index.html')


def about(request):
    """About page application"""
    return render(request, "loadfile_app/about.html")


def search_result(request):
    """Page with result search"""
    res_fields = LoadFile.objects.last()
    # Вернем строку в список
    str_found = res_fields.position_found
    lst_found = ast.literal_eval(str_found)
    lst_found_str = []
    format_triad = lambda s: " ".join([s[max(i - 3, 0):i] for i in range(len(s), 0, -3)][::-1])
    for i in range(len(lst_found)):
        lst_found_str.append(format_triad(str(lst_found[i])))

    file_name_for_delete = res_fields.file_obj.name
    path_file_name_for_delete = res_fields.file_obj.path
    if os.path.exists(path_file_name_for_delete):
        os.remove(path_file_name_for_delete)
    else:
        pass


    context = {'count_finder': res_fields.count_found,
               'lst_res': lst_found_str,
               'time_search': res_fields.time_search,
               'file_name_deleted' : file_name_for_delete
               }

    return render(request, 'loadfile_app/search_result.html', context)

def str_input(request):
    """Page for string input"""
    upload_file_obj = LoadFile.objects.last()
    upload_file_path = upload_file_obj.file_obj.path
    upload_file_size = upload_file_obj.file_obj.size
    format_triad = lambda s: " ".join([s[max(i - 3, 0):i] for i in range(len(s), 0, -3)][::-1])
    upload_file_size_templ = format_triad(str(upload_file_size))
    upload_file_name = upload_file_obj.file_obj.name

    if request.method != 'POST':
        form = StrInputForm()
    else:
        #Data send method POST, work data
        form = StrInputForm(request.POST)
        if form.is_valid():
            form_with_str = form.save(commit=False)
            # Присвоили полю базы file_name имя загруженного файла
            form_with_str.file_name = upload_file_name
            #Создаем объект поиска
            if upload_file_size < 2097152:
                find_in_upload = FinderBF(upload_file_path, form_with_str.str_for_search)
            else:
                find_in_upload = CombBF(upload_file_path, form_with_str.str_for_search)
            # Запускаем поиск
            find_in_upload.search()
            # Забираем результаты поиска
            form_with_str.position_found = str(find_in_upload.result())
            form_with_str.count_found = len(find_in_upload.result())
            form_with_str.time_search = str(find_in_upload.time_search())
            # Указание первичного ключа для модели формы
            # из загруженного из базы объекта
            form_with_str.id = upload_file_obj.pk
            # Обновляем запись в базе

            form_with_str.save(update_fields=['file_name', 'str_for_search','count_found',
                                              'position_found', 'time_search'])
            return HttpResponseRedirect(reverse('loadfile_app:search_result'))

    context = {'form': form, 'upload_file_for_form': upload_file_obj,
               'upload_file_size' : upload_file_size_templ}
    return render(request, 'loadfile_app/str_input.html', context)



def load_file(request):
    """Page for load file"""
    if request.method != 'POST':
        form = LoadFileForm()
    else:
        #Data send method POST, work data
        form = LoadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            fs = new_file.file_obj.size
            new_file.count_found = 0
            new_file.file_size = fs
            if fs <= 10485760:
                new_file.save()
                print(str(new_file.file_obj.path))
            else:
                format_triad = lambda s: " ".join([s[max(i - 3, 0):i] for i in range(len(s), 0, -3)][::-1])
                fs_str_triad = format_triad(str(fs))
                context = {'form': form, 'fs': fs_str_triad}
                return render(request, 'loadfile_app/load_file.html', context)

            return HttpResponseRedirect(reverse('loadfile_app:str_input'))

    context = {'form': form}
    return render(request, 'loadfile_app/load_file.html', context)

