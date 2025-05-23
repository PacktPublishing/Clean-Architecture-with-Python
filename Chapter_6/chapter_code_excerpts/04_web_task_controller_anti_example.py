# Anti-example: Controller with framework coupling

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


class WebTaskController:

    def __init__(self, app: FastAPI):

        # Controller now tightly coupled to FastAPI
        self.app = app
        # Direct instantiation too!
        self.create_use_case = CreateTaskUseCase()

    async def handle_create(self, request: Request):

        try:
            data = await request.json()
            result = self.create_use_case.execute(data)

            return JSONResponse(status_code=201, content={"task": result})

        except ValidationError as e:

            raise HTTPException(status_code=400, detail=str(e))
