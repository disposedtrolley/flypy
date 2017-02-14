from datetime import datetime


def convert_str_to_date(str_to_convert):
    """This function converts a string to a datetime object.

    Args:
        str_to_convert (string): The string to convert in the format of
                                 <YYYY>-<MM>-<DD>
    Returns:
        datetime: The input string converted to a datetime object.

    """

    output = datetime.strptime(str_to_convert, "%Y-%m-%d")
    return output
