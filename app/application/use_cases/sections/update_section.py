from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.section import Section

from app.application.exceptions import SectionNotFoundError
from app.application.interfaces.repositories.section_repository import SectionRepository
from app.application.interfaces.unit_of_work import UnitOfWork


@dataclass(slots=True)
class UpdateSectionCommand:
    section_id: UUID
    title: str
    description: str
    position: int


class UpdateSectionUseCase:
    def __init__(
        self,
        section_repository: SectionRepository,
        uow: UnitOfWork,
    ) -> None:
        self.uow = uow
        self.section_repository = section_repository

    async def execute(self, command: UpdateSectionCommand) -> Section:
        async with self.uow:
            section = await self.uow.sections.get_by_id(command.section_id)
            if section is None:
                raise SectionNotFoundError("Section not found.")

            section.update(
                title=command.title,
                description=command.description,
                position=command.position,
            )
            await self.uow.sections.update(section)
            await self.uow.commit()
            return section
