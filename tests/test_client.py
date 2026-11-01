import importlib.util,unittest,io,urllib.error
from unittest.mock import patch
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'packs/chrisbot/agents/chris/skills/chris-bot/scripts/bdp.py'
spec=importlib.util.spec_from_file_location('bdp_client',p);client=importlib.util.module_from_spec(spec);spec.loader.exec_module(client)
class ClientTests(unittest.TestCase):
 def test_primary_source_survives_newer_tweet_mentions(self):
  def resource(ident,source,kind,date,title):return {'id':ident,'properties':{'source_id':source,'kind':kind,'voice':'chris','published':date,'source_title':title}}
  rows=[resource('tweet-'+str(i),'tweet-'+str(i),'tweet','2026-10-30','Gas City is cool') for i in range(20)]
  rows += [resource('passage-'+str(i),'release-post','blog','2026-07-03','Gas City 1.3: now we are looping') for i in range(15)]
  rows += [resource('launch','launch-post','blog','2026-04-28','Announcing Gas City 1.0')]
  chosen=client.rank_matches(rows,['gascity'],12)
  self.assertEqual(chosen[0]['properties']['source_id'],'release-post')
  self.assertEqual(sum(r['properties']['source_id']=='release-post' for r in chosen),2)
  self.assertTrue(any(r['id']=='launch' for r in chosen))
 def test_case_and_spoken_spellings_match(self):
  self.assertEqual(client.compact('GoRouter'),client.compact('go_router'))
  self.assertEqual(client.compact('GO ROUTER'),client.compact('go_router'))
 def test_recent_search_prioritizes_later_positions_over_old_topic_titles(self):
  rows=[{'id':'old','properties':{'kind':'blog','voice':'chris','source_id':'old','published':'2006','source_title':'Why I love WPF'}},
        {'id':'new','properties':{'kind':'blog','voice':'chris','source_id':'new','published':'2015','source_title':'What about HTML?'}}]
  self.assertEqual(client.rank_matches(rows,['wpf'],1,recent=True)[0]['id'],'new')
 def test_transient_read_failure_is_retried_without_changing_the_query(self):
  failure=urllib.error.HTTPError('https://example.org/',502,'Bad Gateway',{},io.BytesIO(b'Bad Gateway'))
  response=io.BytesIO(b'{"ok":true}');response.status=200
  with patch.object(client.urllib.request,'urlopen',side_effect=[failure,response]) as opener,patch.object(client.time,'sleep') as sleep:
   self.assertEqual(client.request('/'),{'ok':True})
   self.assertEqual(opener.call_count,2)
   self.assertEqual(opener.call_args_list[0].args[0].full_url,opener.call_args_list[1].args[0].full_url)
   sleep.assert_called_once()
 def test_guard_catches_current_views_inferred_from_old_positions(self):
  self.assertIn('undated-current-position',client.review_draft('My view has changed: I now recommend HTML first.'))
  self.assertEqual(client.review_draft('In 2015, I recommended HTML. I cannot establish my current view from published work.'),[])
 def test_guard_distinguishes_missing_evidence_from_absolute_absence(self):
  self.assertIn('unsupported-absence-claim',client.review_draft("I never gave a reason for leaving."))
  self.assertIn('unsupported-absence-claim',client.review_draft('I never wrote a post about that.'))
  self.assertEqual(client.review_draft("I cannot establish the reason from the sources I found."),[])
if __name__=='__main__':unittest.main()
