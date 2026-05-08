from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..schemas.organization import ApiKeyResponse, OrganizationRead, OrganizationUpdate
from ..services.organization import OrganizationService
from ..utils.auth import generate_api_key, get_current_user, hash_api_key

router = APIRouter()


@router.get("/me", response_model=OrganizationRead)
async def get_current_organization(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get current organization details."""
    org_service = OrganizationService(session)
    org = await org_service.get_org_by_id(current_user.org_id)

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Organization not found", "code": "ORG_NOT_FOUND"},
        )

    return org


@router.patch("/me", response_model=OrganizationRead)
async def update_current_organization(
    org_data: OrganizationUpdate,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Update current organization details."""
    org_service = OrganizationService(session)

    # Check if new slug is already taken
    if org_data.slug:
        existing_org = await org_service.get_org_by_slug(org_data.slug)
        if existing_org and existing_org.id != current_user.org_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Organization slug already exists",
                    "code": "ORG_SLUG_EXISTS",
                },
            )

    org = await org_service.update_org(current_user.org_id, org_data)

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Organization not found", "code": "ORG_NOT_FOUND"},
        )

    return org


@router.post("/me/rotate-key", response_model=ApiKeyResponse)
async def rotate_api_key(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Rotate organization API key."""
    org_service = OrganizationService(session)

    # Generate new API key
    new_api_key = generate_api_key()
    hashed_key = hash_api_key(new_api_key)

    org = await org_service.update_api_key(current_user.org_id, hashed_key)

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Organization not found", "code": "ORG_NOT_FOUND"},
        )

    return ApiKeyResponse(api_key=new_api_key)
