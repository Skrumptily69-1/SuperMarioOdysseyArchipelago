#!/usr/bin/env python3
"""Generate formatted Switch-runtime logic tables from authored CSVs."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
INVALID_CHARS = '<>:"/\\|?!*\'(),'

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def q(value: str) -> str:
    return '"' + (value or "").replace("\\", "\\\\").replace('"', '\\"') + '"'

def format_name(value: str, region: bool = False) -> str:
    for char in INVALID_CHARS:
        value = value.replace(char, "")
    snake_case = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", value).lower()
    result = snake_case.replace("...", " ").strip().replace(" ", "_").replace("-", "_").replace("&", "and").replace("é", "e").replace("time_", "timer_")
    if region:
        result = re.sub(r"_free$|_obj[0-9]+$", "", result)
    return result

difficulty_dict: dict[str, str] = {
    "casual": "",
    "advanced": "intermediate_tricks",
    "expert": "hard_tricks",
    "glitched": "easy_glitches"
}
def get_logic_reqs(logic: str, difficulty_options: str, raw_scenarios: str, moon_rock: bool = False, moon_rock_flag: str = "") -> list[list[str]]:
    difficulties: list[str] = difficulty_options.split(";")
    scenarioList = [int(id) for id in raw_scenarios]
    # TODO: Implement Scenario logic considerations

    methods: list[str] = logic.replace("(", "").replace(")", "").split(" | ")
    if(len(difficulties) != len(methods)):
        difficulties = [difficulties[0]] * len(methods)
    if moon_rock:
        return [[*method.split(" & "), difficulty_dict[difficulty], moon_rock_flag]
              for method, difficulty in zip(methods, difficulties, strict=True)]
    return [[*method.split(" & "), difficulty_dict[difficulty]]
            for method, difficulty in zip(methods, difficulties, strict=True)]

def get_region_logic_reqs(logic: str, difficulty_options: str, raw_scenarios: str) -> list[list[str]]:
    difficulties: list[str] = difficulty_options.split(";")
    scenarioLists: list[list[int]] = [
        [int(id) for id in scenarioList.split(",")]
        for scenarioList in [scenarioList for scenarioList in raw_scenarios.split(";")]]
    # TODO: Implement Scenario logic considerations

    methods: list[str] = logic.replace("(", "").replace(")", "").split(" | ")
    if(len(difficulties) != len(methods)):
        difficulties = [difficulties[0]] * len(methods)

    return [[*method.split(" & "), difficulty_dict[difficulty]]
            for method, difficulty in zip(methods, difficulties, strict=True)]

def create_rule(reqs: list[list[str]], token_names: dict[str, str], captures: list[str]) -> str:
    methods: list[str] = []
    for token_list in reqs:
        tokens = [token for token in token_list if token]
        if tokens[0] == "impossible":
            return "False_()"
        if tokens[0] == "free":
            return "True_()"

        kingdom_access_rules: list[str] = [
            f"CanReachRegion(regions.{m.group(1).lower()}_kingdom)"
            for token in tokens
            if (m := re.search(r"KingdomAccess_(.+)", token))
        ]
        capture_rules: list[str] = [
            f"CanCapture(tokens.{token_names[token]})"
            for token in tokens
            if (token in captures)
        ]
        if kingdom_access_rules or capture_rules:
            tokens = [
                token for token in tokens
                if (not re.search(r"KingdomAccess_(.+)", token)) and (token not in captures)
                ]

        method = ""
        if tokens:
            method += ("HasAll(" if len(tokens) > 1 else "Has(")+", ".join([
                f"tokens.{token_names[token]}"
                for token in tokens
            ])+")"

        if kingdom_access_rules or capture_rules:
            rules = [*kingdom_access_rules, *capture_rules, method] if method else [*kingdom_access_rules, *capture_rules]
            if len(rules) > 1:
                method = "And("+",".join(rules)+")"
            else:
                method = rules[0]

        methods.append(method)
    if len(reqs) > 1:
        result = "Or(\n"+",\n".join(methods)+"\n)"
    else:
        result = methods[0]
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
        region_names[row["node_id"]] = format_name(row["stage_display_name"] + " " +row["display_name"], True)
    region_moons: dict[str, dict[str, int]] = {}

    output: list[str] = []
    output.append("from rule_builder.rules import *\n")
    output.append("from .TokenNames import SMOTokenNames as tokens\n")
    output.append("from .RegionData import SMORegionData as regions\n")
    output.append("from ....Rules import CanCapture\n")
    output.append("from ...LocationData import SMOLocationData as loc")
    output.append("\nmoon_rule_data : dict[str, Rule] = {\n")
    moons: list[str] = []
    moon_ids: dict[str, int] = {}
    for moon in moon_rows:
        moon_data = ""
        reqs = get_logic_reqs(moon.get("requirement_expr", ""), moon.get("difficulty", ""), moon.get("shine_info_available_scenarios", ""), moon.get("shine_info_is_moon_rock", "false") == "true", moon.get("moon_rock_token", ""))
        moon_name = format_name(moon.get("moon_name", ""))
        moon_id = int(moon.get("uid", 0))
        if(moon_name[0] == "2"):
            moon_name = moon_name.replace("2d", "dot")
        moon_ids[moon_name] = moon_id

        dict = region_moons.get(region_names[moon.get("from_node_id", "")])
        if not dict:
            region_moons[region_names[moon.get("from_node_id", "")]] = {}
        region_moons[region_names[moon.get("from_node_id", "")]][moon_name] = moon_id

        moon_data += "loc."+moon_name+": "
        moon_data += create_rule(reqs, token_names, captures)

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
        token_names_output += "\n\t" + name + ' = "' + name.replace("_", " ").title() + '"'

    (args.output / "TokenNames.py").write_text(token_names_output, encoding="utf-8", newline="\n")

    output = ["class SMORegionData:", "region_names: dict[str, str] = {"]

    for name in region_names.values():
        output.append('"' + name + '": "' + name.replace("_", " ").title() + '",')
    output.append("}\n")

    output.append("region_moons: dict[str, dict[str, int]] = {")
    for (region_name, moon_ids) in region_moons.items():
        output.append('region_names["'+region_name + '"]: {')
        for (moon, id) in moon_ids.items():
            output.append("loc."+moon+": "+str(id)+",")
        output.append("},")
    output.append("}")

    (args.output / "RegionData.py").write_text("from ...LocationData import SMOLocationData as loc\n"+"\n\t".join(output), encoding="utf-8", newline="\n")
    try:
        subprocess.run(
            ["ruff", "format", str(args.output / "RegionData.py")],
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)

    output.append("from rule_builder.rules import *\n")
    output.append("from .TokenNames import SMOTokenNames as tokens\n")
    output.append("from .RegionData import SMORegionData as regions\n")
    output.append("from ....Rules import CanCapture\n")
    output.append("from ...LocationData import SMOLocationData as loc")
    output.append("\nregion_connection_data : dict[str, dict[str, Rule]] = {\n")
    region_connection_data: dict[str, dict[str, str]] = {}
    for connection in connection_rows:
        reqs = get_logic_reqs(connection.get("requirement_expr", ""), connection.get("difficulty", ""), connection.get("option_scenarios", ""))
        from_node = region_names[format_name(connection.get("from_node_id", ""))]
        to_node = region_names[format_name(connection.get("to_node_id", ""))]

        dict = region_connection_data.get(from_node, "")
        if not dict:
            region_connection_data[from_node] = {}
        region_connection_data[from_node][to_node] = create_rule(reqs, token_names, captures)

    for (from_node, connections) in region_connection_data.items():
        output.append('region_names["'+from_node + '"]: {')
        for (to_node, rule) in connections.items():
            output.append('region_names["' + to_node + '"]: ' + rule + ",")
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
