# Chrisbot

Bring a representation of Chris Sells into your Gas City software factory as
`chrisbot.chris`. The pack bundles the conversational skill, authentic writing
examples, career source guide and dependency-free Python BDP client. It retrieves
public evidence from https://chris-bot.sellsbrothers.com/ and follows BDP Links
for surrounding source context. Your factory's agent supplies the reasoning.

## Requirements

- Gas City with schema-2 packs, agent-local skills and `gc import` support
  (validated with gc 1.4.2).
- Claude Code installed and authenticated on the session host; the agent selects
  Sonnet through `option_defaults`, using your existing model access.
- Python 3.10+ and outbound HTTPS to the public BDP service.

There are no BDP credentials or third-party Python dependencies. The pack is
public and self-contained; it needs no access to the private source repository.
Chris's original corpus remains at the endpoint rather than being downloaded as
part of the installation. Your model provider's usual charges or limits apply.

## Install and talk

From your existing city:

```sh
gc import add https://github.com/csells/gas-city-packs/tree/main/packs/chrisbot --name chrisbot
gc import check
gc agent list
gc session new chrisbot.chris --alias chris
```

If the city is stopped, start it with `gc start` before opening the session.
To continue later, run `gc session attach chris`. The alias identifies that
conversation. Another `gc session new chrisbot.chris --alias chris-design` starts
a separate one. In Mission Control, select the `chrisbot.chris` template when
creating a session. Importing the pack does not automatically start an agent.

The equivalent addition to your city's root `pack.toml` is:

```toml
[imports.chrisbot]
source = "https://github.com/csells/gas-city-packs/tree/main/packs/chrisbot"
```

Then run `gc import install`. Commit the resulting `packs.lock` with your city
configuration to give other machines the same version. Use `gc import upgrade`
when you deliberately want newer pack commits.

The import binding qualifies the name: choose binding `advisor` and the agent
becomes `advisor.chris`. This is a city-scoped colleague shared across the factory,
not a rig-scoped worker pool or a background job.

## How the conversation works

The Chris agent loads `skills/chris-bot/SKILL.md`. It stays in role across topics,
remembers the conversation within the host's available context, offers opinions
on new problems, and uses Chris's writing and speaking for history and established
views. There is no turn, topic, follow-up or default word limit. Host context
compaction still applies; the skill tells the agent what to preserve.

Source attribution matters: coauthors, fiction and uncertain transcript speakers
do not become Chris's memories. This is an AI representation, not a live
connection to Chris, and cannot grant his real approval or endorsement.

The endpoint is BDP-only. There is no hosted chat model, website UI or separate
search API. The bundled client searches normalized properties, reads source
Beads, and follows containment Links to passages. Related works are found by
search and then read in their own context.

## Configuration and troubleshooting

Sonnet is the default. Standard Gas City patches can customize the agent in
your city's `city.toml`, without editing the downloaded pack:

```toml
[[patches.agent]]
name = "chrisbot.chris"
option_defaults = { model = "sonnet", effort = "high" }
```

The endpoint defaults to production. `CHRIS_BOT_BDP_ORIGIN` can select an explicit
candidate for testing. `CHRIS_BOT_HTTP_LOG` optionally records full HTTP evidence;
queries in that log may contain your question. Normal use needs neither setting.

For a direct retrieval check from this pack directory:

```sh
python3 agents/chris/skills/chris-bot/scripts/bdp.py search go_router --sources --count
python3 agents/chris/skills/chris-bot/scripts/bdp.py context 'blog:2011/12706'
```

After materialization, Claude sees the same client at
`.claude/skills/chris-bot/scripts/bdp.py` in the session working directory.
If Chris cannot find it, check `gc import check` and the configured agent's skill
materialization before adding manual copies. HTTP errors are reported explicitly;
429 means wait before retrying. Retrieval availability does not guarantee that
every biographical question has an answer in the published corpus.

Pack-format research and validation evidence are in
[specs/research/chrisbot-pack.md](../../specs/research/chrisbot-pack.md).
