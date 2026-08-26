#!/usr/bin/env python3
"""Usage examples for config + header builder."""

from library import get_config, build_headers, generate_config_snippet


def main() -> None:
    # 1. Load config for a given area_code (this is where area_code is used)
    cfg = get_config(65)

    # 2. Build headers from config only (all values come from config.py)
    headers = build_headers(cfg)
    # print("=== Headers from config ===")
    # for k, v in headers.items():
    #     print(f"{k}: {v}")
    # print()

    # 3. Optional extra headers dict (merged on top; overrides on conflict)
    headers_extra = build_headers(
        cfg,
        extra_headers={
            "x-custom-token": "abc123",
            "referer": "https://example.com/",
            "content-type": "application/json",
        },
    )
    print("=== Headers with extra_headers ===")
    for k, v in headers_extra.items():
        print(f"{k}: {v}")
    print()

    # 4. Generate a traditional-looking config.py snippet
    print("=== Generated config snippet (area_code=65) ===")
    print(generate_config_snippet(65))


if __name__ == "__main__":
    main()
