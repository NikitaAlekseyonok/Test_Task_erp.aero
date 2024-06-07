from models import Ticket


def check_ticket_keys_match_the_template_keys(template_ticket: Ticket, ticket: Ticket) -> [()]:
    template_ticket_keys_coordinate = template_ticket.get_ticket_keys_coordinates()
    ticket.set_key_coordinates()
    ticket_keys_coordinate = ticket.get_ticket_keys_coordinates()

    differences = []

    for key in template_ticket_keys_coordinate:
        if template_ticket_keys_coordinate[key] != ticket_keys_coordinate[key]:
            differences.append((key, template_ticket_keys_coordinate[key], ticket_keys_coordinate[key]))

    return differences

