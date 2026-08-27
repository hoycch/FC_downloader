#!/usr/bin/env python3
"""
csv_to_org_json.py
Convert organization CSV (pid → userId hierarchy) into nested JSON
with Chinese field names, sorted by 開戶時間.

Usage:
  python csv_to_org_json.py [input.csv] [output.json]

Expected CSV columns:
  name, userId, pid, Phone, AccCreateTime,
  teamTotalNumber, personalTotalRecharge, personalTotalWithdrawal,
  personalKickback, teamTotalRecharge, teamTotalWithdrawal
"""

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime

MAIN_ROOT_NAMES = {"港澳頭目", "新加坡頭目", "韓國頭目"}


def to_number(val):
    if val is None or str(val).strip() == "":
        return 0
    try:
        s = str(val).strip().replace(",", "")
        return float(s) if "." in s else int(s)
    except (ValueError, TypeError):
        return 0


def parse_time(s):
    if not s or not str(s).strip():
        return ""
    s = str(s).strip()
    for fmt in (
        "%m/%d/%Y %I:%M:%S %p",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%m/%d/%Y %H:%M",
    ):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return s


def has_path(start, target, graph, visited=None):
    if visited is None:
        visited = set()
    if start == target:
        return True
    if start in visited:
        return False
    visited.add(start)
    for child in graph.get(start, []):
        if has_path(child, target, graph, visited):
            return True
    return False


def convert(csv_path: str, json_path: str, keep_all_roots: bool = False):
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    nodes = {}
    children_map = defaultdict(list)
    roots = []
    masked_counter = 0

    for row in rows:
        raw_uid = (row.get("userId") or "").strip()
        raw_pid = (row.get("pid") or "").strip().strip('"')

        if raw_uid.isdigit():
            key = int(raw_uid)
        else:
            masked_counter += 1
            key = f"masked_{masked_counter}"

        pid = int(raw_pid) if raw_pid.isdigit() else None
        if pid is not None and pid == key:  # self-ref
            pid = None

        node = {
            "名稱": (row.get("name") or "").strip() or None,
            "用戶ID": key if isinstance(key, int) else None,
            "電話": (
                (row.get("Phone") or "").strip()
                if (row.get("Phone") or "").strip() not in ("****", "")
                else None
            ),
            "開戶時間": parse_time(row.get("AccCreateTime")),
            "個人總充值": to_number(row.get("personalTotalRecharge")),
            "個人總提現": to_number(row.get("personalTotalWithdrawal")),
            "個人返佣": to_number(row.get("personalKickback")),
            "團隊總人數": to_number(row.get("teamTotalNumber")),
            "團隊總充值": to_number(row.get("teamTotalRecharge")),
            "團隊總提現": to_number(row.get("teamTotalWithdrawal")),
            "children": [],
            "_key": key,
            "_sort": parse_time(row.get("AccCreateTime")),
        }
        nodes[key] = node

        if pid is None:
            roots.append(key)
        else:
            children_map[pid].append(key)

    # Attach children while avoiding cycles
    safe_children = defaultdict(list)
    for parent_id, child_keys in children_map.items():
        if parent_id not in nodes:
            for ck in child_keys:
                if ck not in roots:
                    roots.append(ck)
            continue
        for ck in child_keys:
            if has_path(ck, parent_id, safe_children):
                print(f"  Cycle avoided: {ck} → {parent_id}")
                continue
            safe_children[parent_id].append(ck)

    for parent_id, child_keys in safe_children.items():
        for ck in child_keys:
            nodes[parent_id]["children"].append(nodes[ck])

    tree = []
    seen = set()
    for rid in roots:
        if rid in nodes and rid not in seen:
            tree.append(nodes[rid])
            seen.add(rid)

    if keep_all_roots:
        main_roots = tree
    else:
        main_roots = [n for n in tree if n.get("名稱") in MAIN_ROOT_NAMES]
        if not main_roots:
            main_roots = [n for n in tree if n.get("名稱")]

    def sort_and_clean(node, path=None):
        if path is None:
            path = set()
        k = node.get("_key")
        if k in path:
            return
        path = path | {k}
        node["children"].sort(key=lambda x: x.get("_sort") or "")
        node["children"] = [c for c in node["children"] if c.get("_key") != k]
        for c in node["children"]:
            sort_and_clean(c, path)
        node.pop("_key", None)
        node.pop("_sort", None)

    for r in main_roots:
        sort_and_clean(r)

    virtual = {
        "名稱": "頂層",
        "用戶ID": None,
        "電話": None,
        "開戶時間": "",
        "個人總充值": 0,
        "個人總提現": 0,
        "個人返佣": 0,
        "團隊總人數": 0,
        "團隊總充值": 0,
        "團隊總提現": 0,
        "children": main_roots,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(virtual, f, ensure_ascii=False, indent=2)

    print(f"Wrote {json_path}")
    print(f"  CSV rows     : {len(rows)}")
    print(f"  Masked nodes : {masked_counter}")
    print(f"  Main roots   : {[r.get('名稱') for r in main_roots]}")


if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "full_top4_layers.csv"
    json_file = sys.argv[2] if len(sys.argv) > 2 else "org_data.json"
    convert(csv_file, json_file)
