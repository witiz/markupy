import argparse
import sys

from .html import to_markupy


def main() -> None:
    parser = argparse.ArgumentParser(prog="html2markupy")

    parser.add_argument(
        "--selector",
        action=argparse.BooleanOptionalAction,
        help="Use the selector #id.class syntax instead of explicit `id` and `class_` attributes",
        default=True,
    )
    parser.add_argument(
        "--tag-prefix",
        action=argparse.BooleanOptionalAction,
        help="Output mode for imports of markupy elements",
        default=False,
    )
    parser.add_argument(
        "input",
        type=argparse.FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="input HTML from file or stdin",
    )

    args = parser.parse_args()
    try:
        html = args.input.read()
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)

    use_selector: bool = args.selector
    use_import_tag: bool = args.tag_prefix

    print(to_markupy(html, use_selector=use_selector, use_import_tag=use_import_tag))
