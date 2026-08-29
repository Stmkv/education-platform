from dataclasses import dataclass

from app.domain.entities import Course

from app.application.interfaces.repositories.course_repository import CourseRepository


@dataclass(slots=True)
class GetCoursesQuery:
    pass


class GetCoursesUseCase:
    def __init__(self, course_repository: CourseRepository) -> None:
        self.course_repository = course_repository

    async def execute(self, query: GetCoursesQuery) -> list[Course]:
        return await self.course_repository.list()
