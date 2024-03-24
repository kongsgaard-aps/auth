import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe import emailpassword, session, dashboard, userroles, usermetadata
from supertokens_python.recipe.userroles.asyncio import create_new_role_or_add_permissions, get_all_roles

from settings import settings

if "test" not in settings.SERVER_NAME.lower():
    logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI(
    debug=True,
    title=settings.SERVER_NAME,
    openapi_url=f"{settings.API_STR}/openapi.json",
)
app.add_middleware(get_middleware())

init(
    app_info=InputAppInfo(
        app_name=settings.SERVER_NAME,
        api_domain=str(settings.SERVER_HOST),
        website_domain=settings.DOMAIN,
        api_base_path=f"{settings.API_STR}/auth",
        website_base_path="/auth"
    ),
    supertokens_config=SupertokensConfig(
        connection_uri=str(settings.CONNECTION_URI),
        api_key=settings.API_KEY
    ),
    framework='fastapi',
    recipe_list=[
        session.init(),
        emailpassword.init(),
        dashboard.init(),
        userroles.init(),
        usermetadata.init()
    ],
    mode='asgi'
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await create_new_role_or_add_permissions("okobau", ["read"])
    logger.info(f"Available Roles: {', '.join((await get_all_roles()).roles)}")
