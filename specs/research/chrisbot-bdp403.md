# Chrisbot v0.2 release validation

Pack1.1.0 targets production BDPv0.2 at https://chris-bot.sellsbrothers.com/.
All five bundled skill files match the exact sb8 release source recorded in
[skill-provenance.json](skill-provenance.json). The endpoint is anonymous and
deterministic; the consuming factory supplies Sonnet and Python3.10+.

Qualification: the Node24.22.1 independent checker passes1,721HTTPexchanges
over73,643resources,32applicable execution rows, with82normative/Appendix E
clauses accounted for. Core/stdlib source hashes match latest upstream main
5972a4486888c8a70844321e7deb79ce80a3d144. The checker extension is submitted
for upstream review in [BDP PR406](https://github.com/gastownhall/bdp/pull/406);
this is not upstream certification.

Six client regression tests pass. Live source search and relationship-based
context acquisition pass for both the source skill and bundled client. The
installed Gas City1.4.2 controller/materialized pack previously passed actual
suspend/attach/resume using one native Claude UUID in a supported file-provider
city. The pack supplies session_id_flag through the existing provider interface;
shared Dolt/runtime is unchanged. The release changes the pack version and
protocol-reference status only; conversational instructions, client logic and
resume configuration match the evaluated candidate.

Native Sonnet evaluations include40baseline/40corrected turns and focused
career, webinar and attribution follow-ups. Tests exercise ongoing conversation
without adding turn/topic/word caps; they do not claim unlimited context or
indistinguishability from Chris. No Fable or model judge was used.

Production verification and exact source/pack release commits are retained in
the owning sb8 release evidence and publication receipts.
