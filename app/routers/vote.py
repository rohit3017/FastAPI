from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import database, oauth2, schemas, models

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {vote.post_id} does not exist",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )

    vote_found = vote_query.first()

    if vote.dir == 1:
        if vote_found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already vote on post {vote.post_id}",
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added succesfully"}

    else:
        if not vote_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f" user {current_user.id} has not vote on post {vote.post_id}",
            )

        vote_query.delete()
        db.commit()
        return {"message": "vote deleted succesfully"}
