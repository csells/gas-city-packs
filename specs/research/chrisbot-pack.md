# Chrisbot pack research and validation

Researched November 1, 2026 against Gas City main snapshot
`d5261665dcd8f12e8a5a7ed4fdf9343f849f8c37`. Examined the authoring guide,
authoritative specification, agent discovery, provider/model configuration,
skill materialization command and session CLI. Installed CLI: gc 1.4.2.

## Decisions traced to upstream

- [Pack specification](https://github.com/gastownhall/gascity/blob/d5261665dcd8f12e8a5a7ed4fdf9343f849f8c37/docs/reference/specs/pack-spec.md):
  schema 2, scoped product name `csells/chrisbot`, conventional agent directory,
  prompt discovery, agent-local skill discovery and source-relative paths.
  Pack metadata does not determine the import binding. Binding `chrisbot`
  produces city agent identity `chrisbot.chris`.
- [Create and Share Packs](https://github.com/gastownhall/gascity/blob/d5261665dcd8f12e8a5a7ed4fdf9343f849f8c37/docs/guides/shareable-packs.md):
  use a durable GitHub tree URL, `gc import add/install/check`, and commit the
  resolved `packs.lock`. Private helper code stays with the owning skill.
- [Configure an Agent](https://github.com/gastownhall/gascity/blob/d5261665dcd8f12e8a5a7ed4fdf9343f849f8c37/docs/guides/configuring-an-agent.md):
  `option_defaults.model = "sonnet"` selects the model. A pack-owned provider
  inheriting `builtin:claude` avoids requiring the consumer's `claude` alias
  or overriding their provider settings.
- [Agent discovery implementation](https://github.com/gastownhall/gascity/blob/d5261665dcd8f12e8a5a7ed4fdf9343f849f8c37/internal/config/agent_discovery.go):
  discovers `agents/chris/skills/` and `prompt.template.md` directly. No custom
  installer, copied cache paths, legacy attachment lists or symlinks are needed.
- [Skill materializer](https://github.com/gastownhall/gascity/blob/d5261665dcd8f12e8a5a7ed4fdf9343f849f8c37/cmd/gc/cmd_internal_materialize_skills.go):
  actual provider materialization places the skill under `.claude/skills/`.
- `gc session new --help` and `gc session attach --help`: manual sessions are
  persistent conversations. No always-on named session or worker pool is needed.
  The user explicitly starts Chris; import alone does not start inference.

The skill and client are extracted from the reviewed production release,
without changing their conversational policy. Provenance hashes are retained in
[skill-provenance.json](skill-provenance.json). Production BDP is the only corpus
dependency. No endpoint implementation, secret or private corpus is published.

## Validation boundary

Validated using real Gas City configuration loading, strict prompt rendering,
provider-specific skill materialization and the real public BDP endpoint. Tests
of the client preserve ranking, normalization, transient-error and attribution
regressions. Native Sonnet exercises the rendered prompt and materialized skill.

An attempt to initialize a default disposable factory encountered the host's
existing shared Beads schema mismatch (v57 versus v66). Beads refused automatic
migration. No schema migration was authorized or attempted as a remedy. Subsequent
pack/config/materialization checks use a disposable file-backed city with real
core imports and production BDP data. No controller-managed session, tmux
attach/resume, or Mission Control browser flow is claimed as tested here.
This package adds configuration and an existing client, and does not deploy or
change the production BDP service or any existing factory's configuration.

Executed checks: six client regressions passed; strict `gc prime` rendered
the Chris prompt; `gc config show --validate` accepted both the minimal import
and the disposable city with real pinned core imports; actual materialization
installed Chris's complete skill alongside seven core skills. The materialized
client's live normalized go_router source Query returned 25 matches.
The core control-dispatcher emits an informational singleton/drain advisory in
this CLI version; Chris defines neither a pool nor an always-on session, so that
upstream core advisory does not require a Chris pack change.

For maintenance, run `python3 -m unittest discover -s tests -v`. To inspect the
installed artifact, run `gc config show --validate`, `gc import check` and
`gc prime chrisbot.chris --strict` from a consuming city.

## Public installation and conversation results

Published pack payload commit: `446e02df654cd3f0c98ec7d909539496fbc168ba`.
Anonymous GitHub raw access succeeds and matches the local manifest. The exact
README `gc import add` command fetched the public pack into a new disposable
city, wrote the pinned SHA into the import and `packs.lock`, and passed
`gc import check` (one remote import). Strict public prompt rendering succeeded.
The resolved agent is city-scoped `chris`, provider `chrisbot-claude`, model
`sonnet`; the import qualifies its runtime name as `chrisbot.chris`.
Actual materialization from the public download produced a skill whose five
files exactly match the provenance hashes. Its context command read the real
Microsoft-to-Telerik announcement through production BDP.

Two native Sonnet turns used the rendered pack prompt and materialized skill.
Both completed without execution errors and the exact-input audit passed. The
first reply retrieved career context and compared developer advocacy with Gas
City; the follow-up applied that perspective to a small team's concern about
losing interesting work. The model retained context. Ten HTTP receipts include
nine successful reads and one correctly refused overbroad Query (413); the
agent narrowed its retrieval. Three actual Link-walk requests were recorded.
Both answers were reviewed against their source context. The voice remains
somewhat essay-like and can explain evidence limits too much; this is not a
claim of indistinguishability from Chris or exhaustive corpus coverage.

The test harness ran the native Claude provider after Gas City prompt rendering
and skill materialization, rather than a controller-managed Gas City session.
The shared Beads mismatch described above remains outside this pack's scope.
GitHub Actions also passed all six client regressions.
