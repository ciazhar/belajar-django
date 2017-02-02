#Tutorial Django

#setup environment
  ```
    install python3
    pip install djanggo
  ```
  Note : pastikan install python-pip

#bikin project
  ```
    django-admin startproject tutorial_bioskop
  ```
  NOte : pastikan install python-django-common

add project ke text editor

migrate database, secara default dia pake SQLite:
  ```
    python manage.py migrate
  ```

bikin superuser
  ```
    python manage.py createsuperuser
  ```
#jananin project
jalankan aplikasi :
  ```
    python manage.py runserver
  ```
aplikasi di browser :
  ```
    localhost:8000
  ```
  Note : buat accsess admin localhost:8000/admin, kalo mau ganti di urls.py

#bikin apps movie
bikin apps :
  ```
    python manage.py startapp movie
  ```
bikin model (movie/models.py):
  ```
    from __future__ import unicode_literals

    from django.db import models
    from django.contrib.auth.models import User

    class  Genre(object):
        title = models.CharField(max_length=200)
        description = models.TextField(null=True, blank=True)

    class  movie(object):
        title = models.Charfield(max_length=200)
        description = models.TextField(null=True, blank=True)
        show_from = models.DateField()
        show_until = models.DateField()
        genres = models.ManyToManyField(Genre)
        posted_by = models.ForeignKey(user)
        created_at = models.DataField(auto_now_add=True)
        updated_at = models.DateField(auto_now=True)
  ```
setting app (settings.py)
  ```
    'movie' ke INSTALLED_APPS
  ```

setting admin(admin.py)
  ```
    from django.contrib import admin
    from .models import Genre, Movie

    class  GenreAdmin(admin.ModelAdmin):
        pass

    class  MovieAdmin(admin,ModelAdmin):
        list_display = {'title', 'posted_by', 'show_from', 'show_until', 'created_at'}

        admin.site.register(Genre, GenreAdmin)
        admin.site.register(Movie, GenreAdmin)
  ```

buat skrip migrasi :
  ```
    python manage.py makemigration
  ```
migrasi ke database :
  ```
    python manage.py migrate
  ```
Hari ke 2

#Setting UI untuk Movie
untuk mengganti nama variabel yang ada di system menjadi berbeda di UI, bisa menggunakan verbose_name, atau menulis di parameter pertama(movie/models.py)
  ```
    title = models.CharField(max_length=200, verbose_name="judul") #verbose_name digunakaan untuk mengubah nama di UI
    description = models.TextField("deskripsi",null=True, blank=True)#mengubah nama di UI juga bisa di parameter pertama
    show_from = models.DateField()
    show_until = models.DateField()
    genres = models.ManyToManyField(Genre)
    posted_by = models.ForeignKey(User)
    created_at = models.DateField(auto_now_add=True)#ketika kita membuat pertama kali akan dibuat pawa waktu pertama kali, ketika ada baru gk update
    updated_at = models.DateField(auto_now=True)#ketika membuat pertambahan maka akan diupdate
  ```
buat fungsi untuk  Menampilkan macam-macam genre (movie/models.py)
  ```
    #fungsi Menampilkan macam-macam genre
      def show_genres(self):
          genre = self.genres.all()
          text=''
          for data in genre:
              text += data.title+", "
          return text
  ```
setting dependency movie(title, description dll) yang akan ditampilkan di UI (movie/admin.py)
  ```
    #menentukan field apa saja yang ditampilkan pada tabel UI Movie, termasuk kita bisa menampilkan methode dari model yang di return string
    list_display = ('title','show_genres', 'posted_by', 'show_from', 'show_until', 'created_at', 'show_status')

    #menentukan field apa saja yang ditampilkan pada form UI Movie
    fields = ('title','description', 'show_from', 'show_until', 'genres')

    #override pada prosedur simpan
    def save_model(self, request, obj, form, change):
        obj.posted_by = request.user
        super(MovieAdmin, self).save_model(request,obj,form, change)
  ```
#Service di sisi client berupa daftar movie
setting directory template ke folder view (setting.py)
  ```
    TEMPLATES = [
        {
            ...
            'DIRS': ['view'],
            ...
        },
    ]
  ```
bikin UI (index.html)

bikin service show status movie (movie/models.py)
  ```
      #fungsi untuk menampilkan movie sedang tayang, sudah tayang atau segera tayang dengan representasi angka
      def in_show(self):
          now = datetime.now().date()
          if now >= self.show_from and now <= self.show_until:
              return 1 #sedang tayang
          elif now > self.show_until:
              return -1 #sudah tayang
          else :
              return 0 #segera tayang
      #fungsi untuk menampilkan movie sedang tayang, sudah tayang atau segera tayang dengan representasi angka
      def show_status(self):
          if self.in_show() == 1 :
              return "sedang tayang"
          elif self.in_show()== -1 :
              return "selesai tayang"
          else :
              return "segera tayang"
  ```
setting view(movie/views.py)
  ```
    from django.shortcuts import render
    from django.views.generic import ListView, DetailView, TemplateView
    from .models import Movie

    class IndexView(ListView):
        model = Movie
        template_name = 'index.html'
  ```
bikin mapping url (urls.py)
  ```
    urlpatterns = [
        url(r'^$',IndexView.as_view(),name="index")#dollar ($) merupakan regular expression, merujuk pada url yang didepanya gak ada dan setelahnya gak ada
    ]
  ```

Hari 3
#Bootstrapping UI
- Add File Bootstrap ke folder static
- Setting default static files(settings.py)
  ```
    
    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]

  ```
- Load Static file ke UI (view/index.html)
  ```
    ...
    {%load static%}
    ...
    ...
    <link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">
    ...
  ```
  Note :
  dengan memanggil {% load static %} kita dapat menimpor file folder static
  dengan memanggil {% static 'css/bootstrap.min.css' %}

#Template Inheritance
- Memasukkan komponen dari dashboard.html ke index.html menggunakan {% block nama-fungsi %}
  (view/index.html)
  ```
    <div class="row">
      <div class="col-md-9">
          {% block content %}

          {% endblock%}
      </div>
      <div class="col-md-3">
          {% block sidebar %}
            <div class="panel panel-default">
              <div class="panel-heading">
                Panel Sidebar
              </div>
              <div class="panel-body">
                Panel Content
              </div>
            </div>
          {% endblock%}
      </div>
    </div>
  ```
  Note :
  sintaks {% block content %}{% endblock%} akan memanggil fungsi yang ada di dashboard.html

  (view/index.html)
  ```
    {% extends 'index.html' %}
    {% load static %}
    {% block content %}
      <h1>Tayang Sekarang</h1>
      <div class="row">
        {% for data in object_list %}
          {% if data.in_show == 1 %}
            <div class="col-md-4">
              <a href="">
                <img src="{% static 'images/no-pre.png' %}" alt="" />
                <h3>{{data.title}}</h3>
                <div>tayang : {{data.show_from}} - {{data.show_until}} </div>
              </a>
            </div>
          {% endif %}
        {% endfor %}
      </div>

    {% endblock%}
  ```
