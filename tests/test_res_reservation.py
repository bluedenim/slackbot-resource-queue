from van.res_reservation import ResourceReservationProcessor


def test_hello(reservation_processor: ResourceReservationProcessor):
    responses = reservation_processor.hello(['printer2'], {'user_id': 'user_3', 'web_client': object()})
    assert responses[0] == 'Hello back, Real User 3!'


def test_add(reservation_processor: ResourceReservationProcessor):
    queue_for_printer_2 = reservation_processor.reservations.resources['printer2']
    assert len(queue_for_printer_2) == 1
    assert 'user_1' in queue_for_printer_2

    assert reservation_processor.add(['printer2'], {'user_id': 'user_3', 'web_client': object()})

    assert len(queue_for_printer_2) == 2
    assert 'user_1' in queue_for_printer_2
    assert 'user_3' in queue_for_printer_2


def test_status(reservation_processor: ResourceReservationProcessor):
    response = reservation_processor.status([], {'user_id': 'user_3', 'web_client': object()})

    assert len(response) == 2
    assert response[0] == '*printer*: Real User 1, Real User 2'
    assert response[1] == '*printer2*: Real User 1'


def test_remove(reservation_processor: ResourceReservationProcessor):
    queue_for_printer = reservation_processor.reservations.resources['printer']
    assert len(queue_for_printer) == 2
    assert 'user_1' in queue_for_printer
    assert 'user_2' in queue_for_printer

    assert reservation_processor.remove(['printer'], {'user_id': 'user_1', 'web_client': object()})

    assert len(queue_for_printer) == 1
    assert 'user_1' not in queue_for_printer
    assert 'user_2' in queue_for_printer


def test_remove_all(reservation_processor: ResourceReservationProcessor):
    queue_for_printer_2 = reservation_processor.reservations.resources['printer2']
    assert len(queue_for_printer_2) == 1
    assert 'user_1' in queue_for_printer_2

    assert reservation_processor.remove_all(['printer2'], {'user_id': 'user_3', 'web_client': object()})

    queue_for_printer_2 = reservation_processor.reservations.resources['printer2']
    assert len(queue_for_printer_2) == 0


def test_help(reservation_processor: ResourceReservationProcessor):
    response = reservation_processor.help([], {})
    assert len(response) == len(reservation_processor.command_handlers.keys())


def test_get_handler_method(reservation_processor: ResourceReservationProcessor):
    assert reservation_processor._get_handler_method('hello') == reservation_processor.hello
    assert reservation_processor._get_handler_method('add') == reservation_processor.add
    assert reservation_processor._get_handler_method('status') == reservation_processor.status
    assert reservation_processor._get_handler_method('remove') == reservation_processor.remove
    assert reservation_processor._get_handler_method('remove-all') == reservation_processor.remove_all
    assert reservation_processor._get_handler_method('help') == reservation_processor.help


def test_process_message_text(reservation_processor: ResourceReservationProcessor):
    response = reservation_processor.process_message_text(
        ['add', 'scanner'],
        {
            'user_id': 'user_1',
            'web_client': object(),
        }
    )
    assert response[0] == 'Real User 1 queued for resource *scanner*'
