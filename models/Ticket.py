from typing import Any
from config.data import KEYS_LIST
from helpers.file_helper import extract_text_from_pdf, render_pdf_to_images, decode_barcodes, find_text_coordinates


class Ticket:

    def __init__(self, pdf_file_path: str) -> None:
        self.pdf_file_path = pdf_file_path
        self._data = self.__create_ticket_property_dict_from_pdf_file(self.pdf_file_path, KEYS_LIST)

    @property
    def title(self) -> str:
        return self._data['title']['data']

    @property
    def main_code(self) -> str:
        return self._data['main_code']['data']

    @property
    def pn(self) -> str:
        return self._data['PN']['data']

    @property
    def sn(self) -> str:
        return self._data['SN']['data']

    @property
    def description(self) -> str:
        return self._data['DESCRIPTION']['data']

    @property
    def location(self) -> str:
        return self._data['LOCATION']['data']

    @property
    def condition(self) -> str:
        return self._data['CONDITION']['data']

    @property
    def receiver(self) -> str:
        return self._data['RECEIVER#']['data']

    @property
    def uom(self) -> str:
        return self._data['UOM']['data']

    @property
    def exp_date(self) -> str:
        return self._data['EXP DATE']['data']

    @property
    def po(self) -> str:
        return self._data['PO']['data']

    @property
    def cert_source(self) -> str:
        return self._data['CERT SOURCE']['data']

    @property
    def rec_date(self) -> str:
        return self._data['REC.DATE']['data']

    @property
    def mfg(self) -> str:
        return self._data['MFG']['data']

    @property
    def batch(self) -> str:
        return self._data['BATCH#']['data']

    @property
    def dom(self) -> str:
        return self._data['DOM']['data']

    @property
    def remark(self) -> str:
        return self._data['REMARK']['data']

    @property
    def lot(self) -> str:
        return self._data['LOT#']['data']

    @property
    def tagged_by(self) -> str:
        return self._data['TAGGED BY']['data']

    @property
    def qty(self) -> str:
        return self._data['Qty']['data']

    @property
    def notes(self) -> str:
        return self._data['NOTES']['data']

    def set_key_coordinates(self) -> None:
        for key in KEYS_LIST:
            self._data[key]['rect'] = find_text_coordinates(self.pdf_file_path, key)

        self._data['title']['rect'] = find_text_coordinates(self.pdf_file_path, self._data['title']['data'])

    def get_ticket_keys_coordinates(self) -> dict[str, Any]:
        keys_coordinate = {}

        for key in KEYS_LIST:
            keys_coordinate[key] = self._data[key]['rect']

        return keys_coordinate

    @staticmethod
    def __create_ticket_property_dict_from_pdf_file(pdf_file_path: str, substrings: [str]) -> dict[dict[str, str]]:
        pdf_text = extract_text_from_pdf(pdf_file_path)
        result = {}
        start_index = None

        for substring in substrings:
            start_index = pdf_text.find(substring, start_index) + len(substring) + 1
            if start_index == -1:
                raise ValueError("Некорректное значение для текста!")

            if substrings.index(substring) == 0:
                result['title'] = {'data': pdf_text[0:pdf_text.find(substring, 0)].replace(':', '').strip()}

            if substrings.index(substring) != len(substrings) - 1:
                end_index = pdf_text.find(substrings[substrings.index(substring) + 1], start_index)
                if end_index == -1:
                    result[substring] = {'data': pdf_text[start_index:].replace(':', '').strip()}
                else:
                    result[substring] = {'data': pdf_text[start_index:end_index].replace(':', '').strip()}
            else:
                result[substring] = {'data': pdf_text[start_index:].replace(':', '').strip()}

        images = render_pdf_to_images(pdf_file_path)
        decode_result = decode_barcodes(images)

        try:
            result['main_code'] = decode_result[0]
            result['TAGGED BY'] = decode_result[1]
        except IndexError:
            print(f"Ошибка! В файле {len(decode_result)} баркода.")

        return result
