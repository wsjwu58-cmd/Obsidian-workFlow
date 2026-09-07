import pathlib
import tempfile
import unittest

try:
    import sync_wordpress as sync
except ModuleNotFoundError:
    sync = None


@unittest.skipIf(sync is None, 'Install scripts/requirements-blog.txt for blog tests')
class BlogSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.folder = self.root / 'wiki/Topic'
        self.folder.mkdir(parents=True)
        self.note = self.folder / 'One.md'
        self.note.write_text('# One\n\n' + 'Detailed content. ' * 20, encoding='utf-8')
        self.config = dict(status='draft', site_url='http://example.com', author_id=1,
                           max_note_bytes=10000, max_image_bytes=10000,
                           notes=[dict(id='note-one',path='wiki/Topic/One.md')])

    def test_readonly_and_id_stable_after_move(self):
        original = self.note.read_bytes()
        first = sync.build(self.root,self.config)
        self.assertEqual(self.note.read_bytes(), original)
        new = self.folder / 'Renamed.md'
        self.note.rename(new)
        self.config['notes'][0]['path']='wiki/Topic/Renamed.md'
        self.assertEqual(sync.build(self.root,self.config)['posts'][0]['key'], first['posts'][0]['key'])

    def test_code_and_links_and_table(self):
        with self.note.open('a',encoding='utf-8') as f:
            f.write('\n\n```python\n[[Not a link]]\n```\n\n[[Missing|Label]]\n\n| A | B |\n|---|---|\n|1|2|\n')
        result=sync.build(self.root,self.config)
        body=result['posts'][0]['html']
        self.assertIn('<code class="language-python">[[Not a link]]',body)
        self.assertIn('data-wiki-unpublished="true">Label',body)
        self.assertIn('<table>',body)

    def test_local_image_hash_and_encoded_path(self):
        (self.folder/'attachments').mkdir()
        image=self.folder/'attachments/test image.png'
        image.write_bytes(b'image fixture')
        with self.note.open('a') as f: f.write('\n\n![alt](/attachments/test%20image.png)')
        result=sync.build(self.root,self.config)
        self.assertEqual(len(result['assets']),1)
        self.assertIn('wiki-asset:',result['posts'][0]['html'])
        image.write_bytes(b'updated image')
        self.assertNotEqual(result['posts'][0]['html'],sync.build(self.root,self.config)['posts'][0]['html'])

    def test_private_scope_and_secret_rejected(self):
        self.config['notes'][0]['path']='private.md'
        with self.assertRaises(ValueError): sync.build(self.root,self.config)
        self.config['notes'][0]['path']='wiki/Topic/One.md'
        with self.note.open('a') as f: f.write('\n'+'ghp_'+'x'*24)
        with self.assertRaises(ValueError): sync.build(self.root,self.config)

    def test_missing_is_reported_not_deleted(self):
        self.note.unlink()
        result=sync.build(self.root,self.config)
        self.assertEqual(result['missing'],['note-one'])
        self.assertEqual(result['posts'],[])

    def test_external_and_escape_images_fail_closed(self):
        for target in ('https://example.com/image.png','../../private.png','C:/private.png'):
            self.note.write_text('# One\n'+'Text '*40+'\n\n![x]('+target+')',encoding='utf-8')
            with self.assertRaises(ValueError): sync.build(self.root,self.config)

    def test_selected_wikilink_is_deferred_until_post_is_public(self):
        with self.note.open('a') as f: f.write('\n\n[[One|Self link]]')
        result=sync.build(self.root,self.config)
        self.assertIn('href="wiki-note:note-one"',result['posts'][0]['html'])


if __name__ == '__main__': unittest.main()
