from django.db import models
import json

class CustomJSONField(models.JSONField):
    """
    CustomJSONField is a specialized JSONField that ensures compatibility across
    various SQL databases by using jsonb data type and incorporating flexible
    decoding methods. 
    """
    def db_type(self, connection):
        # Ensures the use of jsonb data type in the database
        return 'jsonb'

    def from_db_value(self, value, expression, connection):
        # Handling the conversion of database values to Python objects
        if value is None:
            return None

        if isinstance(value, dict):
            return value

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            # Provide a default serialization for unprocessable values
            return json.dumps(value)
