from flask_apidoc.commands import GenerateApiDoc


def register(app):
    @app.cli.group()
    def docs():
        """API documentation commands."""
        pass

    @docs.command()
    def api():
        """Compile apidoc"""
        GenerateApiDoc("./app", "app/static/docs").run()
