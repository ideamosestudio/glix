import importlib.util
from pathlib import Path
import re
import unittest

spec=importlib.util.spec_from_file_location('config',Path(__file__).with_name('configure-cpanel-web.py'))
config=importlib.util.module_from_spec(spec);spec.loader.exec_module(config)

class HostingConfigTests(unittest.TestCase):
    def test_preserves_provider_and_is_idempotent(self):
        original='php_flag display_errors Off\n# provider helpdesk\n'
        block=config.build(['index.html','styles.css','assets/logo.webp'])
        merged=config.merge(original,block)
        self.assertTrue(merged.startswith(original))
        self.assertEqual(config.merge(merged,block),merged)
        updated=config.merge(merged,config.build(['index.html','new.css']))
        self.assertTrue(updated.startswith(original))
        self.assertNotIn('styles[.]css',updated)

    def test_rejects_ambiguous_markers(self):
        with self.assertRaises(ValueError):config.merge(config.START,'new')
        with self.assertRaises(ValueError):config.merge((config.START+config.END)*2,'new')

    def test_scope_excludes_helpdesk_mail_and_php(self):
        block=config.build(['index.html','styles.css','assets/logo.webp'])
        patterns=re.findall(r'm#(.*?)#',block)
        for pattern in patterns:
            for path in ['/helpdesk/index.html','/webmail','/api/contacto.php','/assets/unrelated.webp']:
                self.assertIsNone(re.search(pattern,path))
        self.assertTrue(any(re.search(p,'/') for p in patterns))
        self.assertTrue(any(re.search(p,'/index.html') for p in patterns))

if __name__=='__main__':unittest.main()
