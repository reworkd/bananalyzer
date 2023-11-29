from typing import Dict, Optional, Type

from pydantic import BaseModel, Field

"""
This file contains mapping of fetch_id to fetch schema to avoid duplicate schemas in examples.json
"""


class ContactSchema(BaseModel):
    name: str = Field(
        description="name of the location (not the hospital system name) *precisely* as it is written on the page (do not edit it, add text, or combine names)"
    )
    address: str = Field(
        description="complete address of the location including street, city, state, and ZIP",
    )
    phone: str = Field(
        description="phone number of the location (only include the number but retain its formatting)",
    )
    fax: Optional[str] = Field(
        description="fax number of the location (only include the number but retain its formatting)",
        default=None,
    )
    type: Optional[str] = Field(
        description="the type of location: Neurosurgery, MRI Services, etc. (not all locations will have a type available on the page)",
        default=None,
    )


class JobPostingSchema(BaseModel):
    job_id: str
    job_title: str
    job_category: str
    date_posted: str
    location: str
    job_description: str
    roles_and_responsibilities: str
    qualifications: str
    preferred_qualifications: str
    benefits: str
    salary: str


class Specification(BaseModel):
    label: str
    value: str


class Document(BaseModel):
    url: str
    filename: str


class ManufacturingCommerceSchema(BaseModel):
    mpn: str
    alias_mpns: list[str] = Field(description="Other MPNs that this part is known by")
    manufacturer: str
    classifications: list[str]
    description: str
    hero_image: str
    series: str
    lifecycle_status: str
    country_of_origin: str
    aecq_status: str
    reach_status: str
    rohs_status: str
    export_control_class_number: str
    packaging: str
    power_rating: str
    voltage_rating: str
    mount_type: str
    moisture_sensitivity_level: str
    tolerance: str
    inductance: str
    capacitance: str
    resistance: str
    min_operating_temperature: str
    max_operating_temperature: str
    leadfree: str
    termination_type: str
    num_terminations: int
    specs: list[Specification]
    product_change_notification_documents: list[Document]
    reach_compliance_documents: list[Document]
    rohs_compliance_documents: list[Document]
    datasheets: list[Document]
    specsheets: list[Document]
    suggested_alternative_mpns: list[str]


class ForumSchema(BaseModel):
    auther: str
    title: str
    post_date: str
    content: str
    up_votes: int
    down_votes: int
    views: int
    num_comments: int


def get_fetch_schema(fetch_id: str) -> Type[BaseModel]:
    fetch_schemas: Dict[str, Type[BaseModel]] = {
        "contact": ContactSchema,
        "job_posting": JobPostingSchema,
        "manufacturing_commerce": ManufacturingCommerceSchema,
        "forum": ForumSchema,
    }

    if fetch_id not in fetch_schemas:
        raise ValueError(f"Invalid fetch_id: {fetch_id}")

    return fetch_schemas[fetch_id]
