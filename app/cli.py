import os


def register(app):
    @app.cli.group()
    def database():
        """Database management commands"""
        pass

    @datebase.command()  # pyright: ignore # noqa
    def seed():
        """Seed database with admin user and spots"""
