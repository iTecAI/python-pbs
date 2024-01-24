class PBSException(Exception):
    def __init__(self, code: int, *args: object, context: str = None) -> None:
        self.code = code
        self.context = context
        super().__init__(*args)

    def __str__(self) -> str:
        return (
            f"PBS Command failed with code {self.code} with context [{self.context}]: "
            + super().__str__()
        )
