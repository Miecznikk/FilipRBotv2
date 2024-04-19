import random
from itertools import chain

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


class GetDefaultMessageView(APIView):
    keywords_dict = {
        JuliaRelatedMessage: ['julia', 'julk', 'julci'],
        AudiRelatedMessage: ['audi', 'whiteshark', 'white shark', 'bialy rekin', 'biały rekin'],
        PbRelatedMessage: ['pb', 'polibud', 'studia'],
        AlcoholRelatedMessage: ['piwo', 'piwko', 'piwka', 'piwa', 'wódka', 'wodka', 'wodke', 'wódke', 'wódki', 'wodki',
                                'alkohol'],
        GrubassyRelatedMessage: ['grubass'],
        GlucoseRelatedMessage: ['cukier', 'cukr', 'dzik', 'dziczek', 'witamin'],
        GreetingsRelatedMessage: ['siema', 'hej', 'czesc', 'czolem']
    }

    permission_classes = [IsAuthenticated]

    def get(self, request, user_name, message_content, roles_names=""):
        possible_tables = [key for key, value in self.keywords_dict.items() for val in value if val in message_content]
        if len(possible_tables) == 1:
            message = random.choice(possible_tables[0].objects.all())
            try:
                member = Member.objects.get(name=user_name)
                member_name = random.choice(member.nicknames.split(','))
            except Member.DoesNotExist:
                member_name = user_name
            return Response(message.format(member_name.upper()))

        else:
            try:
                member = Member.objects.get(name=user_name)
                roles = [role for role in roles_names.split(",")]
                roles_queryset = Role.objects.filter(name__in=roles)
                roles_related_messages = RoleDefaultMessage.objects.filter(role__in=roles_queryset)
            except Member.DoesNotExist:
                return Response(random.choice(DefaultMessage.objects.all()).format(user_name.upper()))

            combined_messages = list(chain(DefaultUserRelatedMessage.objects.filter(user=member),
                                           DefaultMessage.objects.all(),
                                           roles_related_messages))

            return Response(random.choice(combined_messages)
                            .format(random.choice(member.nicknames.split(','))).upper())
