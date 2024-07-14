from app import schemas, models, oauth2
from fastapi import Depends, HTTPException, status, Response, APIRouter
from app.database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter(tags=["Posts"])


@router.get("/posts/", response_model=list[schemas.PostOut])
# @router.get("/posts/")
async def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 5,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cur.execute("SELECT * FROM posts")
    # posts = cur.fetchall()

    results = (
        db.query(models.Posts, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True)
        .group_by(models.Posts.id)
        .filter(models.Posts.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return results


@router.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    # cur.execute(
    #     f""" INSERT INTO posts (title, content, published) VALUES (%s,%s ,%s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )

    # new_post = cur.fetchone()
    # conn.commit()
    print(current_user.email)
    db_post = models.Posts(owner_id=current_user.id, **post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@router.get("/posts/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # post = find_post(id)
    # cur.execute(""" select * from posts where id = %s """, (str(id),))
    # post = cur.fetchone()
    post = (
        db.query(models.Posts, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True)
        .group_by(models.Posts.id)
        .filter(models.Posts.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    # return {"post_detail": f"Here is post {post}"}
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # index = find_index_post(id)
    # cur.execute(""" delete from posts where id = %s returning *""", (str(id),))
    # del_post = cur.fetchone()

    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    del_post = post_query.first()
    if del_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    if del_post.owner_id != current_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requestde action",
        )

    del_post.delete(synchronize_session=False)
    db.commit()


@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    # cur.execute(
    #     """ update posts set title = %s, content = %s where id = %s returning *""",
    #     (post.title, post.content, id),
    # )

    # db_post = cur.fetchone()
    print(post)

    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    db_post = post_query.first()
    print(db_post)
    if db_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    # conn.commit()

    return db_post
