from django.db import models


class Corporation(models.Model):
    name        = models.CharField(max_length=200, verbose_name="Название")
    slogan      = models.CharField(max_length=300, verbose_name="Слоган")
    description = models.TextField(verbose_name="Описание")
    founded     = models.IntegerField(verbose_name="Год основания")
    logo_url    = models.URLField(blank=True, verbose_name="Логотип")

    class Meta:
        verbose_name = "Корпорация"
        verbose_name_plural = "Корпорации"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Hacker(models.Model):
    RANK_CHOICES = [
        ("script_kiddie", "Script Kiddie"),
        ("netrunner",     "Netrunner"),
        ("elite",         "Elite Hacker"),
        ("ghost",         "Ghost"),
    ]
    handle      = models.CharField(max_length=100, verbose_name="Псевдоним")
    bio         = models.TextField(verbose_name="Биография")
    rank        = models.CharField(max_length=20, choices=RANK_CHOICES,
                                   default="netrunner", verbose_name="Ранг")
    corporation = models.ForeignKey(Corporation, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name="hackers",
                                    verbose_name="Корпорация")
    avatar_url  = models.URLField(blank=True, verbose_name="Аватар")
    rep         = models.IntegerField(default=0, verbose_name="Репутация")

    class Meta:
        verbose_name = "Хакер"
        verbose_name_plural = "Хакеры"
        ordering = ["-rep"]

    def __str__(self):
        return self.handle


class Mission(models.Model):
    STATUS_CHOICES = [
        ("open",      "Открыта"),
        ("active",    "Активна"),
        ("completed", "Завершена"),
        ("failed",    "Провалена"),
    ]
    DIFFICULTY_CHOICES = [(i, str(i)) for i in range(1, 6)]

    title         = models.CharField(max_length=200, verbose_name="Название")
    description   = models.TextField(verbose_name="Описание")
    reward        = models.IntegerField(verbose_name="Награда (кредиты)")
    difficulty    = models.IntegerField(choices=DIFFICULTY_CHOICES,
                                        verbose_name="Сложность")
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                     default="open", verbose_name="Статус")
    corporation   = models.ForeignKey(Corporation, on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      related_name="missions",
                                      verbose_name="Заказчик")
    posted_at     = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Миссия"
        verbose_name_plural = "Миссии"
        ordering = ["-posted_at"]

    def __str__(self):
        return self.title

    def difficulty_bars(self):
        return "█" * self.difficulty + "░" * (5 - self.difficulty)


class Implant(models.Model):
    SLOT_CHOICES = [
        ("neural",   "Нейронный"),
        ("optical",  "Оптический"),
        ("physical", "Физический"),
        ("software", "Программный"),
    ]
    name        = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    slot        = models.CharField(max_length=20, choices=SLOT_CHOICES,
                                   verbose_name="Слот")
    price       = models.IntegerField(verbose_name="Цена (кредиты)")
    manufacturer= models.ForeignKey(Corporation, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name="implants",
                                    verbose_name="Производитель")
    class Meta:
        verbose_name = "Имплант"
        verbose_name_plural = "Импланты"
        ordering = ["slot", "name"]

    def __str__(self):
        return self.name


class MissionApplication(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE,
                                related_name="applications",
                                verbose_name="Миссия")
    hacker  = models.ForeignKey(Hacker, on_delete=models.CASCADE,
                                related_name="applications",
                                verbose_name="Хакер")
    message = models.TextField(verbose_name="Сообщение")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        unique_together = ["mission", "hacker"]

    def __str__(self):
        return f"{self.hacker.handle} → {self.mission.title}"


class NewsPost(models.Model):
    title      = models.CharField(max_length=200, verbose_name="Заголовок")
    content    = models.TextField(verbose_name="Текст")
    source     = models.CharField(max_length=100, verbose_name="Источник")
    posted_at  = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    views      = models.IntegerField(default=0, verbose_name="Просмотры")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-posted_at"]

    def __str__(self):
        return self.title
