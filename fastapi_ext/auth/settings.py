from fastapi_ext.settings import Settings


class AuthSettings(Settings):
    client_id: str = "webapi"
    client_secret: str = "AngtmsOWvi7fnp3xUruLMbdWlkk7s4iL"
    openid_configuration_endpoint: str = (
        "https://auth.cekocloud.com/realms/industry-dev/.well-known/openid-configuration"
    )
    redirect_path: str = "app"


auth_settings = AuthSettings()
