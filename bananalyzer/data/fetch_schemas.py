from typing import Dict, List, Type

from pydantic import BaseModel, Field, HttpUrl

from bananalyzer.data.schemas import FetchId

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
    fax: str = Field(
        description="fax number of the location (only include the number but retain its formatting)",
    )
    type: str = Field(
        description="the type of location: Neurosurgery, MRI Services, etc. (not all locations will have a type available on the page)",
    )


class JobPostingSchema(BaseModel):
    job_id: str = Field(
        description="Unique alphanumeric identifier for the job posting."
    )
    job_title: str = Field(
        description="The entire job title, including team name or specialization if present in the title."
    )
    job_category: str = Field(
        description="Team name or specialization if present separate from the title."
    )
    date_posted: str = Field(description="Date posted, only if present on the page.")
    location: str = Field(description="Entire location of the job.")
    job_description: str = Field(
        description="Comprehensive job description including all its sentences."
    )
    roles_and_responsibilities: str
    qualifications: str
    preferred_qualifications: str
    benefits: str
    salary: str = Field(
        description="Numerical annual salary following format provided, including lower and upper bounds if present."
    )


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
    author: str = Field(description="Author of the main or original post")
    title: str = Field(description="Title of the original post")
    post_date: str
    content: str = Field(
        description="Entire content of the original post, including all sentences"
    )
    up_votes: int = Field(
        description="Number of likes, upvotes, etc on the original post"
    )
    down_votes: int
    views: int
    num_comments: int = Field(
        description="Number of comments or responses, not including the original post"
    )


class AttorneyExperience(BaseModel):
    title: str = Field(description="Title at the previous law firm")
    firm: str = Field(description="Name of the law firm")
    dates: str = Field(description="Duration of employment at the law firm")


class AttorneyBarAdmission(BaseModel):
    state: str = Field(description="State of bar admission")
    year: str = Field(description="Year of bar admission")
    country: str = Field(description="Country of bar admission", default="USA")


class AttorneyEducation(BaseModel):
    school: str = Field(description="Name of the educational institution")
    year: str = Field(description="Year of graduation")
    degree: str = Field(
        description="Type of degree obtained",
    )
    honors: str = Field(
        description="Honors received during education",
    )


class AttorneyAward(BaseModel):
    date: str = Field(description="Date or duration when the award was received")
    award: str = Field(description="Name of the award")
    url: HttpUrl = Field(
        description="URL link to the award recognition",
    )


class AttorneySchema(BaseModel):
    website: HttpUrl = Field(description="URL of the attorney's profile page")
    name: str = Field(description="Full name of the attorney")
    title: str = Field(
        description="Title of the attorney, such as Associate, Counsel, or Partner"
    )
    practice_areas_main: List[str] = Field(
        description="Primary practice areas of the attorney"
    )
    practice_areas_all: List[str] = Field(description="Complete list of practice areas")
    specialties: List[str] = Field(description="Specialized industry sectors")
    email: str = Field(description="Email address of the attorney")
    location: str = Field(description="Office location of the attorney")
    phone: str = Field(
        description="Direct phone number of the attorney",
    )
    bio: str = Field(description="Main bio description of the attorney")
    experience: List[AttorneyExperience] = Field(
        description="Past work history at other law firms"
    )
    matters: str = Field(description="List of past cases and work done by the attorney")
    bar_admissions: List[AttorneyBarAdmission] = Field(
        description="Bar admissions of the attorney"
    )
    law_school: List[AttorneyEducation] = Field(
        description="Law school information of the attorney"
    )
    other_schools: List[AttorneyEducation] = Field(
        description="Other education details of the attorney"
    )
    awards: List[AttorneyAward] = Field(
        description="Awards and recognitions received by the attorney"
    )
    pdf_url: HttpUrl = Field(
        description="Link to a PDF bio of the attorney",
    )
    photo_url: HttpUrl = Field(description="Link to the photo of the attorney")
    news: List[HttpUrl] = Field(
        description="Links to news articles involving the attorney", default=[]
    )


class AttorneyJobPostingSchema(BaseModel):
    website: HttpUrl = Field(
        description="URL of the job listing. May or may not be unique to this job."
    )
    tier: str = Field(
        description="Categorize into: Associate (general), Junior Associate, Mid-Level Associate, Senior Associate, Partner, Other (catch all if unsure)."
    )
    department: str = Field(
        description="Department, only if explicitly stated.",
    )
    title: str = Field(
        description="Job title. Remove location but keep everything else."
    )
    description: str = Field(description="Job description.")
    locations: List[str] = Field(
        description="Offices/cities/locations where this job is being offered."
    )
    salary_range: str = Field(
        description="Pay range specifically stated in the listing."
    )
    experience: str = Field(
        description="Required experience specifically stated in the listing."
    )
    full: str = Field(
        description="Complete information related to this job including HTML content for links."
    )


def get_fetch_schema(fetch_id: FetchId) -> Type[BaseModel]:
    fetch_schemas: Dict[str, Type[BaseModel]] = {
        "contact": ContactSchema,
        "job_posting": JobPostingSchema,
        "manufacturing_commerce": ManufacturingCommerceSchema,
        "forum": ForumSchema,
        "attorney": AttorneySchema,
        "attorney_job_listing": AttorneyJobPostingSchema,
    }

    if fetch_id not in fetch_schemas:
        raise ValueError(f"Invalid fetch_id: {fetch_id}")

    return fetch_schemas[fetch_id]
