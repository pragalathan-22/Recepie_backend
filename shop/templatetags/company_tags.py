from django import template
from shop.models import CompanyInfo

register = template.Library()

@register.simple_tag
def get_company_info():
    return CompanyInfo.objects.first()
