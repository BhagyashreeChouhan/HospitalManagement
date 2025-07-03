from rest_framework.permissions import BasePermission

class DoctorOrAdminPermission(BasePermission):
    """
    Grants access to:
    - Admins (superusers): full access.
    - Doctors: access only to their own patients and records.
    """

    def has_object_permission(self, request, view, obj):
        # Superusers have unrestricted access
        if request.user.is_superuser:
            return True

        # Doctors can access patients they created
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user

        # Doctors can access records if they created the patient
        if hasattr(obj, 'patient') and hasattr(obj.patient, 'created_by'):
            return obj.patient.created_by == request.user

        # Default: deny access
        return False