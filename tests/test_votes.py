import pytest
from app import models

@pytest.fixture
def test_vote(test_post,session):
    db = next(session)
    new_vote = models.Vote(post_id = test_post[3].id, dir =1)
    db.add(new_vote)
    db.commit()



def test_vote_on_post(authorized_client,test_post):
    res = authorized_client.post("/vote/",json={"post_id":test_post[3].id ,"dir":1})
    res.status_code == 201

def test_vote_twice_on_post(authorized_client,test_post,test_vote):
     res = authorized_client.post("/vote/",json={"post_id":test_post[3].id ,"dir":1})
     assert res.status_code == 409