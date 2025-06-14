import responses

import agentic_index_cli.internal.scrape as scrape


@responses.activate
def test_scrape_mock():
    import warnings

    warnings.filterwarnings("ignore", category=DeprecationWarning, module="responses")
    item = {
        "name": "repo",
        "full_name": "owner/repo",
        "html_url": "https://example.com/repo",
        "description": "test repo",
        "stargazers_count": 1,
        "forks_count": 0,
        "open_issues_count": 0,
        "archived": False,
        "license": {"spdx_id": "MIT"},
        "language": "Python",
        "pushed_at": "2025-01-01T00:00:00Z",
        "owner": {"login": "owner"},
    }
    for _ in scrape.QUERIES:
        responses.add(
            responses.GET,
            "https://api.github.com/search/repositories",
            json={"items": [item]},
            headers={"X-RateLimit-Remaining": "99"},
            match_querystring=False,
            status=200,
        )
    repos = scrape.scrape(min_stars=0, token=None)
    assert repos and repos[0]["full_name"] == "owner/repo"
