from . import api_namespace_user
from flask_restx import Resource, reqparse
from app.models import Invite
from utils.wrappers import authenticate


@api_namespace_user.route("user/generate_invite")
class UserGenerateInvite(Resource):
    get_parser = reqparse.RequestParser()

    @authenticate
    @api_namespace_user.doc(parser=get_parser)
    @api_namespace_user.response(201, "Generate an invite.")
    @api_namespace_user.response(500, "Failed to generate an invite.")
    def post(self):
        """Generate an invite."""
        try:
            inviteid = Invite().generate()
            return {"inviteid": inviteid}, 201
        except Exception as e:
            return {"message": str(e)}, 500
