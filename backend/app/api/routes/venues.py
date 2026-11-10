from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import (
    Message,
    Venue,
    VenueCreate,
    VenuePublic,
    VenuesPublic,
    VenueUpdate,
)

router = APIRouter(prefix="/venues", tags=["venues"])


@router.get("/", response_model=VenuesPublic)
def read_venues(
    session: SessionDep, _: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve venues.
    """
    count = session.exec(select(func.count()).select_from(Venue)).one()
    statement = select(Venue).order_by(col(Venue.id)).offset(skip).limit(limit)
    venues = session.exec(statement).all()
    return VenuesPublic(
        data=[VenuePublic.model_validate(v) for v in venues], count=count
    )


@router.get("/{venue_id}", response_model=VenuePublic)
def read_venue(venue_id: int, session: SessionDep, _: CurrentUser) -> Any:
    """
    Get a venue by id.
    """
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=VenuePublic,
)
def create_venue(*, session: SessionDep, venue_in: VenueCreate) -> Any:
    """
    Create a venue.
    """
    venue = Venue.model_validate(venue_in)
    session.add(venue)
    session.commit()
    session.refresh(venue)
    return venue


@router.patch(
    "/{venue_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=VenuePublic,
)
def update_venue(
    *, session: SessionDep, venue_id: int, venue_in: VenueUpdate
) -> Any:
    """
    Update a venue.
    """
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    venue.sqlmodel_update(venue_in.model_dump(exclude_unset=True))
    session.add(venue)
    session.commit()
    session.refresh(venue)
    return venue


@router.delete("/{venue_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_venue(session: SessionDep, venue_id: int) -> Message:
    """
    Delete a venue.
    """
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    session.delete(venue)
    session.commit()
    return Message(message="Venue deleted successfully")
