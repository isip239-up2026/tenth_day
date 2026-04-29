import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cyberpunk.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import Corporation, Hacker, Mission, Implant, NewsPost

Corporation.objects.all().delete()
Hacker.objects.all().delete()
Mission.objects.all().delete()
Implant.objects.all().delete()
NewsPost.objects.all().delete()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin")
    print("Создан администратор: логин=admin пароль=admin")

corps = {}
for name, slogan, desc, year in [
    ("Arasaka", "Нет ничего более постоянного, чем наша защита",
     "Крупнейшая японская мегакорпорация. Занимается безопасностью, банковским делом и производством оружия. Её отделения есть в каждом крупном городе мира.",
     1915),
    ("Militech", "Сила — это мир",
     "Американская военно-промышленная мегакорпорация. Производит оружие, военную технику и частные армии. Главный конкурент Arasaka.",
     1996),
    ("Kang Tao", "Инновации без границ",
     "Китайская корпорация, специализирующаяся на разработке оружия, кибернетике и системах наблюдения. Быстро набирает влияние.",
     2008),
    ("Biotechnica", "Жизнь — это технология",
     "Корпорация занимается биотехнологиями, генной инженерией и производством синтетической еды. Контролирует значительную часть мирового сельского хозяйства.",
     2001),
    ("Netwatch", "Мы видим всё",
     "Международная организация, занимающаяся обеспечением безопасности в сети. Охотится за хакерами и нелегальными AI.",
     2005),
]:
    corps[name] = Corporation.objects.create(
        name=name, slogan=slogan, description=desc, founded=year)

hackers_data = [
    ("GhostByte",  "elite",        "Netwatch", 4200,
     "https://i.pravatar.cc/150?img=11",
     "Легенда андерграунда. Взломала Arasaka три раза подряд. Никто не знает её настоящего лица."),
    ("ZeroCool",   "ghost",        None, 7800,
     "https://i.pravatar.cc/150?img=12",
     "Призрак в сети. Существование подтверждено только косвенными уликами. Говорят, работает на себя."),
    ("D4RKM4TTER", "elite",        "Militech", 3100,
     "https://i.pravatar.cc/150?img=13",
     "Специалист по промышленному шпионажу. Слил датабазу Arasaka в 2073. Ценится корпорациями."),
    ("px1_ghost",  "netrunner",    None, 1500,
     "https://i.pravatar.cc/150?img=14",
     "Молодой нетраннер из трущоб. Агрессивный стиль взлома. Быстро набирает репутацию."),
    ("Syn4pse",    "netrunner",    "Kang Tao", 2700,
     "https://i.pravatar.cc/150?img=15",
     "Эксперт по нейронным интерфейсам. Работает на Kang Tao, но берёт частные заказы."),
    ("NULL_PTR",   "script_kiddie",None, 300,
     "https://i.pravatar.cc/150?img=16",
     "Новичок в сети. Использует чужие скрипты, но учится быстро."),
    ("0x_CIPHER",  "elite",        "Netwatch", 5500,
     "https://i.pravatar.cc/150?img=17",
     "Работает с Netwatch официально, но слухи ходят разные. Специалист по крипто и деньгам."),
    ("Kira//Null", "ghost",        None, 9100,
     "https://i.pravatar.cc/150?img=20",
     "Самый опасный призрак в сети. Единственный нетраннер, взломавший военный спутник."),
]

hackers = {}
for handle, rank, corp_name, rep, avatar, bio in hackers_data:
    h = Hacker.objects.create(
        handle=handle, rank=rank, rep=rep, avatar_url=avatar, bio=bio,
        corporation=corps.get(corp_name) if corp_name else None)
    hackers[handle] = h

missions_data = [
    ("Удалить досье", "Arasaka", 5, 15000, "open",
     "Проникнуть в архивы Arasaka и удалить файлы на нескольких корпоративных осведомителей. Требуется работа в реальном времени — у вас будет не более 90 секунд до поднятия тревоги."),
    ("Взломать Netwatch", "Militech", 4, 12000, "open",
     "Militech хочет знать, что Netwatch знает о проекте BLACKWALL. Требуется извлечь зашифрованные логи без следов вторжения."),
    ("Угнать прототип", "Kang Tao", 3, 8000, "open",
     "Перехватить беспроводную передачу данных о новом прототипе оружия. Окно — 20 минут во время транспортировки."),
    ("Слежка за корпом", None, 2, 3000, "open",
     "Анонимный клиент хочет знать маршруты передвижения одного корпоративного менеджера. Установить трекер на его ИИ-водителя."),
    ("Отключить камеры", None, 1, 1500, "open",
     "Отключить сеть наблюдения в блоке C9 на 10 минут. Простая работа для опытного нетраннера. Анонимная оплата."),
    ("Кража биоданных", "Biotechnica", 5, 20000, "open",
     "Похитить данные генетических исследований из защищённого сервера Biotechnica. Сервер полностью изолирован — придётся найти физический способ подключения."),
    ("Диверсия в сети", "Militech", 3, 7000, "active",
     "Внедрить вирус в логистическую сеть конкурентов, чтобы задержать цепочку поставок на 48 часов."),
    ("Разблокировать ИИ", None, 4, 11000, "open",
     "Клиент хочет разблокировать нелегальный ИИ, заблокированный Netwatch. Работа опасная — за такое дают до 20 лет."),
    ("Спасти информатора", None, 2, 5000, "open",
     "Корпоративный информатор просит стереть его цифровой след до того, как Arasaka его найдёт. Быстрая работа, чистая оплата."),
    ("Взлом биржи", "Kang Tao", 5, 25000, "open",
     "Манипуляция торгами на Найтсити Фондовой Бирже в пользу заказчика. Высокий риск — Netwatch активно мониторит биржу."),
]

for title, corp_name, diff, reward, status, desc in missions_data:
    Mission.objects.create(
        title=title, description=desc, reward=reward,
        difficulty=diff, status=status,
        corporation=corps.get(corp_name) if corp_name else None)

implants_data = [
    ("Kiroshi Optics Mk.3", "neural",   8500,  "Militech",  "Военные нейронные импланты для ускорения реакции. Снижают время отклика на 40мс."),
    ("Mantis Blades",       "physical", 15000, "Arasaka",   "Убирающиеся лезвия из монокристаллического карбида. Режут почти всё."),
    ("Reflex Tuner",        "neural",   6000,  "Kang Tao",  "Оптимизирует нейронные пути для боевых ситуаций. +15% к скорости."),
    ("Smart Eye v2",        "optical",  4500,  "Kang Tao",  "Дополненная реальность, сканирование угроз, ночное зрение."),
    ("Memory Booster",      "software", 3000,  "Biotechnica","Расширяет оперативную память мозга. Идеален для нетраннеров."),
    ("Subdermal Armor",     "physical", 12000, "Militech",  "Подкожные керамические пластины. Снижают урон от огнестрельного оружия."),
    ("Sandevistan",         "neural",   18000, "Arasaka",   "Легендарный адреналиновый имплант. Замедляет восприятие времени на 3 секунды."),
    ("Rebreather",          "physical", 2500,  "Biotechnica","Встроенный фильтр воздуха. Защищает от токсинов и газов."),
]

for name, slot, price, corp_name, desc in implants_data:
    Implant.objects.create(
        name=name, slot=slot, price=price, description=desc,
        manufacturer=corps.get(corp_name))

news_data = [
    ("Arasaka открывает новый офис в Алматы", "NightCity Herald",
     "Мегакорпорация объявила о расширении в Центральную Азию. Эксперты предупреждают о рисках для цифрового суверенитета региона."),
    ("Netwatch усиливает патрулирование Blackwall", "NetFeed",
     "После серии инцидентов с нелегальными ИИ организация увеличивает бюджет на 300%. Хакеры предупреждены."),
    ("ZeroCool снова в деле — три банка взломаны за ночь", "DarkNet Pulse",
     "Анонимный источник подтвердил: легендарный призрак провёл серию атак. Следов не осталось."),
    ("Новый имплант Sandevistan вышел в продажу", "CyberMag",
     "Arasaka выпустила обновлённую версию легендарного замедлителя времени. Цена — 18000 кредитов."),
    ("Militech и Kang Tao подписали договор о ненападении", "CorpWatch",
     "Аналитики в шоке. Вечные конкуренты временно объединились против общей угрозы."),
    ("Взлом биржи: подозревают нетраннера из Найтсити", "FinancialNet",
     "Регулятор расследует аномальные торги. Ущерб оценивается в 40 млн кредитов."),
]

for title, source, content in news_data:
    NewsPost.objects.create(title=title, source=source, content=content)

print(f"Готово: {Corporation.objects.count()} корпораций, "
      f"{Hacker.objects.count()} хакеров, "
      f"{Mission.objects.count()} миссий, "
      f"{Implant.objects.count()} имплантов, "
      f"{NewsPost.objects.count()} новостей.")
