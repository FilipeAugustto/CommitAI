from typing import Literal

from pydantic import BaseModel, Field

TipoCommit = Literal[
    'feat',
    'fix',
    'docs',
    'style',
    'refactor',
    'perf',
    'test',
    'build',
    'ci',
    'chore',
    'revert',
]


class CommitSchema(BaseModel):
    type: TipoCommit
    scope: str | None = None
    description: str = Field(max_length=72)
    body: str | None = None
    breaking: bool = False
    sufficient: bool = True

    def formatar(self) -> str:
        escopo = f'({self.scope})' if self.scope else ''
        marca = '!' if self.breaking else ''
        cabecalho = f'{self.type}{escopo}{marca}: {self.description}'
        return f'{cabecalho}\n\n{self.body}' if self.body else cabecalho
