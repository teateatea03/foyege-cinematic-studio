"""Adapter regressions for observed placeholder/glossary failures; no model quality claim."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('subtitle_adapter', Path(__file__).parents[1] / 'scripts/translate_srt.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class AdapterTests(unittest.TestCase):
    def test_whole_cue_format_is_never_sent_to_model(self):
        class Translator:
            def translate(self, text, source, target, budget, glossary):
                self_args.append((text, glossary))
                return {'text': 'This is a test.', 'status': 'completed'}
        self_args = []
        result = adapter.translate_cue(Translator(), '%%IT_style_0%%這是測試。%%IT_style_1%%', 'zh', 'en', 256, {'瞳': 'Hitomi'})
        self.assertEqual(self_args, [('這是測試。', {})])
        self.assertEqual(result['text'], '%%IT_style_0%%This is a test.%%IT_style_1%%')

    def test_only_current_cue_terms_are_included(self):
        class Translator:
            def translate(self, text, source, target, budget, glossary):
                self_args.append(glossary)
                return {'text': 'Hitomi looks at the door.', 'status': 'completed'}
        self_args = []
        adapter.translate_cue(Translator(), '瞳看著門口。', 'zh', 'en', 256, {'瞳': 'Hitomi', '主人': 'Master'})
        self.assertEqual(self_args, [{'瞳': 'Hitomi'}])

    def test_mixed_or_malformed_styles_rejected(self):
        for text in ['先<i>看門</i>再回頭', '<i>沒有結尾', '{\\an8}text']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                adapter.validate_formatting([SimpleNamespace(text=text)])
        adapter.validate_formatting([SimpleNamespace(text='<i>完整句子。</i>'), SimpleNamespace(text='普通句子。')])

    def test_existing_output_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'subtitle.srt'
            adapter.write_new(path, b'original')
            with self.assertRaises(FileExistsError):
                adapter.write_new(path, b'replacement')
            self.assertEqual(path.read_bytes(), b'original')
            self.assertEqual(list(Path(directory).iterdir()), [path])


if __name__ == '__main__':
    unittest.main()
