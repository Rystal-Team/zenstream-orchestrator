from . import api_namespace_user
from flask_restx import Resource, reqparse
from app.models.user import User


@api_namespace_user.route("user/authenticate")
class AuthenticateUser(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument(
        "Username", type=str, help="The username.", location="headers"
    )
    get_parser.add_argument("TOKEN", type=str, help="The token.", location="headers")

    @api_namespace_user.doc(parser=get_parser)
    @api_namespace_user.response(202, description="User authenticated.")
    @api_namespace_user.response(403, description="User unauthenticated.")
    @api_namespace_user.response(
        500, description="An error occurred while authenticating."
    )
    def post(self):
        """Authenticate the user."""
        args = self.get_parser.parse_args()
        username = args.get("Username").strip()
        token = args.get("TOKEN").strip()
        args = self.get_parser.parse_args()
        username = args.get("Username").strip()
        token = args.get("TOKEN").strip()

        if User(username).authenticate(token):
            return {}, 202
        return {}, 403
