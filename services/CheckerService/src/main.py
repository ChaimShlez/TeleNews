import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from services.CheckerService.src.check_channel import Check_channel


app = FastAPI()
checker = Check_channel()


class ChannelData(BaseModel):
    link: str
    country: str = "unknown"


@app.post("/check")
async def check_channel_endpoint(data: ChannelData):
    approved = await checker.check_channel(data.link)
    return {"link": data.link, "approved": approved}



if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8001)


