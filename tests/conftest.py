import os
import pytest
from models.Ticket import Ticket
from config.data import TEMPLATE_FILE_NAME


@pytest.fixture(scope="session")
def create_ticket_template():
    absolute_path = os.path.abspath(TEMPLATE_FILE_NAME)
    ticket_template = Ticket(absolute_path)
    ticket_template.set_key_coordinates()

    yield ticket_template
