import nox

nox.options.default_venv_backend = "uv"
nox.options.sessions = ["lint", "type_check"]


@nox.session(venv_backend="none")
def tidy(session: nox.Session) -> None:
    """Auto-fix fixable linting issues and format code."""
    session.run("ruff", "check", "--fix")
    session.run("ruff", "format")


@nox.session(venv_backend="none")
def lint(session: nox.Session) -> None:
    """Check code for linting and formatting issues."""
    session.run("ruff", "check", "--no-fix")
    session.run("ruff", "format", "--check")


@nox.session(venv_backend="none")
def type_check(session: nox.Session) -> None:
    """Check code for type errors."""
    session.run("pyright")
