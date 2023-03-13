def convert_tuple_or_list_to_options(values):
    result_list = []
    result_dict = {}
    for row in values:
        option_dict = {
            "id": row[0],
            "name": row[1],
        }
        result_list.append(option_dict)
        result_dict[row[0]] = row[1]
    return result_list, result_dict
