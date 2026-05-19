import importlib.util
import json
import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPipelineRegression:
    def test_pipeline_directories_are_writable(self):
        for rel_path in [
            "pipeline/logs",
            "pipeline/queue",
            "pipeline/workspace",
            "pipeline/workspace/output",
        ]:
            directory = PROJECT_ROOT / rel_path
            directory.mkdir(parents=True, exist_ok=True)
            probe = directory / ".regression_probe"
            probe.write_text("ok\n", encoding="utf-8")
            assert probe.read_text(encoding="utf-8") == "ok\n"
            probe.unlink(missing_ok=True)

    def test_pipeline_state_store_round_trip(self, tmp_path):
        from ops.state_manager import PipelineStateStore

        store = PipelineStateStore(tmp_path / "state.json")
        payload = {"job_id": "regression", "phase": "processing"}
        store.save(payload)
        assert store.load() == payload

    def test_pipeline_idempotency_key_is_stable(self):
        from ops.state_manager import compute_idempotency_key

        first = compute_idempotency_key("chat-1", "video.mp4", "face.jpg", "direct")
        second = compute_idempotency_key("chat-1", "video.mp4", "face.jpg", "direct")
        different = compute_idempotency_key("chat-1", "video.mp4", "face.jpg", "multi")
        assert first == second
        assert first != different

    def test_pipeline_media_validation_rejects_missing_file(self, tmp_path):
        from ops.state_manager import validate_output_media

        ok, detail = validate_output_media(tmp_path / "missing.mp4")
        assert ok is False
        assert "missing" in detail.lower()


class TestBotRegression:
    def test_bot_imports_fast(self):
        start = time.time()
        bot = load_module("bot_regression", PROJECT_ROOT / "bot.py")
        assert bot.ROOT_DIR == PROJECT_ROOT
        assert time.time() - start < 10

    def test_bot_credentials_are_masked(self):
        from config.credentials import mask_secret, validate_credentials

        assert mask_secret("1234567890") == "******7890"
        ok, missing = validate_credentials({"bot_token": "token"})
        assert ok is True
        assert missing == []

    def test_bot_missing_credentials_reported(self):
        from config.credentials import validate_credentials

        ok, missing = validate_credentials({})
        assert ok is False
        assert missing == ["bot_token"]


class TestHealthRegression:
    def test_health_check_main_passes_and_emits_json(self, capsys):
        health_check = load_module("health_check_regression", PROJECT_ROOT / "health_check.py")
        assert health_check.main([]) == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["overall"] == "PASS"
        assert payload["results"]["bot_import"]["status"] == "PASS"

    def test_verify_health_integration(self):
        verify = load_module("verify_regression", PROJECT_ROOT / "verify.py")
        ok, detail = verify.check_health(PROJECT_ROOT)
        assert ok is True, detail
        payload = json.loads(detail)
        assert payload["overall"] == "PASS"

    def test_lightning_import_available(self):
        import lightning

        assert lightning.__version__
