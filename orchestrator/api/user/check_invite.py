from . import api_namespace_user
from flask_restx import Resource, reqparse
from app.models import Invite


@api_namespace_user.route("user/check_invite")
class UserCheckInvite(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument("url", type=str, help="The url.", location="headers")

    @api_namespace_user.doc(parser=get_parser)
    @api_namespace_user.response(202, "Invite is valid.")
    @api_namespace_user.response(403, "Invite is not valid.")
    @api_namespace_user.response(500, "An error occured.")
    def get(self):
        """Check if an invite is valid."""
        args = self.get_parser.parse_args()
        inviteid = args.get("url").strip()
        
        if Invite().validate(inviteid):
            return {}, 202
        return {}, 403
