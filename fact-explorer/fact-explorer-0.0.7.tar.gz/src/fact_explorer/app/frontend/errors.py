from fastapi.responses import HTMLResponse

InlineNotFoundResponse = HTMLResponse(
    status_code=404,
    content="""
            <div class="notification is-link">
                <button class="delete"></button>
                Sorry I could not find anything for that query.
            </div>
            """,
)

JSONParseErrorResponse = HTMLResponse(
    status_code=400,
    content="""
            <div class="notification is-warning">
                <button class="delete"></button>
                You supplied invalid JSON in one of the query fields.
            </div>
            """,
)
