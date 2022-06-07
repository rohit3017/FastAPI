from operator import pos
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from app import models, oauth2, schemas
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
async def posts(
    db: Session = Depends(get_db),
    user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = "",
):
    # cursor.execute(""" Select * from posts """)
    # posts = cursor.fetchall()
    # print(search)
    # post = db.query(models.Post)
    # posts = (
    #     post.order_by("id")
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    posts = (
        db.query(models.Post, func.Count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(
    body: schemas.PostCreate,
    db: Session = Depends(get_db),
    user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """ INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) returning * """,
    #     (body.title, body.content, body.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=user.id, **body.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
async def get_one_post(
    id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)
):
    # cursor.execute(""" SELECT * from posts where id = %s """, str(id))
    # post = cursor.fetchone()
    post = (
        db.query(models.Post, func.Count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
    )
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )

    return post.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)
):
    # cursor.execute(""" DELETE from posts where id = %s returning * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized  for this action",
        )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with given id {id} does not exist",
        )
    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(
    id: int,
    body: schemas.PostCreate,
    db: Session = Depends(get_db),
    user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """UPDATE posts SET title = %s , content = %s , published = %s where id = %s returning * """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized  for this action",
        )

    if post == None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with given id {id} does not exist",
        )
    post_query.update(body.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
