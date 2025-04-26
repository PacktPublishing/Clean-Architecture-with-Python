# Anti-example: Controller with framework coupling


class WebTaskController:

    def __init__(self, app: FastAPI):

        self.app = app

        # Direct instantiation too!

        self.use_case = CreateTaskUseCase()

    async def handle_create(self, request: Request):

        try:

            data = await request.json()

            # Controller now tightly coupled to FastAPI

            return JSONResponse(status_code=201, content={"task": result})

        except ValidationError as e:

            raise HTTPException(status_code=400, detail=str(e))
