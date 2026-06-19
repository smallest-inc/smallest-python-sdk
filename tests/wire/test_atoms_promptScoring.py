from .conftest import get_client, verify_request_count
from smallestai.atoms.prompt_scoring import PostPromptScoringScoreRequestVersionId


def test_atoms_promptScoring_score_a_prompt() -> None:
    """Test scoreAPrompt endpoint with WireMock"""
    test_id = "atoms.prompt_scoring.score_a_prompt.0"
    client = get_client(test_id)
    client.atoms.prompt_scoring.score_a_prompt(
        request=PostPromptScoringScoreRequestVersionId(
            version_id="6a1589b75e048394eb37bc47",
        ),
    )
    verify_request_count(test_id, "POST", "/prompt-scoring/score", None, 1)
