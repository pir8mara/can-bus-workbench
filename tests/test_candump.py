from can_workbench.candump import parse_candump_line


def test_parse_candump_with_timestamp():
    frame = parse_candump_line("(1718990000.123456) can0 123#DEADBEEF")
    assert frame is not None
    assert frame.timestamp == 1718990000.123456
    assert frame.channel == "can0"
    assert frame.arbitration_id == 0x123
    assert frame.data == bytes.fromhex("DEADBEEF")
    assert frame.is_extended_id is False


def test_parse_extended_id():
    frame = parse_candump_line("can0 18FEF100#1122334455667788")
    assert frame is not None
    assert frame.arbitration_id == 0x18FEF100
    assert frame.is_extended_id is True


def test_parse_comment_returns_none():
    assert parse_candump_line("# comment") is None
