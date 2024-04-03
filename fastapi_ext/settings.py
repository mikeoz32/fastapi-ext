from typing import Optional
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    JsonConfigSettingsSource,
    SettingsConfigDict,
)

from fastapi_ext.sqla.settings import SqlaSettings


class Settings(BaseSettings):
    src: str = ""
    debug: bool = False
    title: str = "FastAPIExtApp"

    sqla: Optional[SqlaSettings] = None

    model_config = SettingsConfigDict(json_file=["config.json", "config.dev.json", "config.default.json"])

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (env_settings, JsonConfigSettingsSource(settings_cls), init_settings)

settings = Settings()
