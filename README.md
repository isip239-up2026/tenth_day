# NETRUNNER BOARD — учебный проект

Киберпанк-доска заданий: корпорации публикуют миссии, хакеры берут контракты.

## Быстрый старт

```bash
pip install django
python manage.py migrate
python seed.py          # загрузить данные
python manage.py runserver
```

Открыть: http://127.0.0.1:8000  
Админка: http://127.0.0.1:8000/admin — логин `admin` / пароль `admin`

---

## Структура проекта

```
cyberpunk/
├── cyberpunk/              # настройки проекта
│   ├── settings.py
│   └── urls.py
├── core/                   # приложение
│   ├── models.py           # Corporation, Hacker, Mission, Implant, MissionApplication, NewsPost
│   ├── views.py            # index, mission_detail, hackers
│   ├── urls.py
│   ├── admin.py
│   └── templates/core/
│       ├── base.html
│       ├── index.html
│       ├── hackers.html
│       └── mission_detail.html
├── seed.py
└── db.sqlite3
```

## Модели

```
Corporation       — name, slogan, description, founded, logo_url
Hacker            — handle, bio, rank, corporation(FK), avatar_url, rep
Mission           — title, description, reward, difficulty(1-5), status, corporation(FK), posted_at
Implant           — name, description, slot, price, manufacturer(FK)
MissionApplication— mission(FK), hacker(FK), message, applied_at
NewsPost          — title, content, source, posted_at, views
```

## Страницы в стартовом проекте

| URL | Описание |
|-----|----------|
| `/` | Доска миссий + последние новости |
| `/mission/<id>/` | Детальная страница миссии |
| `/hackers/` | Реестр хакеров |

---

## Задания для студентов

Все задания выполняются **параллельно**. Каждый студент создаёт свою ветку и делает Pull Request.

---

### Task 1 — Профиль хакера
**Ветка:** `feature/hacker-profile`  
**Файлы:** `core/views.py`, `core/urls.py`, `core/templates/core/hacker_detail.html` (создать), `core/templates/core/hackers.html`

Сейчас список хакеров есть, но у каждого нет своей страницы.

Что сделать:
1. Добавить маршрут `/hacker/<int:hacker_id>/` и view `hacker_detail`
2. View передаёт хакера в шаблон: `hacker = get_object_or_404(Hacker, id=hacker_id)`
3. Создать `hacker_detail.html` — аватар, псевдоним, ранг, биография, репутация, корпорация
4. Вывести на странице профиля список миссий на которые хакер подавал заявки через `hacker.applications.select_related('mission').all()`
5. В `hackers.html` в блоке `ЗАДАНИЕ 2` сделать псевдоним хакера кликабельной ссылкой на профиль

---

### Task 2 — Страница корпорации
**Ветка:** `feature/corporation`  
**Файлы:** `core/views.py`, `core/urls.py`, `core/templates/core/corporation_detail.html` (создать), `core/templates/core/corporations.html` (создать), `core/templates/core/base.html`, `core/templates/core/mission_detail.html`

Что сделать:
1. Добавить маршруты `/corporations/` и `/corporation/<int:corp_id>/`
2. View `corporations` — список всех корпораций
3. View `corporation_detail` — корпорация, её миссии и хакеры в штате
4. Создать `corporations.html` — карточки корпораций: название, слоган, год основания
5. Создать `corporation_detail.html` — название, описание, список миссий, список хакеров
6. В `base.html` в блоке `ЗАДАНИЕ 3` добавить ссылку «Корпорации»
7. В `mission_detail.html` в блоке `ЗАДАНИЕ 3` сделать имя заказчика ссылкой на страницу корпорации

---

### Task 3 — Фильтрация и пагинация миссий
**Ветка:** `feature/missions-filter`  
**Файлы:** `core/views.py`, `core/templates/core/index.html`

Сейчас на главной показываются только открытые миссии без фильтрации. Нужно добавить управление списком.

Что сделать:
1. В view `index` добавить фильтрацию по сложности через `request.GET.get('difficulty')` — `Mission.objects.filter(difficulty=diff)` если параметр передан
2. Добавить фильтрацию по статусу через `request.GET.get('status')` — по умолчанию показывать все
3. В `index.html` в блоке `ЗАДАНИЕ 4` добавить кнопки фильтрации: сложность (1–5) и статус (Bootstrap `btn-group`)
4. Добавить пагинацию через `Paginator` — по 5 миссий на страницу
5. При формировании ссылок пагинации сохранять активные фильтры: `?difficulty=3&status=open&page=2`

---

### Task 4 — Форма заявки на миссию
**Ветка:** `feature/application`  
**Файлы:** `core/forms.py` (создать), `core/views.py`, `core/urls.py`, `core/templates/core/mission_detail.html`

Что сделать:
1. Создать `core/forms.py` с классом `ApplicationForm`:
```python
from django import forms

class ApplicationForm(forms.Form):
    hacker_handle = forms.CharField(label="Ваш псевдоним", max_length=100)
    message       = forms.CharField(label="Сообщение заказчику", widget=forms.Textarea)
```
2. Добавить маршрут `/mission/<int:mission_id>/apply/` и view `apply_mission`
3. View обрабатывает GET (показывает форму) и POST:
   - находит или сообщает об ошибке если хакера с таким псевдонимом нет в БД
   - создаёт `MissionApplication`, если хакер ещё не подавал заявку на эту миссию
   - редиректит на страницу миссии
4. В `mission_detail.html` в блоке `ЗАДАНИЕ 5` вывести форму с Bootstrap-стилями
5. В инфо-блоке в блоке `ЗАДАНИЕ 5` заменить `—` на реальное количество заявок

---

### Task 5 — Поиск
**Ветка:** `feature/search`  
**Файлы:** `core/views.py`, `core/urls.py`, `core/templates/core/base.html`, `core/templates/core/search.html` (создать)

Что сделать:
1. В `base.html` в блоке `ЗАДАНИЕ 6` добавить GET-форму поиска в навбар
2. Добавить маршрут `/search/` и view `search`
3. Искать одновременно по миссиям, хакерам и новостям:
```python
from django.db.models import Q
missions = Mission.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
hackers  = Hacker.objects.filter(Q(handle__icontains=q) | Q(bio__icontains=q))
news     = NewsPost.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
```
4. Создать `search.html` — три секции результатов: «Миссии», «Хакеры», «Новости». Если секция пуста — не показывать
5. В заголовке выводить: `Поиск: "arasaka" — найдено 3 миссии, 1 хакер, 2 новости`

---

### Task 6 — Каталог имплантов (После task 2)
**Ветка:** `feature/implants`  
**Файлы:** `core/views.py`, `core/urls.py`, `core/templates/core/implants.html` (создать), `core/templates/core/implant_detail.html` (создать), `core/templates/core/base.html`

Что сделать:
1. Добавить маршруты `/implants/` и `/implant/<int:implant_id>/`
2. View `implants` — список всех имплантов с фильтрацией по слоту через `request.GET.get('slot')`
3. Создать `implants.html` — карточки имплантов: название, слот, цена, производитель. Кнопки-фильтры по слоту: Нейронный, Оптический, Физический, Программный
4. View `implant_detail` и шаблон `implant_detail.html` — полное описание, цена, производитель со ссылкой на корпорацию (использует код task 2)
5. В `base.html` в блоке `ЗАДАНИЕ 7` добавить ссылку «Импланты» в навбар

---

### Task 7 — Похожие миссии
**Ветка:** `feature/related-missions`  
**Файлы:** `core/views.py`, `core/templates/core/mission_detail.html`

Что сделать:
1. В view `mission_detail` добавить похожие миссии — те у которых совпадает уровень сложности или заказчик:
```python
from django.db.models import Q
related = Mission.objects.filter(
    Q(difficulty=mission.difficulty) | Q(corporation=mission.corporation)
).exclude(id=mission.id)[:4]
```
2. В `mission_detail.html` в блоке `ЗАДАНИЕ 8` вывести похожие миссии списком — название, награда, сложность, ссылка
3. Если похожих нет — блок не показывать
4. Рядом с каждой похожей миссией пометить причину совпадения: «Похожая сложность» или «Тот же заказчик»

---

### Task 8 — Новости
**Ветка:** `feature/news`  
**Файлы:** `core/views.py`, `core/urls.py`, `core/templates/core/news_list.html` (создать), `core/templates/core/news_detail.html` (создать), `core/templates/core/index.html`, `core/templates/core/base.html`

Что сделать:
1. Добавить маршруты `/news/` и `/news/<int:post_id>/`
2. View `news_list` — список всех новостей
3. View `news_detail` — при каждом открытии увеличивать счётчик `post.views += 1; post.save()`, передавать пост в шаблон
4. Создать `news_list.html` — карточки новостей: заголовок, источник, дата, просмотры
5. Создать `news_detail.html` — полный текст новости, источник, дата, счётчик просмотров
6. В `index.html` заголовки новостей в боковой панели сделать кликабельными ссылками (блок `ЗАДАНИЕ 9`)
7. В `index.html` добавить ссылку «Все новости» и в `base.html` добавить ссылку «Новости» в навбар

---

### Task 9 — Сортировка хакеров
**Ветка:** `feature/hackers-sort`  
**Файлы:** `core/views.py`, `core/templates/core/hackers.html`

Что сделать:
1. В view `hackers` добавить фильтрацию по рангу через `request.GET.get('rank')` — `Hacker.objects.filter(rank=rank)`
2. Добавить сортировку через `request.GET.get('sort', '-rep')`: по репутации (`-rep`), по псевдониму (`handle`), по рангу (`rank`)
3. В `hackers.html` добавить Bootstrap `btn-group` с кнопками рангов: «Все», «Ghost», «Elite», «Netrunner», «Script Kiddie»
4. Добавить кнопки сортировки: «По репутации», «По псевдониму»
5. Выделить активные фильтры через `{% if request.GET.rank == 'ghost' %}btn-success{% else %}btn-outline-success{% endif %}`

---

### Task 10 — Форма связи с хакером
**Ветка:** `feature/contact`  
**Файлы:** `core/forms.py` (создать если не создан), `core/views.py`, `core/urls.py`, `core/templates/core/contact.html` (создать), `core/templates/core/hackers.html`

Что сделать:
1. Создать или дополнить `forms.py` классом `ContactForm` — поля: `from_handle` (псевдоним отправителя), `subject` (тема), `message` (сообщение)
2. Добавить маршрут `/hacker/<int:hacker_id>/contact/`
3. View `contact_hacker` обрабатывает GET и POST. При успешной отправке — показать страницу успеха с сообщением «Сообщение зашифровано и доставлено»
4. Создать `contact.html` — форма в стиле терминала, Bootstrap-стилизация полей
5. В `hackers.html` в блоке `ЗАДАНИЕ 10` добавить кнопку «Связаться» у каждого хакера

---

### Task 11 — Топ хакеров и статистика
**Ветка:** `feature/top`  
**Файлы:** `core/views.py`, `core/urls.py`, `core/templates/core/top.html` (создать), `core/templates/core/index.html`, `core/templates/core/base.html`

Что сделать:
1. Добавить маршрут `/top/` и view `top_hackers`
2. В view получить топ-10 хакеров по репутации и статистику:
```python
from django.db.models import Count, Avg
top = Hacker.objects.order_by('-rep')[:10]
stats = {
    'total_missions': Mission.objects.count(),
    'total_hackers':  Hacker.objects.count(),
    'total_reward':   Mission.objects.aggregate(s=Sum('reward'))['s'],
    'avg_difficulty': Mission.objects.aggregate(a=Avg('difficulty'))['a'],
}
```
3. Создать `top.html` — нумерованный топ с аватаром, псевдонимом, рангом и репутацией. Первые три места выделить золотом/серебром/бронзой
4. Добавить блок «Статистика сети» — общее число миссий, хакеров, суммарная награда, средняя сложность
5. В `index.html` в блоке `ЗАДАНИЕ 11` вывести топ-5 хакеров в боковой панели
6. В `base.html` добавить ссылку «Топ хакеров» в навбар

---

### Task 12 — Экспорт и страница 404
**Ветка:** `feature/export`  
**Файлы:** `core/views.py`, `core/urls.py`, `core/templates/core/mission_detail.html`, `core/templates/404.html` (создать), `cyberpunk/settings.py`, `cyberpunk/urls.py`

**Часть А — Экспорт миссии:**
1. Добавить маршрут `/mission/<int:mission_id>/export/`
2. View `export_mission` возвращает текстовый файл:
```python
response = HttpResponse(content_type='text/plain; charset=utf-8')
response['Content-Disposition'] = f'attachment; filename="mission_{mission.id}.txt"'
```
3. Файл содержит: название, сложность (`difficulty_bars()`), награду, статус, заказчика, описание, список заявок
4. На странице миссии добавить кнопку «Скачать бриф»
5. Если передан параметр `?format=csv` — вернуть CSV через стандартный модуль `csv`

**Часть Б — Своя страница 404:**
1. В `settings.py` выставить `DEBUG = False` и `ALLOWED_HOSTS = ['*']`
2. Создать `core/templates/404.html` в киберпанк-стиле — терминальный вид, сообщение `ERROR_404: SIGNAL_LOST`, кнопка «Вернуться на базу»
3. В `views.py` добавить `def handler404(request, exception): return render(request, '404.html', status=404)`
4. В `cyberpunk/urls.py` добавить `handler404 = 'core.views.handler404'`
