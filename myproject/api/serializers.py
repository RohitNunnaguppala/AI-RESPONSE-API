# api/serializers.py
from rest_framework import serializers
from .models import Response

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'prompt', 'response_text', 'model_used', 
                  'timestamp', 'status', 'processing_time']
        read_only_fields = ['id', 'response_text', 'timestamp', 
                            'status', 'processing_time']

    def validate_prompt(self, value):
        # Ensure prompt is not empty or whitespace
        if not value.strip():
            raise serializers.ValidationError("Prompt cannot be empty.")
        return value

    def validate_model_used(self, value):
        # Validate that the model_used is among allowed choices
        allowed_models = ['gpt-3.5', 'gpt-4', 'claude-3']
        if value not in allowed_models:
            raise serializers.ValidationError(f"Invalid model. Choose from {allowed_models}.")
        return value

    def validate_status(self, value):
        # Ensure status is valid
        allowed_statuses = ['pending', 'processing', 'completed', 'failed']
        if value not in allowed_statuses:
            raise serializers.ValidationError(f"Invalid status. Choose from {allowed_statuses}.")
        return value

    def validate_processing_time(self, value):
        # Ensure processing_time is non-negative
        if value < 0:
            raise serializers.ValidationError("Processing time cannot be negative.")
        return value

    def validate_response_text(self, value):
        # Ensure response_text is present when status is 'completed' or 'failed'
        if self.initial_data.get('status') in ['completed', 'failed'] and not value.strip():
            raise serializers.ValidationError("Response text cannot be empty when status is 'completed' or 'failed'.")
        return value
