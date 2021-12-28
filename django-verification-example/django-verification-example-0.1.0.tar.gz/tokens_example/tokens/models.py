from django.contrib.auth.models import User
from django.db import models
from django.db.transaction import atomic
from django.utils.timezone import now

from .utils import get_default_token_lifetime


class SecurityTokenManager(models.Manager):
    @atomic
    def use_token(self, issuer, action, raw_value):
        """
        Фактически расходует токен, удаляя экземпляр SecurityToken,
        хранящий соответствующие значения для параметров.

        Стоит отметить, что найденный экземпляр SecurityToken
        удаляется в любом случае:

          1. Если он просрочен, то его нужно удалить,
             потому что его хранение бессмысленно.

          2. Если он не просрочен, значит он должен
             быть удален из соображений одноразовости.

        В конечном итоге возвращается логическое значение, определяющее,
        валиден ли токен.
        """
        instance = self.filter(
            issuer=issuer,
            action=action,
            raw_value=raw_value).first()

        if instance is not None:
            instance.delete()
            return not instance.is_expired

        return False

    def delete_expired(self):
        """
        Utility-метод, предназначенный для периодического
        вызова, как часть регулярного обслуживания системы.

        Для этих целей это приложение имеет специальную
        management-команду (manage.py delete_expired_tokens).

        Благодаря ему происходит очистка базы от просроченных
        экземпляров SecurityToken.
        """
        expression = models.ExpressionWrapper(
            models.F("created_at") + models.F("lifetime"),
            models.DateTimeField()
        )
        self.annotate(expires_at=expression).filter(expires_at__lte=now()).delete()


class SecurityToken(models.Model):
    """
    Модель, представляющая одноразовый токен безопасности с
    ограниченным временем жизни.

    Наличие этой модели обусловлено необходимостью унифицировать
    хранение двух видов токенов, используемых в разных контекстах:
    цифровой и символьный.

    Хотелось бы отметить, что поле lifetime не определяет фактическое
    время жизни этого экземпляра. Это говорит о том, что он не будет
    удален сразу же, как только его время жизни истечет.

    Удаление экземпляра этой модели происходит двумя способами:

      1. Если к экземпляру произошло обращение с помощью
         SecurityToken.objects.use_token(). Но ясно, что система не может
         ограничиться лишь этим методом, ведь маловероятно, что обращение
         будет происходить ко всем просроченным экземплярам SecurityToken.

      2. Периодический вызов SecurityToken.objects.delete_expired() решает
         проблему, описанную в первом пункте, удаляя абсолюнто все просроченные
         экземпляры SecurityToken.

    Помимо вышеперечисленного, поле action может дезориентировать.
    Его предназначение заключается в том, чтобы идентифицировать экземпляр:
    было бы глупо, если бы пользователь, получив токен, предназначенный для
    восстановления пароля, мог бы изменить с его помощью адрес электронной почты.
    """
    action = models.CharField(max_length=40, db_index=True)
    raw_value = models.TextField(unique=True, db_index=True)
    lifetime = models.DurationField(default=get_default_token_lifetime)
    issuer = models.ForeignKey(User, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SecurityTokenManager()

    def __str__(self):
        return "{}; for {}; at {}".format(
            self.action,
            self.issuer.id,
            self.created_at.strftime("%d.%m.%Y %H:%M")
        )

    @property
    def is_expired(self):
        expiration_datetime = self.created_at + self.lifetime
        return now() > expiration_datetime