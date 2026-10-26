"""Independent boundary regressions added by the audit; no model API calls."""
from pathlib import Path
import contextlib, http.client, io, json, os, subprocess, sys, tempfile, unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/glasspring/scripts'
sys.path.insert(0, str(SCRIPTS))
import verify_output as vo
import mcp_server as mcp
import probe_render as probe
import samples_gate as gate


class ReleaseIntegrity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_design_differentiator_requirement_is_task_scoped(self):
        skill = (SCRIPTS.parent / 'SKILL.md').read_text(encoding='utf-8')
        self.assertNotIn('Every deliverable must have', skill)
        self.assertIn('For a new preview or full restyle, require', skill)
        self.assertIn('Do not impose this requirement on small edits or review-only work', skill)
        self.assertIn('a new visual differentiator', skill)

    def test_fake_pngs_are_rejected(self):
        good, _ = vo._build_fixture(str(self.root))
        for p in Path(good, 'shots').glob('*.png'):
            p.write_bytes(b'\x89PNG fake')
        self.assertEqual(dict((n, s) for n, s, _ in vo.check_run(good))['shots-coverage'], 'FAIL')

    def test_two_desktop_captures_do_not_cover_mobile(self):
        good, _ = vo._build_fixture(str(self.root))
        p = Path(good, 'shots')
        (p/'shot-0.png').write_bytes((p/'shot-1.png').read_bytes())
        self.assertEqual(dict((n, s) for n, s, _ in vo.check_run(good))['shots-coverage'], 'FAIL')

    def test_token_drift_returns_failure_not_exception(self):
        good, _ = vo._build_fixture(str(self.root))
        Path(good, 'preview.html').write_text('<style>:root{--a:1}</style>'+'var(--a)'*10)
        Path(good, 'other.html').write_text('<style>:root{--b:1}</style>'+'var(--b)'*10)
        self.assertEqual(dict((n, s) for n, s, _ in vo.check_run(good))['multi-page-consistency'], 'FAIL')

    def test_unknown_cli_is_not_success(self):
        good, _ = vo._build_fixture(str(self.root))
        Path(good, 'preview.html').write_text('<p style="color:var(--ink)">hello</p>')
        p = subprocess.run([sys.executable, str(SCRIPTS/'verify_output.py'), good], capture_output=True)
        self.assertEqual(p.returncode, 2)

    def test_notes_draft_stdout_is_utf8_with_legacy_pipe_encoding(self):
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'cp936'
        p = subprocess.run(
            [sys.executable, str(SCRIPTS/'notes_draft.py'), str(self.root), '--stdout'],
            capture_output=True, env=env,
        )
        self.assertEqual(p.returncode, 0, p.stderr.decode('utf-8', errors='replace'))
        output = p.stdout.decode('utf-8')
        self.assertIn('文件名›节名', output)
        self.assertIn('生成时扫描快照', output)

    def test_blank_page_mcp_is_failure(self):
        with patch.object(probe, 'probe', return_value=([], [], [], 0, [], [], [], True, {})):
            result, _ = mcp.t_probe_render({'url': 'about:blank'})
        self.assertEqual(result['verdict'], 'FAIL')
        self.assertFalse(result['ok'])

    def test_axe_skip_mcp_preserves_unknown(self):
        with patch.object(probe, 'probe', return_value=([], [], [], 0, None, None, [], False, {})):
            result, _ = mcp.t_probe_render({'url': 'about:blank'})
        self.assertEqual(result['verdict'], 'UNKNOWN')
        self.assertIsNone(result['axe_serious'])
        self.assertFalse(result['ok'])

    def test_missing_click_observation_is_unknown(self):
        self.assertEqual(probe.coverage_verdict([], [], 0, [], None, False)['verdict'], 'UNKNOWN')

    def test_component_page_with_composed_text_is_not_vacuous(self):
        self.assertFalse(probe.is_vacuous_render({
            'textChars': 91, 'headings': 1, 'controls': 0, 'media': 0,
        }))

    def test_empty_render_is_vacuous_and_unmeasured_render_is_unknown(self):
        self.assertTrue(probe.is_vacuous_render({
            'textChars': 0, 'headings': 0, 'controls': 0, 'media': 0,
        }))
        self.assertIsNone(probe.is_vacuous_render(None))
        self.assertEqual(probe.coverage_verdict([], [], 0, [], [], None)['verdict'], 'UNKNOWN')

    def test_expected_negative_control_requires_the_exact_finding(self):
        expected = {'id': 'color-contrast', 'impact': 'serious', 'targets': ['.subscribe-sub', '.subscribe-unit']}
        exact = [{'id': 'color-contrast', 'impact': 'serious', 'targets': ['.subscribe-sub', '.subscribe-unit']}]
        self.assertEqual(probe.expected_a11y_verdict(exact, expected), 'EXPECTED-NEGATIVE')
        self.assertEqual(probe.expected_a11y_verdict([], expected), 'XPASS')
        self.assertEqual(probe.expected_a11y_verdict([
            {'id': 'color-contrast', 'impact': 'serious', 'targets': ['.subscribe-sub', '.other']},
        ], expected), 'MISMATCH')
        self.assertEqual(probe.expected_a11y_verdict(None, expected), 'UNKNOWN')

    def test_expected_negative_does_not_hide_other_probe_failures(self):
        expected = {'id': 'color-contrast', 'impact': 'serious', 'targets': ['.subscribe-sub']}
        result = probe.coverage_verdict(
            [{'sel': 'h1'}], [], 0,
            [{'id': 'color-contrast', 'impact': 'serious', 'targets': ['.subscribe-sub']}], [], False,
            expected_a11y=expected,
        )
        self.assertEqual(result['verdict'], 'FAIL')
        self.assertEqual(result['expected_negative'], 'EXPECTED-NEGATIVE')

    def test_empty_color_batch_is_unknown(self):
        result, _ = mcp.t_check_contrast({'pairs': []})
        self.assertFalse(result['ok'])
        self.assertEqual(result['verdict'], 'UNKNOWN')

    def install(self, *args):
        return subprocess.run(['node', str(SCRIPTS/'install.mjs'), *map(str, args)], capture_output=True, text=True, encoding='utf8')

    def test_host_layouts_and_copy_integrity(self):
        for host, folder in [('codex', '.agents'), ('claude', '.claude')]:
            target = self.root/host
            self.assertEqual(self.install('--target', target, '--host', host).returncode, 0)
            dest = target/folder/'skills/glasspring'
            self.assertEqual((dest/'SKILL.md').read_bytes(), (SCRIPTS.parent/'SKILL.md').read_bytes())
            self.assertFalse(list(dest.rglob('__pycache__')))

    def test_existing_install_is_preserved_without_replace(self):
        self.assertEqual(self.install('--target', self.root).returncode, 0)
        marker = self.root/'.agents/skills/glasspring/local.txt';marker.write_text('keep me')
        self.assertNotEqual(self.install('--target', self.root).returncode, 0)
        self.assertEqual(marker.read_text(), 'keep me')

    def test_replace_retains_backup(self):
        self.assertEqual(self.install('--target', self.root).returncode, 0)
        marker=self.root/'.agents/skills/glasspring/local.txt';marker.write_text('keep me')
        self.assertEqual(self.install('--target', self.root, '--replace').returncode, 0)
        backups=list((self.root/'.agents/skills').glob('glasspring.backup-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0]/'local.txt').read_text(), 'keep me')

    def test_dry_run_does_not_create_target(self):
        target=self.root/'absent'
        self.assertEqual(self.install('--target', target, '--dry-run').returncode, 0)
        self.assertFalse(target.exists())

    def test_missing_target_is_rejected(self):
        self.assertNotEqual(self.install('--target').returncode, 0)

    def test_skip_only_suite_cannot_succeed(self):
        (self.root/'empty-case').mkdir()
        with patch.object(sys, 'argv', ['samples_gate', '--root', str(self.root), '--only', 'empty-case']), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(gate.main(), 2)

    def test_unknown_probe_cannot_become_pass(self):
        with patch.object(probe, 'probe', return_value=([], [], [], 0, None, None, [], False, {})):
            ok, detail=gate.probe('about:blank', attempts=1)
        self.assertFalse(ok)
        self.assertIn('UNKNOWN', detail)

    def test_multi_page_discovery_probes_every_width(self):
        sample=self.root/'multi-page-case';sample.mkdir()
        for name in ['index.html', 'pricing.html', 'journal.html']:(sample/name).write_text('<h1>Demo</h1>')
        with patch.object(sys, 'argv', ['samples_gate', '--root', str(self.root), '--only', 'multi-page-case']), patch.object(gate, 'has_unreachable_remote_deps', return_value=None), patch.object(gate, 'slop_ok', return_value=(True, 'clean')), patch.object(gate, 'probe', return_value=(True, 'observed')) as check, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(gate.main(), 0)
        self.assertEqual(check.call_count, 6)
        self.assertEqual({c.kwargs['width'] for c in check.call_args_list}, {390, 1440})

    def test_sample_failure_is_not_exempted(self):
        sample=self.root/'sample-case';sample.mkdir()
        (sample/'preview.html').write_text('<h1>Demo</h1>')
        capture=io.StringIO()
        with patch.object(sys, 'argv', ['samples_gate', '--root', str(self.root)]), patch.object(gate, 'has_unreachable_remote_deps', return_value=None), patch.object(gate, 'slop_ok', return_value=(True, 'clean')), patch.object(gate, 'probe', return_value=(False, 'probe crash')), contextlib.redirect_stdout(capture):
            self.assertEqual(gate.main(), 1)
        self.assertIn('[FAIL]', capture.getvalue())

    def test_preview_wait_retries_malformed_startup_response(self):
        with patch.object(gate.urllib.request, 'urlopen', side_effect=[
            http.client.BadStatusLine('GET / HTTP/1.1'),
            contextlib.nullcontext(),
        ]) as open_url, patch.object(gate.time, 'sleep'):
            self.assertTrue(gate.wait_for_preview('http://localhost:1234/', attempts=2))
        self.assertEqual(open_url.call_count, 2)

    def test_preview_wait_does_not_accept_persistent_malformed_responses(self):
        with patch.object(gate.urllib.request, 'urlopen', side_effect=http.client.BadStatusLine('GET / HTTP/1.1')) as open_url, patch.object(gate.time, 'sleep'):
            self.assertFalse(gate.wait_for_preview('http://localhost:1234/', attempts=2))
        self.assertEqual(open_url.call_count, 2)

    def test_non_private_sample_directory_is_discovered(self):
        samples=self.root/'samples';samples.mkdir()
        case=samples/'accessibility-case';case.mkdir()
        (case/'preview.html').write_text('<h1>Demo</h1>')
        with patch.object(sys, 'argv', ['samples_gate', '--root', str(samples)]), patch.object(gate, 'has_unreachable_remote_deps', return_value=None), patch.object(gate, 'slop_ok', return_value=(True, 'clean')), patch.object(gate, 'probe', return_value=(True, 'observed')) as check, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(gate.main(), 0)
        self.assertEqual(check.call_count, 2)


if __name__ == '__main__':
    unittest.main()
