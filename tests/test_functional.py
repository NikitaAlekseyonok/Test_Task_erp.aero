import os
import pytest
from config.data import TEST_FILES_NAMES
from models.Ticket import Ticket
from tests.checks.ticket_form_checks import check_ticket_keys_match_the_template_keys


class TestTicketForm:

    @pytest.mark.parametrize("pdf_file_path", TEST_FILES_NAMES)
    def test_ticket_form(self, create_ticket_template, pdf_file_path):
        ticket_template = create_ticket_template
        pdf_file_absolute_path = os.path.abspath(pdf_file_path)
        ticket = Ticket(pdf_file_absolute_path)

        differences = check_ticket_keys_match_the_template_keys(ticket_template, ticket)
        assert len(differences) == 0, f"Формат файла отличается от шаблона. Различия в полях {differences}"
        assert len(ticket.tagged_by) != 0, "Нет данных с баркода tagged by"
        assert len(ticket.main_code) != 0, "Нет данных с баркода main code"
        assert len(ticket.title) != 0, "Нет главного заголовка"


