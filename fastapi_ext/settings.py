from typing import List
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    JsonConfigSettingsSource,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    src: str = ""
    debug: bool = False
    title: str = "FastAPIExtApp"

    apps: List[str] = []

    model_config = SettingsConfigDict(extra="allow",json_file=["config.json", "config.dev.json", "config.default.json"])

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
