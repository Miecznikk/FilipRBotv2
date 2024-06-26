import yaml
from discord.ext.commands import check, CheckFailure


def get_member_nickname(dc_member):
    if dc_member.nick is not None:
        return dc_member.nick
    return dc_member.global_name


def convert_to_time(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60

    return f"{hours}h:{remaining_minutes}min"


def channel_check(channel_name):
    def predicate(ctx):
        return ctx.channel.name == channel_name

    return check(predicate)


def check_in_call(bot_instance):
    def predicate(ctx, *args):
        return not bot_instance.julia_call

    return check(predicate)


def check_in_game(bot_instance):
    def predicate(ctx, *args):
        return not bot_instance.in_game

    return check(predicate)


def load_commands_config():
    with open('utils/commands_config.yaml', 'r') as yaml_file:
        return yaml.safe_load(yaml_file)
