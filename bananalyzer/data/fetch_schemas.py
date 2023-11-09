"""
Mapping of fetch_id to fetch schema to avoid duplicate schemas in examples.json
"""
fetch_goals = {
    "job_posting": "Return the provided information about the job posting. For salaries, provide the range as ${lower} - ${upper} if available, otherwise just provide ${salary}",
}

fetch_schemas = {
    "contact": {
        "name": "string",
        "website": "string",
        "phone": "string",
        "fax": "string",
        "address": "string",
        "type": "string",  # What kind of location / person is it? May not be available
    },
    "job_posting": {
        "job_id": "string",
        "job_title": "string",
        "job_category": "string",
        "date_posted": "string",
        "location": "string",
        "job_description": "string",
        "roles_and_responsibilities": "string",
        "qualifications": "string",
        "preferred_qualifications": "string",
        "benefits": "string",
        "salary": "string",
    },
    "manufacturing_commerce": {
        "mpn": "string",
        "alias_mpns": ["string"],
        "manufacturer": "string",
        "classifications": ["string"],
        "description": "string",
        "hero_image": "string",
        "series": "string",
        "lifecycle_status": "string",
        "country_of_origin": "string",
        "aecq_status": "string",
        "reach_status": "string",
        "rohs_status": "string",
        "export_control_class_number": "string",
        "packaging": "string",
        "power_rating": "string",
        "voltage_rating": "string",
        "mount_type": "string",
        "moisture_sensitivity_level": "string",
        "tolerance": "string",
        "inductance": "string",
        "capacitance": "string",
        "resistance": "string",
        "min_operating_temperature": "string",
        "max_operating_temperature": "string",
        "leadfree": "string",
        "termination_type": "string",
        "num_terminations": "int",
        "specs": [{"label": "string", "value": "string"}],
        "product_change_notification_documents": [
            {"url": "string", "filename": "string"}
        ],
        "reach_compliance_documents": [{"url": "string", "filename": "string"}],
        "rohs_compliance_documents": [{"url": "string", "filename": "string"}],
        "datasheets": [{"url": "string", "filename": "string"}],
        "specsheets": [{"url": "string", "filename": "string"}],
        "suggested_alternative_mpns": ["string"],
    },
}
