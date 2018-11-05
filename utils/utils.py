
def format_name_to_display(name):
    formatted_name = name.replace("_", " ").replace("-", " ").split()
    return " ".join([x.capitalize() for x in formatted_name])

def format_name_to_query(name):
    formatted_name = name.replace(" ", "_").replace(" ", "_").split()
    return "_".join([x.lower() for x in formatted_name])
