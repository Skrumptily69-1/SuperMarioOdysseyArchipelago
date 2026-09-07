#!/usr/bin/env python3
"""Generate formatted Switch-runtime logic tables from authored CSVs."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

default_progression = [0, 1, 2, 3]
scenario_progression: dict[str, list[int]] = {
    "cap": default_progression,
    "cascade": default_progression,
    "sand": [0, 1, 2, 3, 4],
    "wooded": [0, 1, 2, 3, 4],
    "lake": default_progression,
    "cloud": default_progression,
    "lost": default_progression,
    "metro": [0, 1, 3, 4, 7], # Not sure if the "festival" scenario needs to be included here, if it is needed, its [0, 1, 2, 3, 4, 7]
    "seaside": default_progression,
    "snow": default_progression,
    "luncheon": [0, 1, 6, 2, 7], # If Bruncheon needs to be included, append '9' to the start of the list
    "ruined": default_progression,
    "bowsers": default_progression,
    "moon": [0, 1, 2],
    "mushroom": [0, 1, 2],
    "dark": [0, 1],
    "darker": [0, 1]
}

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
INVALID_CHARS = '@<>:"/\\|?!*\'(),ã©'

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))

def format_name(value: str, region: bool = False) -> str:
    for char in INVALID_CHARS:
        value = value.replace(char, "")
    snake_case = re.sub(r"(?<=[a-z])(?=[A-Z])|\.\.\.", " ", value).lower()
    result = re.sub(r"\s?-\s?|\s", "_", snake_case).strip().replace("&", "and").replace("é", "e").replace("time_", "timer_").replace("valleyball", "volleyball")
    if region:
        result = re.sub(r"_free$|_obj[0-9]+$", "", result)
    return result

difficulty_dict: dict[str, str] = {
    "casual": "",
    "advanced": "intermediate_tricks",
    "expert": "hard_tricks",
    "glitched": "easy_glitches"
}

def get_logic_reqs(logic: str, difficulty_options: str, available_scenarios: str, option_scenarios: str) -> tuple[list[list[str]], list[int]]:
    difficulties: list[str] = difficulty_options.split(";")
    methods: list[str] = re.sub("[()]", "", logic).split(" | ")
    available_scenario_list = []
    if available_scenarios:
        available_scenario_list = [int(id)-1 for id in available_scenarios.split(";") if int(id) > 0]
        available_scenario_list.sort()
    if option_scenarios:
        scenario_lists: list[list[int]] = [
            [int(id)-1 for id in scenario_list.split(",") if int(id) > 0]
            for scenario_list in option_scenarios.split(";")]
        [list.sort() for list in scenario_lists]
        if len(scenario_lists) > 1 and len(methods) == len(scenario_lists):
            methods = [f"{f"{method} & " if len(methods) else ""}StoryProgress_{scenarios}" for method, scenarios in zip(methods, scenario_lists, strict=True)]
        else:
            available_scenario_list = scenario_lists[0]


    if(len(difficulties) != len(methods)):
        difficulties = [difficulties[0]] * len(methods)

    return [[*method.split(" & "), *([difficulty_dict[difficulty]] if difficulty != "casual" else [])]
            for method, difficulty in zip(methods, difficulties, strict=True)], available_scenario_list

def create_rule(reqs: list[list[str]], token_names: dict[str, str], captures: list[str], region_names: dict[str, str], scenario_list: list[int] = [], kingdom: str = "") -> str:
    methods: list[str] = []
    for token_list in reqs:
        tokens = [token for token in token_list if token and not token.startswith("RequiresDeath")]
        if tokens[0] == "free":
            if len(tokens) > 1 and tokens[1].startswith("Story"):
                scenario_list = [int(scenario) for scenario in tokens[1].split("_")[1].strip("[]").split(",")]
                if scenario_list:
                    break
            return "True_()"
        if tokens[0] == "impossible":
            return "False_()"

        scenario_rule: str | None = None
        scenarios: str | None = next(iter([
            m.group(1)
            for token in tokens
            if (m := re.search(r"StoryProgress_(.+)", token))
        ]), None)
        if scenarios:
            scenario_list = [int(scenario) for scenario in scenarios.strip("[]").split(",") if int(scenario) in scenario_progression[kingdom]]

            scenario_rule = f"HasStoryProgress('{kingdom}', {scenario_list})" if scenario_list != scenario_progression[kingdom] else None
        min_hp_rule: str | None = next(iter([
            f"HasHP({int(m.group(1))})"
            for token in tokens
            if (m := re.search(r"MinHp(\d)", token))
        ]), None)

        kingdom_access_rules: list[str] = [
            f"CanReachRegion(regions.region_names['{region_names.get(token.replace('@', ''), '')}'])"
            for token in tokens
            if token.startswith("@")
        ]
        capture_rules: list[str] = [
            f"CanCapture(tokens.{token_names[token]})"
            for token in tokens
            if (token in captures)
        ]

        if kingdom_access_rules or capture_rules or scenarios or min_hp_rule:
            if scenario_rule:
                scenario_list = []
            tokens = [
                token for token in tokens
                if not re.search(r"@|StoryProgress_|MinHp", token) and token not in captures
                ]

        method = ""
        if tokens:
            method += f"{'HasAll(' if len(tokens) > 1 else 'Has('}{', '.join([
                f'tokens.{token_names[token]}'
                for token in tokens
            ])})"

        if kingdom_access_rules or capture_rules or scenario_rule or min_hp_rule:
            rules = kingdom_access_rules + capture_rules + ([scenario_rule] if scenario_rule else []) + ([min_hp_rule] if min_hp_rule else []) + ([method] if method else [])
            if len(rules) > 1:
                method = f"And({','.join(rules)})"
            else:
                method = rules[0]

        methods.append(method)
    if len(reqs) > 1:
        method_str = ",\n".join(methods)
        result = f"Or(\n{method_str}\n)"
    else:
        result = methods[0]
    if scenario_list:
        scenario_list = [scenario for scenario in scenario_list if scenario in scenario_progression[kingdom]]
        if scenario_list != scenario_progression[kingdom]:
            result = f"{f'And(\n{result},\n' if result else ''}HasStoryProgress('{kingdom}', {scenario_list}){'\n)' if result else ''}"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate RuleData.py")
    parser.add_argument("--input", type=Path, default=Path("templates"))
    parser.add_argument("--output", type=Path, default=Path("generated"))
    args = parser.parse_args()

    root = args.input
    moon_rows = read_csv(root / "moon_access.csv")
    token_data = read_csv(root / "logic_tokens.csv")
    node_data = read_csv(root / "logic_nodes.csv")
    connection_rows = read_csv(root / "route_edges.csv")
    token_names: dict[str, str] = {
        "intermediate_tricks": "intermediate_tricks",
        "hard_tricks": "hard_tricks",
        "easy_glitches": "easy_glitches"
    }
    captures: list[str] = []
    for row in token_data:
        token_names[row["token"]] = format_name(row["display_name"])
        if row["token_type"] == "capture":
            captures.append(row["token"])
    # coverage for inconsistencies between secret dev and our item names
    token_names["SingleJump"] = "jump"
    token_names["trex"] = "t_rex"

    region_names: dict[str, str] = {}
    for row in node_data:
        region_names[row["node_id"]] = format_name(f"{row['stage_display_name']} {row['display_name']}", True)
    region_moons: dict[str, dict[str, int]] = {}

    output: list[str] = []
    output.append("from rule_builder.rules import *\n")
    output.append("from .TokenNames import SMOTokenNames as tokens\n")
    output.append("from .RegionData import SMORegionData as regions\n")
    output.append("from ....Rules import CanCapture, HasStoryProgress\n")
    output.append("from ...LocationData import SMOLocationData as loc")
    output.append("\nmoon_rule_data : dict[str, Rule] = {\n")
    moons: list[str] = []
    moon_ids: dict[str, int] = {}
    for moon in moon_rows:
        moon_data = ""
        moon_name = format_name(moon.get("moon_name", ""))
        reqs, scenario_list = get_logic_reqs(moon.get("requirement_expr", ""), moon.get("difficulty", ""), moon.get("shine_info_available_scenarios", ""), moon.get("option_scenarios", ""))
        moon_id = int(moon.get("uid", 0))
        if(moon_name[0] == "2"):
            moon_name = moon_name.replace("2d", "dot")
        moon_ids[moon_name] = moon_id

        dict = region_moons.get(region_names[moon.get("from_node_id", "")])
        if not dict:
            region_moons[region_names[moon.get("from_node_id", "")]] = {}
        region_moons[region_names[moon.get("from_node_id", "")]][moon_name] = moon_id

        moon_data += f"loc.{moon_name}: "
        try:
            rule = create_rule(reqs, token_names, captures, region_names, scenario_list, format_name(moon.get("kingdom", "")).split("_")[0])
        except Exception as e:
            print(e)
            print(f"WARNING: Moon {moon.get('moon_name', '')} has invalid logic. Will assume free")
            rule = "True_()"
        moon_data += rule

        moons.append(moon_data)
    output.append(",\n".join(moons))
    output.append("\n}")

    args.output.mkdir(parents=True, exist_ok=True)

    (args.output / "RuleData.py").write_text("".join(output), encoding="utf-8", newline="\n")
    try:
        subprocess.run(
            ["ruff", "format", str(args.output / "RuleData.py")],
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)

    token_names_output = "class SMOTokenNames:"
    for name in token_names.values():
        token_names_output += f"\n\t{name} = \"{name.replace('_', ' ').title()}\""

    (args.output / "TokenNames.py").write_text(token_names_output, encoding="utf-8", newline="\n")

    output = ["class SMORegionData:", "region_names: dict[str, str] = {"]

    for name in region_names.values():
        output.append(f"\"{name}\": {name.replace('_', ' ').title()}\",")
    output.append("}\n")

    output.append("region_moons: dict[str, dict[str, int]] = {")
    for (region_name, moon_ids) in region_moons.items():
        output.append(f'region_names["{region_name}"]: {{')
        for (moon, id) in moon_ids.items():
            output.append(f"loc.{moon}: {id},")
        output.append("},")
    output.append("}")

    (args.output / "RegionData.py").write_text(f"from ...LocationData import SMOLocationData as loc\n{'\n\t'.join(output)}", encoding="utf-8", newline="\n")
    try:
        subprocess.run(
            ["ruff", "format", str(args.output / "RegionData.py")],
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)

    output = ["from rule_builder.rules import *\n"]
    output.append("from .TokenNames import SMOTokenNames as tokens\n")
    output.append("from .RegionData import SMORegionData as regions\n")
    output.append("from ....Rules import CanCapture, HasStoryProgress\n")
    output.append("\nregion_connection_data : dict[str, dict[str, Rule]] = {\n")
    region_connection_data: dict[str, dict[str, str]] = {}
    for connection in connection_rows:
        reqs, scenario_list = get_logic_reqs(connection.get("requirement_expr", ""), connection.get("difficulty", ""), connection.get("shine_info_available_scenarios", ""), connection.get("option_scenarios", ""))
        from_node = region_names.get(connection.get("from_node_id", ""), "")
        to_node = region_names.get(connection.get("to_node_id", ""), "")
        if not from_node or not to_node:
            if not from_node:
                print(f"Node with id: {connection.get('from_node_id', '')} does not exist!")
            if not to_node:
                print(f"Node with id: {connection.get('from_node_id', '')} does not exist!")
            print(f"WARNING: Ignoring invalid region connection from {connection.get('from_node_id', '')} to {connection.get('to_node_id', '')}")
            continue
        dict = region_connection_data.get(from_node, "")
        if not dict:
            region_connection_data[from_node] = {}
        try:
            rule = create_rule(reqs, token_names, captures, region_names, scenario_list, format_name(connection.get("kingdom", "")).split("_")[0])
        except Exception as e:
            print(f"WARNING: Ignoring region connection from {from_node} to {to_node} due to invalid logic")
            # print(f"Error: {e}")
            continue
        region_connection_data[from_node][to_node] = rule

    for (from_node, connections) in region_connection_data.items():
        output.append(f'regions.region_names["{from_node}"]: {{')
        for (to_node, rule) in connections.items():
            output.append(f'regions.region_names["{to_node}"]: {rule},')
        output.append("},")
    output.append("}")

    args.output.mkdir(parents=True, exist_ok=True)

    (args.output / "ConnectionData.py").write_text("".join(output), encoding="utf-8", newline="\n")
    try:
        subprocess.run(
            ["ruff", "format", str(args.output / "ConnectionData.py")],
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
