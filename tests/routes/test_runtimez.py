from src.config import settings


def test_runtimez_reports_rsi_runtime_shape(client):
    response = client.get("/runtimez")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["namespace"] == settings.NAMESPACE
    assert body["db_schema"] == settings.DB.SCHEMA
    assert body["cache_enabled"] == settings.CACHE.ENABLED
    assert body["cache_url_configured"] is bool(settings.CACHE.URL)
    assert body["deriver"] == {
        "provider": settings.DERIVER.MODEL_CONFIG.transport,
        "model": settings.DERIVER.MODEL_CONFIG.model,
        "reasoning_effort": settings.DERIVER.MODEL_CONFIG.reasoning_effort,
    }
    assert body["summary"] == {
        "provider": settings.SUMMARY.MODEL_CONFIG.transport,
        "model": settings.SUMMARY.MODEL_CONFIG.model,
        "reasoning_effort": settings.SUMMARY.MODEL_CONFIG.reasoning_effort,
    }
    assert set(body["dialectic_levels"]) == set(settings.DIALECTIC.LEVELS)
    for level, level_settings in settings.DIALECTIC.LEVELS.items():
        assert body["dialectic_levels"][level] == {
            "provider": level_settings.MODEL_CONFIG.transport,
            "model": level_settings.MODEL_CONFIG.model,
            "reasoning_effort": level_settings.MODEL_CONFIG.reasoning_effort,
            "thinking_budget_tokens": level_settings.MODEL_CONFIG.thinking_budget_tokens
            or 0,
        }
