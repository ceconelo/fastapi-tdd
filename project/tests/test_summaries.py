import json


def test_create_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://www.google.com"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://www.google.com"


def test_create_summaries_invalid_url(test_app_with_db):
    response = test_app_with_db.post("/summaries/", data=json.dumps({}))

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_read_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/",
        data=json.dumps({"url": "https://www.google.com", "summary": "test"}),
    )
    summary_id = response.json()["id"]
    summary_url = response.json()["url"]

    assert summary_id
    assert summary_url

    response = test_app_with_db.get(f"/summaries/{summary_id}")
    assert response.status_code == 200

    response_dict = response.json()
    print(response_dict)
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == summary_url


def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/summaries/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_all_summaries(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x["id"] == summary_id, response_list))) == 1


def test_remove_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.delete(f"/summaries/{summary_id}/")
    assert response.status_code == 200

    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == 404


def test_remove_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app_with_db):
    response = test_app_with_db.post("/summaries/", data=json.dumps({"url": "https://foo.bar"}))
    summary_id = response.json()["id"]

    response = test_app_with_db.put(f"/summaries/{summary_id}/", data=json.dumps(
        {"url": "https://foo.bar", "summary": "updated!"}))

    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["summary"] == "updated!"
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["created_at"]


def test_update_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.put("/summaries/999/", data=json.dumps(
        {"url": "https://foo.bar", "summary": "updated!"}))
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary_invalid_json(test_app_with_db):
    response = test_app_with_db.post("/summaries/", data=json.dumps({"url": "https://foo.bar"}))
    summary_id = response.json()["id"]

    response = test_app_with_db.put(f"/summaries/{summary_id}/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_update_summary_invalid_keys(test_app_with_db):
    response = test_app_with_db.post("/summaries/", data=json.dumps({"url": "https://foo.bar"}))
    summary_id = response.json()["id"]

    response = test_app_with_db.put(f"/summaries/{summary_id}/", data=json.dumps({
        "url": "https://foo.bar",
    }))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
