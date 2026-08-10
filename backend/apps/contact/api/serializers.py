from rest_framework import serializers

from ..models import ContactInquiry


class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = [
            "id",
            "company_or_recruiter",
            "phone",
            "email",
            "description",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]
        extra_kwargs = {
            "company_or_recruiter": {"write_only": True},
            "phone": {"write_only": True},
            "email": {"write_only": True},
            "description": {"write_only": True},
        }

    def validate_company_or_recruiter(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Enter a company or recruiter name.")
        return value

    def validate_description(self, value):
        value = value.strip()
        if len(value) < 20:
            raise serializers.ValidationError("Describe the opportunity in at least 20 characters.")
        return value
