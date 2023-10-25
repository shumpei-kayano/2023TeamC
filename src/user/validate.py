from django.core.exceptions import ValidationError

def validate_admin(value):
  if 'admin' in value:
    raise ValidationError('adminを含んだメールアドレスはご利用頂けません')