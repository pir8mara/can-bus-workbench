from can_workbench.candump import read_candump
from can_workbench.report import build_report


def test_report_contains_ids():
    frames = read_candump("examples/sample_candump.log")
    report = build_report(frames)
    assert "0x123" in report
    assert "0x456" in report
    assert "0x18FEF100" in report
    assert "Total frames: 7" in report
