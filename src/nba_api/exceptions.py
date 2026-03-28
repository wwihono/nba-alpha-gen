class OddsApiError(Exception):
    """Raised when The Odds API returns an error or invalid response."""

    def __init__(self, message: str, status_code: int | None = None, body: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body
