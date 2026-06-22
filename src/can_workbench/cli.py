from __future__ import annotations

import argparse
from pathlib import Path
from .candump import read_candump
from .capture import capture_socketcan
from .decode import decode_with_dbc
from .llm import build_prompt_pack
from .models import load_jsonl, write_jsonl
from .report import build_report


def cmd_import_candump(args: argparse.Namespace) -> None:
    frames = read_candump(args.input)
    write_jsonl(args.output, frames)
    print(f"Imported {len(frames)} frames -> {args.output}")


def cmd_analyze(args: argparse.Namespace) -> None:
    frames = load_jsonl(args.input)
    report = build_report(frames)
    Path(args.output).write_text(report, encoding="utf-8")
    print(f"Wrote report -> {args.output}")


def cmd_decode(args: argparse.Namespace) -> None:
    frames = load_jsonl(args.input)
    decoded, unknown = decode_with_dbc(frames, args.dbc, args.output)
    print(f"Decoded {decoded} frames, skipped {unknown} unknown/failed frames -> {args.output}")


def cmd_capture(args: argparse.Namespace) -> None:
    count = capture_socketcan(args.channel, args.output, args.duration)
    print(f"Captured {count} frames -> {args.output}")


def cmd_prompt_pack(args: argparse.Namespace) -> None:
    report = Path(args.input).read_text(encoding="utf-8")
    prompt = build_prompt_pack(report)
    Path(args.output).write_text(prompt, encoding="utf-8")
    print(f"Wrote prompt pack -> {args.output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="canwb", description="Local CAN bus workbench")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("import-candump", help="Convert candump text logs to JSONL")
    p.add_argument("input")
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_import_candump)

    p = sub.add_parser("analyze", help="Generate a Markdown traffic report")
    p.add_argument("input")
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_analyze)

    p = sub.add_parser("decode", help="Decode JSONL frames using a DBC file")
    p.add_argument("input")
    p.add_argument("--dbc", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_decode)

    p = sub.add_parser("capture", help="Passive capture from a SocketCAN interface")
    p.add_argument("--channel", default="can0")
    p.add_argument("--output", required=True)
    p.add_argument("--duration", type=float, default=30.0)
    p.set_defaults(func=cmd_capture)

    p = sub.add_parser("prompt-pack", help="Create a local-LLM analysis prompt from a report")
    p.add_argument("input")
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_prompt_pack)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
