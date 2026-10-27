#!/usr/bin/env python3

import argparse
import json
import os
import re
import subprocess
import sys


def extract_section(header, text):
    pattern = rf"### {header}\s*(.*?)(?=\n### |\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None


def clean_cpuinfo(cpuinfo_raw):
    code_block_match = re.search(r"```[a-z]*\n(.*?)```",
                                 cpuinfo_raw, re.DOTALL)
    if code_block_match:
        return code_block_match.group(1).strip()
    return cpuinfo_raw


def parse_issue_body(body):
    vendor = extract_section("Vendor", body)
    soc = extract_section("SoC Name", body)
    extra_info = extract_section("Extra info", body)
    cpuinfo_raw = extract_section("/proc/cpuinfo dump", body)

    if not vendor or not soc or not cpuinfo_raw:
        print("Failed to parse required fields"
              " (Vendor, SoC Name, or cpuinfo dump)"
              " from the issue body.")
        sys.exit(1)

    cpuinfo_clean = clean_cpuinfo(cpuinfo_raw)
    return vendor, soc, extra_info, cpuinfo_clean


def parse_github_event():
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    if not event_path or not os.path.exists(event_path):
        print("GITHUB_EVENT_PATH not set or file does not exist.")
        sys.exit(1)

    with open(event_path, 'r', encoding='utf-8') as f:
        event_data = json.load(f)

    body = event_data.get('issue', {}).get('body', '')
    if not body:
        print("No issue body found in the event JSON.")
        sys.exit(1)

    return parse_issue_body(body)


def get_issue_number():
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    if not event_path or not os.path.exists(event_path):
        return None
    with open(event_path, 'r', encoding='utf-8') as f:
        event_data = json.load(f)
    return event_data.get('issue', {}).get('number')


def comment_on_issue(issue_number, body):
    repo = os.environ.get('GITHUB_REPOSITORY')
    if not repo or not issue_number:
        return
    cmd = [
        'gh', 'issue', 'comment',
        str(issue_number),
        '--repo', repo,
        '--body', body,
    ]
    subprocess.run(cmd, check=False)


def parse_missing_cores(output):
    missing = []
    for line in output.splitlines():
        if 'is missing' in line:
            missing.append(line.strip())
    return missing


def run_import(vendor, soc, extra_info, cpuinfo_text):
    cpuinfo_file = 'temp_cpuinfo.txt'
    with open(cpuinfo_file, 'w') as f:
        f.write(cpuinfo_text)

    print(f"Vendor: {vendor}")
    print(f"SoC: {soc}")
    ei = extra_info if extra_info else 'None'
    print(f"Extra info: {ei}")

    cmd = [
        'python', 'import-cpuinfo.py',
        cpuinfo_file, soc, vendor,
    ]
    print(f"Running command: {' '.join(cmd)}")

    result = subprocess.run(
        cmd, capture_output=True, text=True,
    )
    if result.returncode != 0:
        output = result.stdout + result.stderr
        missing = parse_missing_cores(output)
        if missing:
            print("Missing CPU core information:")
            for m in missing:
                print(f"  {m}")
            issue_number = get_issue_number()
            if issue_number:
                lines = '\n'.join(f'- {m}' for m in missing)
                body = (
                    "Import failed due to missing"
                    " CPU core information in the"
                    " database:\n\n"
                    f"{lines}\n\n"
                    "This needs to be added to"
                    " `data/cpu_cores.yml`"
                    " before import can proceed."
                )
                comment_on_issue(issue_number, body)
        else:
            print("Error running import-cpuinfo.py:")
            print(output)
        sys.exit(1)

    print("Script output:")
    print(result.stdout)

    return vendor, soc, extra_info


def export_github_env(vendor, soc, extra_info):
    env_file = os.environ.get('GITHUB_ENV')
    if not env_file:
        return

    with open(env_file, 'a') as f:
        f.write(f"SOC_VENDOR={vendor}\n")
        f.write(f"SOC_NAME={soc}\n")

        if extra_info:
            f.write("EXTRA_INFO<<EOF_EXTRA\n")
            f.write(f"{extra_info}\n")
            f.write("EOF_EXTRA\n")


def main():
    parser = argparse.ArgumentParser(
        description="Process cpuinfo data from a GitHub issue or direct input"
    )
    parser.add_argument(
        "--issue-body", type=str,
        help="Path to file with GitHub issue body text",
    )
    parser.add_argument("--vendor", type=str, help="SoC vendor name")
    parser.add_argument("--soc", type=str, help="SoC name")
    parser.add_argument("--cpuinfo", type=str,
                        help="Path to cpuinfo dump file")
    parser.add_argument(
        "--extra-info", type=str,
        help="Extra information about the SoC",
    )
    args = parser.parse_args()

    if args.issue_body:
        with open(args.issue_body, 'r', encoding='utf-8') as f:
            body = f.read()
        vendor, soc, extra_info, cpuinfo_text = parse_issue_body(body)
    elif args.vendor and args.soc and args.cpuinfo:
        vendor = args.vendor
        soc = args.soc
        extra_info = args.extra_info
        with open(args.cpuinfo, 'r', encoding='utf-8') as f:
            cpuinfo_text = f.read()
    elif os.environ.get('GITHUB_EVENT_PATH'):
        vendor, soc, extra_info, cpuinfo_text = parse_github_event()
    else:
        parser.print_help()
        print("\nProvide either --issue-body, or --vendor/--soc/--cpuinfo, "
              "or set GITHUB_EVENT_PATH.")
        sys.exit(1)

    run_import(vendor, soc, extra_info, cpuinfo_text)
    export_github_env(vendor, soc, extra_info)


if __name__ == '__main__':
    main()
