#!/usr/bin/env python3
# 用途：验证计划边界、证据/语言缺项、路径保护及字幕时间精度。
# 参数：python3 -m unittest discover -s tests。
# 输出：测试结果。
# 退出码：0=成功，1=出错
# Known Issues: 无。
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_plan import validate
from export_captions import timestamp


class WorkflowTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name) / 'project'
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/init_project.py'), '--output', str(self.base),
                                 '--engine', 'remotion', '--product', '产品样本', '--source', '文件',
                                 '--languages', 'zh-CN', 'en-US'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.plan = json.loads((self.base / 'plan.json').read_text())

    def tearDown(self):
        self.temp.cleanup()

    def test_sample_and_production_gate(self):
        self.assertEqual(validate(self.plan, self.base), [])
        self.assertTrue(validate(self.plan, self.base, True))
        plan = copy.deepcopy(self.plan)
        plan['demo'] = False
        plan['evidence'] = [{'id': 'claim', 'claim': '官方明确描述的流程', 'source': 'https://example.com', 'status': 'official-claim'}]
        plan['shots'][0]['claimIds'] = ['claim']
        self.assertEqual(validate(plan, self.base, True), [])

    def test_gap_overlap_and_language(self):
        for offset in (-1, 1):
            plan = copy.deepcopy(self.plan)
            plan['shots'][1]['startFrame'] += offset
            self.assertTrue(validate(plan, self.base))
        del self.plan['shots'][0]['title']['en-US']
        self.assertTrue(validate(self.plan, self.base))

    def test_asset_escape_and_missing_claim(self):
        self.plan['assets'] = [{'id': 'unsafe', 'file': '../outside.png', 'kind': 'image'}]
        self.plan['shots'][0]['claimIds'] = ['unknown']
        self.assertGreaterEqual(len(validate(self.plan, self.base)), 2)

    def test_caption_overlap_and_precision(self):
        self.assertEqual(timestamp(1, 30, ','), '00:00:00,033')
        self.assertEqual(timestamp(3600 * 30 + 1, 30, '.'), '01:00:00.033')
        self.plan['captions']['zh-CN'] = [{'startFrame': 0, 'endFrame': 40, 'text': '测试'}, {'startFrame': 39, 'endFrame': 50, 'text': '重叠'}]
        self.assertTrue(validate(self.plan, self.base))

    def test_initializer_preserves_existing_work(self):
        (self.base / 'user.txt').write_text('原内容')
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/init_project.py'), '--output', str(self.base),
                                 '--engine', 'hyperframes', '--product', '测试', '--source', '文件'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual((self.base / 'user.txt').read_text(), '原内容')


if __name__ == '__main__':
    unittest.main()
