# Gas City packs

Reusable [Gas City](https://github.com/gastownhall/gascity) packs from Chris Sells.

| Pack | What it adds |
| --- | --- |
| [chrisbot](packs/chrisbot/) | A Chris agent for ongoing conversations, with his published work available through public BDP. |

## Install Chris

In an existing Gas City factory, run:

```sh
gc import add https://github.com/csells/gas-city-packs/tree/main/packs/chrisbot --name chrisbot
gc import check
gc agent list
gc session new chrisbot.chris --alias chris
```

Gas City pins the fetched commit in `packs.lock`. Start the city with `gc start`
if it is not already running. Resume the conversation with `gc session attach chris`.
You can create other conversations from the same template with different aliases.

Ask Chris about a design, a difficult engineering tradeoff, his career, or an idea
you're still working through. Change topics and keep talking; there is no fixed
turn count or answer length.

See the [pack README](packs/chrisbot/README.md) for prerequisites, configuration,
validation and the exact TOML import. These are opt-in agent definitions; the
repository does not install a new service or change your factory's default agents.
