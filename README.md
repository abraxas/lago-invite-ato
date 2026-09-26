<p align="center">
  <img src="header.png" alt="Abraxas Labs — lago-invite-ato" width="100%">
</p>

<p align="center">
  <a href="https://abraxaslabs.tech"><strong>abraxaslabs.tech</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas">github.com/abraxas</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/abraxas/lago-invite-ato">lago-invite-ato</a>
</p>

# lago-invite-ato

**Lago** `v1.53.0` — GetLago

Unpublished Lago source finding: acceptInvite issues a user-scoped JWT for an existing account when an org admin invites that email. Password and mailbox are not checked on the email/password accept path. Distinct from IdP accept, which binds the identity-provider email.

| | |
|---|---|
| ID | Unpublished Lago source finding #1 (no CVE yet) |
| CWE | [CWE-287, CWE-306](https://cwe.mitre.org/data/definitions/306.html) |
| CVSS | **Critical: 9.6** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Product | [Lago](https://github.com/getlago/lago) |
| Affected | all versions **through v1.53.0** (inclusive) |
| Patched | vendor patch — see references |
| Auth | authenticated (see source map) |
| License | [GNU Affero GPL v3.0](LICENSE) |
| Lab | `127.0.0.1` only · vendor/client disclosure pack, not a scanner |

---

## Advisory (from the source map)

mutations/invites/accept.rb 4-18 no AuthenticableApiUser. invites/accept_service.rb 8-16. users_service.rb 89-117 find_or_initialize_by email, skip password if memberships exist. types/invites/object.rb 16 token field. Google/Okta accept binds IdP email (control).

---

## Entry

- **Method:** `POST`
- **Path:** `/graphql`
- **Router:** AcceptInvite has no AuthenticableApiUser. Invites::AcceptService loads invite by token. UsersService#register_from_invite find_or_initialize_by email; if user exists with memberships, password is not checked. Utils::AuthToken.encode(user:) is user-scoped. Client then sends x-lago-organization for the victim org.
- **Notes:** Logged-in org admin unpublished Lago #1 CWE-287 v1.53.0. Cloud signup is enough for createInvite. Witness: LAGO-INVITE-ATO JWT user is existing victim; currentUser lists Victim Corp. Dummy accept password does not overwrite victim login. Not eval. Not a reverse shell. Disclose security@getlago.com, not a public GitHub issue.

### Call chain

- `POST /graphql registerUser attacker + victim orgs`
- `POST /graphql createInvite(email: victim) as attacker admin (token in response)`
- `POST /graphql acceptInvite(email, dummy password, invite token) with no Authorization`
- `JWT from acceptInvite is victim user id`
- `POST /graphql currentUser + x-lago-organization: victim org`

### Lab preconditions

- Lago v1.53.0 (getlago/lago:v1.53.0)
- LAGO_DISABLE_SIGNUP false (default)
- Attacker has an org they control (Cloud signup or self-host admin)
- Victim email already belongs to another org on the same database

### Witness

acceptInvite JWT user id equals existing victim; currentUser organizations includes Victim Corp; dummy password does not log in; victim real password still works

### Not success

- eval/base64/system payload
- reverse shell
- acceptInvite requires current password or mailbox
- JWT is attacker-org-only
- dummy password overwrites victim login

---

## Patch / remediation

**Do this first:** Apply the vendor patch for **Lago**. See references.

**Verify after upgrade**

- Re-run `lago-invite-ato-Abraxas-Labs.py` against the patched build: the mapped witness must **not** appear.
- Confirm the vendor advisory / changeset in the deployed tree (see references).
- A WAF signature is delay, not a patch.

**If you cannot update immediately**

- Disable or isolate the affected component.
- Hunt for the witness condition on production (new privileged users, unexpected files, injected rows — whatever this CVE's map names).

---

## Reproduction (authorized lab)

Target **only** `http://127.0.0.1:13000` (or the loopback you bound). Do not point this script at the internet.

```bash
python3 lago-invite-ato-Abraxas-Labs.py
```

Success is the **witness** above in the response body. Generic 200 HTML is not it.

---

## Lab images

Loopback stack used to reproduce. Official images unless a `Dockerfile` in this folder builds from source.

- [`lab/docker-compose.yml`](lab/docker-compose.yml)
- [`lab/Dockerfile`](lab/Dockerfile)
- [`lab/run.sh`](lab/run.sh)

Official image `getlago/lago:v1.53.0` on loopback `:13000`. Then:

```bash
cd lab
./run.sh
```

Publish nothing except `127.0.0.1`.

---

## References

- [github.com/getlago/lago](https://github.com/getlago/lago) tag v1.53.0
- [github.com/getlago/lago-api](https://github.com/getlago/lago-api)
- Vendor intake: [security@getlago.com](mailto:security@getlago.com) ([policy](https://www.getlago.com/company/security)). Do **not** open a public GitHub issue.

- Abraxas Labs: [abraxaslabs.tech](https://abraxaslabs.tech) · [github.com/abraxas](https://github.com/abraxas) · [@abraxas_null](https://x.com/abraxas_null)

---

## Records (structured)

```
# Lago unpublished #1 — acceptInvite ATO

CWE: CWE-287, CWE-306
Severity: Critical (HTTP lab SUCCESS, 90%)

## Description

`acceptInvite` has no login. `register_from_invite` loads the user by invite email. If that user already has memberships, the posted password is ignored and a user-scoped JWT is issued. The inviter already has the invite token from `createInvite`.

## Product

Lago v1.53.0. Lab oracle: `LAGO-INVITE-ATO` — JWT is the existing victim, `currentUser` lists Victim Corp, dummy accept password does not log in.
```

---

## License

This disclosure pack is licensed under the **GNU Affero General Public License v3.0**. See [LICENSE](LICENSE).

---

## Disclaimer

This pack is for **the vendor, the site owner, and licensed labs**. The script talks to `127.0.0.1`. Using it against systems you do not own is not authorized by Abraxas Labs. No warranty.

<p align="center">
  <a href="https://abraxaslabs.tech">abraxaslabs.tech</a> ·
  <a href="https://github.com/abraxas">github.com/abraxas</a> ·
  <a href="https://x.com/abraxas_null">@abraxas_null</a>
</p>
