# Private PR403 pack revision

Local branch only. No push, public skill update or new endpoint sharing is authorized
until compliance passes. Uses the current production corpus and the candidate's
structured ResourceId/body representation, List paging and stdlib Query calls.
The native Sonnet checks use the actual private VM and retain source context.
The public main branch remains on its previously released protocol.

The exact PR403 provider kit still validates the old v0.1 wire contract and reports
failure against this v0.2 candidate. No upstream assertions are changed. Full Core
qualification remains unestablished, and local tests are not a replacement oracle.
