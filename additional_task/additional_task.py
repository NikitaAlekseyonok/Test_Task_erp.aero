import re


table = [{'Columns View': 'SO Number', 'Sort By': '', 'Highlight By': 'equals=S110=rgba(172,86,86,1),equals=S111', 'Condition': 'equals=S110,equals=S111', 'Row Height': '60', 'Lines per page': '25'},
         {'Columns View': 'Client PO', 'Sort By': '', 'Highlight By': 'equals=P110,equals=P111', 'Condition': 'equals=P110', 'Row Height': '', 'Lines per page': ''},
         {'Columns View': 'Terms of Sale', 'Sort By': 'asc', 'Highlight By': 'equals=S110=rgba(172,86,86,1)', 'Condition': '', 'Row Height': '', 'Lines per page': ''}]

websocket_response = {'Client PO': {'index': 'so_list_client_po', 'filter': 'client_po'},
                      'SO Number': {'index': 'so_list_so_number', 'filter': 'so_no'},
                      'Terms of Sale': {'index': 'so_list_terms_of_sale', 'filter': 'term_sale'}}

base_ws = {'Columns View': 'columns',
           'Sort By': 'order_by',
           'Condition': 'conditions_data',
           'Lines per page': 'page_size',
           'Row Height': 'row_height',
           'Highlight By': 'color_conditions'}

result = {'columns': [{'index': 'so_list_so_number', 'sort': 0},
                      {'index': 'so_list_client_po', 'sort': 1},
                      {'index': 'so_list_terms_of_sale', 'sort': 2}],
          'order_by': {'direction': 'asc', 'index': 'so_list_terms_of_sale'},
          'conditions_data': {'so_no': [{'type': 'equals', 'value': 'S110'},
                                        {'type': 'equals', 'value': 'S111'}],
                              'client_po': [{'type': 'equals', 'value': 'P110'}]},
          'page_size': '25',
          'row_height': '60',
          'color_conditions': {'so_no': [{'type': 'equals', 'value': 'S110', 'color': 'rgba(172,86,86,1)'}, {'type': 'equals', 'value': 'S111', 'color': ''}],
                               'client_po': [{'type': 'equals', 'value': 'P110', 'color': ''}, {'type': 'equals', 'value': 'P111', 'color': ''}],
                               'term_sale': [{'type': 'equals', 'value': 'S110', 'color': 'rgba(172,86,86,1)'}]},
          'module': 'SO'}


def parse_conditions(conditions_str: str) -> [dict[str, str]]:
    conditions = []

    for condition in conditions_str.split(','):
        if '=' in condition:
            cond_type, cond_value = condition.split('=', 1)
            conditions.append({'type': cond_type, 'value': cond_value})

    return conditions


def parse_highlight_conditions(highlight_conditions_str: str) -> [dict[str, str]]:
    color_conditions = []
    pattern = r'(?<=\))\s*,\s*|,(?!\d)'

    for condition in re.split(pattern, highlight_conditions_str):
        values = condition.split('=')

        if len(values) == 2:
            color_conditions.append({'type': values[0], 'value': values[1], 'color': ''})

        if len(values) == 3:
            color_conditions.append({'type': values[0], 'value': values[1], 'color': values[2]})

    return color_conditions


def transform_table_to_request(table: [dict[str, str]], websocket_response: dict[str, dict[str, str]],
                               base_ws: dict[str, str]):
    columns = []
    order_by = {}
    conditions_data = {}
    color_conditions = {}

    for idx, row in enumerate(table):
        column_view = row.get('Columns View', '')

        if column_view in websocket_response:
            col_info = websocket_response[column_view]
            columns.append({'index': col_info['index'], 'sort': idx})

            if row.get('Sort By', ''):
                order_by = {'direction':  row['Sort By'], 'index': col_info['index']}

            condition_str = row.get('Condition', '')

            if condition_str:
                conditions_data[col_info['filter']] = parse_conditions(condition_str)

            highlight_str = row.get('Highlight By', '')

            if highlight_str:
                color_conditions[col_info['filter']] = parse_highlight_conditions(highlight_str)
            else:
                color_conditions[col_info['filter']] = []

    request_json = {
        base_ws['Columns View']: columns,
        base_ws['Sort By']: order_by,
        base_ws['Condition']: conditions_data,
        base_ws[ 'Lines per page']: table[0].get('Lines per page', ''),
        base_ws['Row Height']: table[0].get('Row Height', ''),
        base_ws['Highlight By']: color_conditions,
        'module': 'SO'
    }

    return request_json


result_request = transform_table_to_request(table, websocket_response, base_ws)

print(result_request == result)
