Released to main on November 25, 2026 as `6fc4ad7`. The candidate record
below is historical; the production hostname now runs the qualified snapshot.
Fresh production verification is retained with the provider release.

# Chrisbot 1.2.1 candidate

This is local work on `fix/chrisbot-schema-compliance`, based on released
`6fed190b07b76f661374a886e280d99ac8f4d38d`. Public main and the production BDP
endpoint remain unchanged. The default client origin stays the public endpoint;
`CHRIS_BOT_BDP_ORIGIN` selects isolated staging for verification.

All five skill files match the provider branch's provenance manifest. Client
regressions pass (7). Gas City 1.4.2 accepts a fresh import using the real cached
Core pack and lists `chrisbot.chris` with `chrisbot-claude`. The Core dispatcher's
singleton warning describes its normal demand lifecycle; no city supervisor or
production agent was started for this check. Agent/session definitions have not
changed, including conversation resume.

Two fresh native Sonnet sessions exercised 20 turns each, with 40 successful BDP
HTTP reads, clean exact-input audits, topic detours, constraint/role corrections,
disagreement and continuation after thanks. All answers were reviewed. Skill
changes address over-explaining a name correction, confusing career chronology,
invented motives/credits and presenting a broken technical example as fixed.
There are no turn/topic/default length limits. Some responses remain structured;
this is finite conversational evidence, not proof of perfect identity or unlimited
host memory. The provider retains full transcripts, HTTP receipts and hashes in
its schema-compliance verification evidence.

The bundled client also followed a real source's containment Links to all five
ordered passages on actual Cloudflare staging. Current read-only Core 0.2.3
package/type corrections are provider responsibilities; the client needs no
credentials or custom server persona route.

Five additional native Sonnet turns exercised the final corpus snapshot, with
six successful BDP reads and clean input audits. The skill hashes match the
40-turn run. The provider candidate passes the current unmodified upstream
read-only checker, the complete 73,643-resource contract audit, and the combined
readiness gate. This is staging evidence; the released pack and production
endpoint remain unchanged.
