def convert_tuple_choices_to_option_list(tuple_choices):
    results = []
    for row in tuple_choices:
        option_dict = {
            "id": row[0],
            "value": row[1],
            row[0]: row[1]
        }
        results.append(option_dict)
    return results
