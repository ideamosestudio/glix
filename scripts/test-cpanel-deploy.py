import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('mirror', Path(__file__).with_name('deploy-cpanel.py'))
mirror = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mirror)

class MirrorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='glix-mirror-test-')
        self.root = Path(self.tmp.name).resolve()
        assert self.root.parent == Path(tempfile.gettempdir()).resolve()
        self.addCleanup(self.tmp.cleanup)
        self.repo, self.home = self.root/'repo', self.root/'home'
        self.repo.mkdir(); self.home.mkdir()
        self.web = self.home/'public_html'; self.web.mkdir()
        self.put(self.repo, 'index.html', 'new index')

    def put(self, root, name, text):
        path=root/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text)

    def deploy(self, names=None, revision='a'*40, **kwargs):
        return mirror.deploy(self.repo,self.home,revision,names or ['index.html'],**kwargs)

    def test_preserves_hosting_files_and_backs_up_overwritten_site(self):
        self.put(self.web,'index.html','old index')
        self.put(self.web,'contacto.php','backend')
        self.put(self.web,'.htaccess','hosting rules')
        self.put(self.repo,'.env','secret')
        self.put(self.repo,'assets/key.pem','private')
        self.put(self.repo,'README.md','internal docs')
        result=self.deploy(['index.html','.env','README.md','assets/key.pem'])
        self.assertTrue(result['verified'])
        self.assertEqual((self.web/'index.html').read_text(),'new index')
        self.assertEqual((self.web/'contacto.php').read_text(),'backend')
        self.assertEqual((self.web/'.htaccess').read_text(),'hosting rules')
        self.assertFalse((self.web/'.env').exists())
        self.assertFalse((self.web/'README.md').exists())
        self.assertFalse((self.web/'assets/key.pem').exists())
        backups=list((self.home/'.glix-mirror/backups').glob('*/index.html'))
        self.assertEqual(backups[0].read_text(),'old index')

    def test_removes_only_previous_managed_files(self):
        self.put(self.repo,'old.html','old')
        self.deploy(['index.html','old.html'])
        self.put(self.web,'unrelated.html','keep')
        result=self.deploy(revision='b'*40)
        self.assertEqual(result['removed'],1)
        self.assertFalse((self.web/'old.html').exists())
        self.assertTrue((self.web/'unrelated.html').exists())

    def test_dry_run_and_idempotence(self):
        self.assertTrue(self.deploy(dry_run=True)['dry_run'])
        self.assertFalse((self.web/'index.html').exists())
        self.deploy()
        self.assertEqual(self.deploy()['changed'],0)

    def test_rejects_path_traversal_in_state(self):
        state=self.home/'.glix-mirror';state.mkdir()
        (state/'manifest.json').write_text(json.dumps({'files':{'../outside.html':'x'}}))
        with self.assertRaises(ValueError):self.deploy()
        self.assertFalse((self.web/'index.html').exists())

    def test_preserves_modified_obsolete_file(self):
        self.put(self.repo,'old.html','old');self.deploy(['index.html','old.html'])
        self.put(self.web,'old.html','manually changed')
        with self.assertRaises(ValueError):self.deploy()
        self.assertEqual((self.web/'old.html').read_text(),'manually changed')

    def test_rolls_back_partial_copy(self):
        self.put(self.web,'index.html','old index')
        self.put(self.repo,'second.html','new second')
        original=mirror.atomic_copy; calls=0
        def fail_once(source,destination):
            nonlocal calls
            calls+=1
            if calls==2:raise OSError('simulated copy failure')
            return original(source,destination)
        with patch.object(mirror,'atomic_copy',side_effect=fail_once):
            with self.assertRaises(OSError):self.deploy(['index.html','second.html'])
        self.assertEqual((self.web/'index.html').read_text(),'old index')
        self.assertFalse((self.web/'second.html').exists())
        self.assertFalse((self.home/'.glix-mirror/deploy.lock').exists())

    def test_rejects_symlink_destinations(self):
        outside=self.root/'outside';outside.mkdir()
        try:(self.web/'assets').symlink_to(outside,target_is_directory=True)
        except OSError:self.skipTest('symlinks unavailable for this local account')
        self.put(self.repo,'assets/test.css','test')
        with self.assertRaises(ValueError):self.deploy(['index.html','assets/test.css'])
        self.assertFalse((outside/'test.css').exists())

if __name__=='__main__':unittest.main()
