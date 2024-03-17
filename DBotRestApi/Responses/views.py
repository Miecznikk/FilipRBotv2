import random
from itertools import chain

from django.db.models import Q
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from Members.models import Member
from .models import *


# Create your views here.

class GetDefaultMessageView(APIView):
    keywords_dict = {
        JuliaRelatedMessage: ['julia', 'julka', 'julk', 'julci'],
        AudiRelatedMessage: ['audi', 'whiteshark', 'white shark', 'bialy rekin', 'biały rekin'],
        PbRelatedMessage: ['pb', 'polibud', 'studia'],
        AlcoholRelatedMessage: ['piwo', 'piwko', 'wódka', 'wodka', 'wodke', 'wódke', 'alkohol'],
        GrubassyRelatedMessage: ['grubass'],
        GlucoseRelatedMessage: ['cukier', 'cukr', 'dzik', 'dziczek'],
        GreetingsRelatedMessage: ['siema', 'hej', 'czesc', 'czolem']
    }

    def get(self, request, user_name, message_content):
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
            except Member.DoesNotExist:
                return Response(random.choice(DefaultMessage.objects.all()).format(user_name.upper()))

            combined_messages = list(chain(DefaultUserRelatedMessage.objects.filter(user=member),
                                           DefaultMessage.objects.all()))

            return Response(random.choice(combined_messages)
                            .format(random.choice(member.nicknames.split(','))).upper())
