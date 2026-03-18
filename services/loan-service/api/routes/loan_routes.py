from flask import Blueprint, request, jsonify
from api.controllers.loan_application_controller import LoanApplicationController
from api.middleware.auth import require_auth
from api.middleware.validation import validate_request

loan_bp = Blueprint('loan', __name__)
controller = LoanApplicationController()

@loan_bp.route('/loans', methods=['POST'])
@require_auth
@validate_request('loan_application.json')
def create_loan_application():
    data = request.get_json()
    result = controller.create_application(user_id=request.user_id, data=data)
    return jsonify(result), 201

@loan_bp.route('/loans', methods=['GET'])
@require_auth
def get_user_loans():
    result = controller.get_user_applications(request.user_id)
    return jsonify(result), 200

@loan_bp.route('/loans/<loan_id>', methods=['GET'])
@require_auth
def get_loan_detail(loan_id):
    result = controller.get_application_detail(loan_id)
    if not result:
        return jsonify({'error': 'Loan application not found'}), 404
    return jsonify(result), 200
