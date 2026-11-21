# PR403 BDP workflow — private candidate

This revision requires the private PR403 candidate. Set `CHRIS_BOT_BDP_ORIGIN`
explicitly for validation. Production and the public pack retain their released protocol pending runtime
qualification and explicit promotion approval. No credentials or inference live
in this endpoint; the caller's agent supplies reasoning and voice.

Use the bundled Python client, keeping retrieval backstage:

```sh
python3 <skill-dir>/scripts/bdp.py search go_router --sources
python3 <skill-dir>/scripts/bdp.py search 'developer relations' devrel evangel
python3 <skill-dir>/scripts/bdp.py context 'SOURCE_ID_FROM_RESULTS'
```

Terms are alternatives. Case, spaces, underscores and hyphens normalize.
Use `--kind`, `--voice`, `--since`, `--until` and `--recent` when they help.
Search as much as needed; reuse acquired context; no fixed search budget applies.
The client follows all continuation pages before ranking. `--limit` controls
local display, not completeness. A miss does not prove Chris never wrote about it.

## Read the evidence

The representation has structured `id` (`scope`, `id`, `rev`), a type path,
optional pinned `authority`, and domain `body`. Read `body.text`, `body.others`,
`body.genre` and `body.attribution`. The original source ID remains `body.source_id`.
Attribution spans use UTF-16 offsets into the original text. First-person facts
require eligible supporting spans; inferred labels, fiction and others' words
cannot become Chris's memories. `--unverified` examines an artifact without
upgrading attribution; `--fiction` includes fiction for literary discussion.

`context` reads the source, queries its actual containment relationship resources,
then reads their target passages and sorts by ordinal. It verifies complete target
acquisition. Relationships are resources with `body.source` and `body.target`
references. Links describe containment and passage order, not inferred topics.
Find related works by search and read each one's context.

## Native wire

GET `/sys/capabilities` for discovery; GET `/` for List; GET `/{id}` for a resource.
List returns `items`, opaque `cursor`, and `head:true` at exhaustion. A cursor binds
the publication and selection. Use returned IDs rather than guessing URL encodings.

POST `/stdlib/query:call` with JSON named arguments and a unique idempotencyKey:

```json
{"arguments":[{"name":"where","value":{"kind":"cond","condition":{"kind":"matches","field":["body","search","compact"],"using":"substring","pattern":"gorouter"}}},{"name":"request","value":{"limit":100}}],"idempotencyKey":"unique-request-key"}
```

Only `outcome.kind:success` succeeds; its value is `outcome.value`. Query supports
`all`, `any`, `not`, `cond` and actual-neighbor `via`. Leaf conditions are shared
with List and use root-addressed FieldPath arrays. Substring matching is literal
and case-sensitive; normalize literals like `body.search.compact` when needed.
Ordered comparisons are lexical under this draft. Unoffered features refuse.

The client sends an empty User-Agent for the existing edge policy. Optional
`CHRIS_BOT_HTTP_LOG` retains full receipts, including query text. Errors fail
explicitly. Transient502/503/504 reads retry with bounded delay;429 requires
waiting;410 means restart an expired selection. Never treat failures as no matches.
The optional local `verify` wording check is not factual or voice certification;
`--max-words` applies only to an actual user-requested word bound.

Pinned source: PR403 5ea7cb385deb3027742984c0ef8a7f2442a91260.
The updated BDP repository tool passes this private candidate in its v0.2 read-only
profile. Production runtime qualification and explicit promotion approval remain
required before release. Conversation checks do not replace protocol qualification.
