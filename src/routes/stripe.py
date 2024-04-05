from fastapi import Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles.syncio import add_role_to_user
from supertokens_python.recipe.userroles.interfaces import UnknownRoleError
from supertokens_python.recipe.userroles import UserRoleClaim, PermissionClaim
from supertokens_python.recipe.session import SessionContainer
from fastapi import APIRouter

router = APIRouter(prefix="/stripe")


@router.get("/after-checkout/{user_id}/{role}")
def after_checkout(user_id: str, role: str, session: SessionContainer = Depends(verify_session())):
    res = add_role_to_user("public", user_id, role)
    if isinstance(res, UnknownRoleError):
        raise HTTPException(status_code=404, detail=f"Role: {role} not found")

    if res.did_user_already_have_role:
        return {"message": "success"}

    # we add the user's roles to the user's session
    session.sync_fetch_and_set_claim(UserRoleClaim)

    # we add the user's permissions to the user's session
    session.sync_fetch_and_set_claim(PermissionClaim)

    return {"message": "success"}
