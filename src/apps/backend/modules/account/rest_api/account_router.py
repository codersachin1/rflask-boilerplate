from flask import Blueprint

from modules.account.rest_api.account_view import AccountView


class AccountRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        account_view = AccountView.as_view("account_view")
        # blueprint.add_url_rule("/accounts", view_func=AccountView.as_view("account_view"))
        blueprint.add_url_rule("/accounts/<id>", view_func=AccountView.as_view("account_update"), methods=["PATCH"])
        blueprint.add_url_rule("/accounts/", defaults={"id": None}, view_func=account_view, methods=["GET"])
        blueprint.add_url_rule("/accounts/<id>/", view_func=account_view, methods=["GET"])
        return blueprint
