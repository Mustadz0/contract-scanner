#!/usr/bin/env python3
"""
Contract Clause Scanner — CLI

Usage:
  python cli.py contract.pdf
  python cli.py contract.docx --language ar
  python cli.py contract.txt --language fr --output report.json
  python cli.py contract.pdf --no-color
"""

import argparse
import json
import sys
from pathlib import Path

from core.parser import extract_text
from core.analyzer import ContractAnalyzer


def colorize(severity: str) -> tuple:
    colors = {
        "CRITICAL": ("\033[1;41m", "\033[0m"),
        "HIGH": ("\033[1;31m", "\033[0m"),
        "MEDIUM": ("\033[1;33m", "\033[0m"),
        "LOW": ("\033[1;32m", "\033[0m"),
    }
    return colors.get(severity.upper(), ("", ""))


def print_report(result: dict, use_color: bool = True):
    level = result.get("risk_level", "UNKNOWN")
    score = result.get("overall_risk_score", 0)

    if use_color:
        start, end = colorize(level)
        print(f"\n{'='*60}")
        print(f"  RISK SCORE: {start} {score}/100 ({level}) {end}")
    else:
        print(f"\n{'='*60}")
        print(f"  RISK SCORE: {score}/100 ({level})")
    print(f"{'='*60}")
    print(f"  Summary: {result.get('summary', 'N/A')}")

    flags = result.get("red_flags", [])
    if flags:
        for i, flag in enumerate(flags, 1):
            sev = flag.get("severity", "LOW")
            if use_color:
                s, e = colorize(sev)
                print(f"\n  [{s} {sev} {e}] Flag #{i}")
            else:
                print(f"\n  [{sev}] Flag #{i}")
            print(f"  Clause:    {flag.get('clause', '')[:120]}")
            print(f"  Why risky: {flag.get('why_risky', '')}")
            tip = flag.get("negotiation_tip", "")
            if tip:
                print(f"  Suggestion: {tip}")

    watch = result.get("key_watchpoints", [])
    if watch:
        print(f"\n{'='*60}")
        print("  WATCH OUT FOR:")
        for w in watch:
            print(f"    * {w}")

    steps = result.get("next_steps", [])
    if steps:
        print(f"\n{'='*60}")
        print("  NEXT STEPS:")
        for s in steps:
            print(f"     ->  {s}")

    print()


def main():
    ap = argparse.ArgumentParser(
        description="AI-powered contract clause scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py contract.pdf
  python cli.py contract.docx --language ar
  python cli.py contract.txt --output report.json
        """,
    )
    ap.add_argument("input", type=Path, help="Contract file (.pdf, .docx, .txt)")
    ap.add_argument("--language", "-l", default="en", choices=["en", "ar", "fr", "es", "de", "tr"], help="Output language")
    ap.add_argument("--output", "-o", type=Path, help="Save report as JSON")
    ap.add_argument("--no-color", action="store_true", help="Disable colored output")

    args = ap.parse_args()

    if not args.input.exists():
        print(f"Error: file not found: {args.input}")
        sys.exit(1)

    print(f"[FILE] Reading: {args.input}")
    try:
        text = extract_text(args.input)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    print(f"[OK] Extracted {len(text)} characters")
    print(f"[AI] Analyzing with Gemini AI...")

    try:
        analyzer = ContractAnalyzer()
        result = analyzer.analyze(text, language=args.language)
    except Exception as e:
        print(f"Analysis error: {e}")
        sys.exit(1)

    if args.output:
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[SAVED] Report saved: {args.output}")

    print_report(result, use_color=not args.no_color)


if __name__ == "__main__":
    main()
