from django.db import models

from Members.models import Member


class UserFormatableMessage(models.Model):
    description = models.CharField(max_length=200)

    def format(self, user_nickname):
        return self.description.format(user_nickname)


class DefaultMessage(UserFormatableMessage):
    pass


class DefaultUserRelatedMessage(UserFormatableMessage):
    user = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, default=None)


class JuliaRelatedMessage(UserFormatableMessage):
    pass


class AudiRelatedMessage(UserFormatableMessage):
    pass


class PbRelatedMessage(UserFormatableMessage):
    pass


class AlcoholRelatedMessage(UserFormatableMessage):
    pass


class GrubassyRelatedMessage(UserFormatableMessage):
    pass


class GlucoseRelatedMessage(UserFormatableMessage):
    pass


class GreetingsRelatedMessage(UserFormatableMessage):
    pass

