def get_member_nickname(dc_member):
    if dc_member.nick is not None:
        return dc_member.nick
    return dc_member.global_name


def convert_to_time(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60

    return f"{hours} h, {remaining_minutes} min"
