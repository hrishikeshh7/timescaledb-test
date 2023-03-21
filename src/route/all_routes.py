from fastapi import APIRouter

from src.route.Test.test import router as test_router


router = APIRouter()

router.include_router(test_router)

