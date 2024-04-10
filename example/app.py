from fastapi_ext.app import create_app

app = create_app()

@app.get("/info")
async def get_service_info():
    return {}
