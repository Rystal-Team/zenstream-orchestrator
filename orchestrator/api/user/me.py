### ======================================================================
### ZenStream Orchestrator
### Copyright 2019-2024 © Rystal. All Rights Reserved.
### ======================================================================


from flask_restx import Resource, fields, reqparse
from utils.wrappers import authenticate
from . import api_namespace_user
from app.models.user import User


@api_namespace_user.route("user/me")
class UserAuthenticate(Resource):
    get_model = api_namespace_user.model(
        "Get",
        {
            "authorized": fields.Raw(
                description=""
            )
        },
    )
    get_parser = reqparse.RequestParser()
    get_parser.add_argument("Username", type=str, help="Username of the user", location="headers")

    @authenticate
    @api_namespace_user.doc(parser=get_parser)
    @api_namespace_user.marshal_with(get_model, description="Get the user's profile.")
    def get(self):
        """Get the user's profile."""
        args = self.get_parser.parse_args()

        username = args.get("Username")

        user = User(username).info()
        if user:
            return user, 200
        return {}, 500
