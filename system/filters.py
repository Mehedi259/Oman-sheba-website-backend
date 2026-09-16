from rest_framework import filters

class CountryFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see content for the selected country.
    Reads the 'X-Country' header, defaulting to 'oman'.
    """
    def filter_queryset(self, request, queryset, view):
        # We check if the field 'country' exists on the model
        has_country_field = any(field.name == 'country' for field in queryset.model._meta.get_fields())
        if has_country_field:
            country = request.headers.get('X-Country', 'oman')
            return queryset.filter(country=country)
        return queryset
