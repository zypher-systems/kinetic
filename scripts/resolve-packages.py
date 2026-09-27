#!/usr/bin/env python3
"""Resolve the full package set of a kiwi image profile with dnf.

Mirrors what kiwi's build installs: the profile's bootstrap, image, and iso
packages and package groups, including every profile it requires, minus the
ignored packages, from the description's repositories. Runs dnf with
--assumeno, so nothing is installed.

    resolve-packages.py DESCRIPTION_DIR KIWI_FILE PROFILE OUTPUT_LIST

Exits non-zero if dnf cannot resolve the transaction.
"""

import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ARCH = "x86_64"
RELEASEVER = "44"


def load(desc, path):
    """Parse a kiwi file and, recursively, the this:// files it includes."""
    root = ET.parse(os.path.join(desc, path)).getroot()
    roots = [root]
    for include in root.findall("include"):
        roots += load(desc, include.get("from").removeprefix("this://./").removeprefix("this://"))
    return roots


def arch_ok(element):
    arch = element.get("arch")
    return not arch or ARCH in arch.split(",")


def main():
    desc, kiwi_file, profile, output = sys.argv[1:5]
    roots = load(desc, kiwi_file)

    requires = {}
    for root in roots:
        for p in root.iter("profile"):
            requires[p.get("name")] = [r.get("profile") for r in p.findall("requires")]
    if profile not in requires:
        sys.exit(f"Unknown profile {profile}")
    active, stack = set(), [profile]
    while stack:
        name = stack.pop()
        if name not in active:
            active.add(name)
            stack += requires.get(name, [])

    packages, groups, ignores = set(), set(), set()
    for root in roots:
        for section in root.findall("packages"):
            if section.get("type") not in ("bootstrap", "image", "iso"):
                continue
            profiles = section.get("profiles")
            if profiles and not set(profiles.split(",")) & active:
                continue
            for item in section:
                if not arch_ok(item):
                    continue
                if item.tag == "package":
                    packages.add(item.get("name"))
                elif item.tag == "namedCollection":
                    groups.add(item.get("name"))
                elif item.tag == "ignore":
                    ignores.add(item.get("name"))

    repo_conf = []
    for root in roots:
        for repo in root.findall("repository"):
            source = repo.find("source").get("path")
            if source.startswith("dir://"):
                source = "file://" + source.removeprefix("dir://")
            key = "metalink" if repo.get("sourcetype") == "metalink" else "baseurl"
            repo_conf.append(
                f"[{repo.get('alias')}]\nname={repo.get('alias')}\n{key}={source}\n"
                f"enabled=1\ngpgcheck=0\npriority={repo.get('priority') or 99}\n"
            )

    with tempfile.TemporaryDirectory() as tmp:
        reposdir = os.path.join(tmp, "repos")
        os.mkdir(reposdir)
        with open(os.path.join(reposdir, "kiwi.repo"), "w") as f:
            f.write("\n".join(repo_conf))
        cmd = [
            "dnf5", "--assumeno",
            f"--installroot={tmp}/root", f"--releasever={RELEASEVER}",
            f"--setopt=reposdir={reposdir}", "--setopt=cachedir=/var/cache/kinetic-resolve",
            "--setopt=install_weak_deps=True",
            "--setopt=group_package_types=default,mandatory,conditional",
            "--setopt=keepcache=True",
        ]
        if ignores:
            cmd.append("--exclude=" + ",".join(sorted(ignores)))
        cmd += ["install"] + sorted(packages) + ["@" + g for g in sorted(groups)]
        result = subprocess.run(cmd, capture_output=True, text=True)

    out = result.stdout + result.stderr
    if "Transaction Summary" not in out:
        print(out[out.find("Failed to resolve"):][:12000] if "Failed to resolve" in out else out[-8000:], file=sys.stderr)
        sys.exit("dnf could not resolve the image's packages")

    # Package rows: " name  arch  epoch:version-release  repo  size"
    row = re.compile(r"^ (\S+)\s+(noarch|x86_64|i686)\s+(\S+)\s+(\S+)\s+[\d.]+\s+\S+$")
    installed = sorted({m.group(1, 3, 4) for m in map(row.match, out.splitlines()) if m})
    with open(output, "w") as f:
        for name, evr, repo in installed:
            f.write(f"{name} {evr} {repo}\n")
    size = re.search(r"After this operation, (.+?) extra will be used", out)
    print(f"Resolved {len(installed)} packages ({size.group(1) if size else '?'} installed) -> {output}")


if __name__ == "__main__":
    main()
