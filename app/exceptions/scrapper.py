from exceptions.error import Error


class ScrapperExceptionError(Error):
    """Base class for scrapper-related exceptions"""

    def __init__(self, message="Encounterd problem with scrapper.") -> None:
        super().__init__(message)


class SearchInitError(ScrapperExceptionError):
    def __init__(self, message='Cannot initialize search process.') -> None:
        super().__init__(message)


class NoResultError(ScrapperExceptionError):
    def __init__(self, message="No results found") -> None:
        super().__init__(message)


class ElementIsNotPaaQuestionError(ScrapperExceptionError):
    def __init__(self, message="An element is not a proper PAA question") -> None:
        super().__init__(message)
