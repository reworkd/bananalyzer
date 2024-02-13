from typing import Dict, List, Type, Union, Any

from pydantic import BaseModel, Field

from bananalyzer.data.schemas import FetchId

"""
This file contains mapping of fetch_id to fetch schema to avoid duplicate schemas in examples.json
"""


class ContactSchema(BaseModel):
    name: str = Field(
        description="Name of the location, facility, or the service provided by the clinic. Typically available at the top of the page or in the contac section. Do NOT use the address as the name which may be street/ state like 'Henry Adams, SF'. Double check that this is not the case"
    )
    address: str = Field(
        description="The complete address of the location. Use the inner text of elements. You MUST include the building name if available and above the other address elements. This value should be building name or medical center name, street, city, state, and ZIP. EXAMPLE: `John Ivy Medical Center\n199 Test Street\nTest, CA 94103.` Concatenate multiple elements together as needed and retain formatting if possible. Do NOT forget the building name. Do not include extra words at the begining or end of the concatenation like 'Address' or 'Phone', etc",
    )
    phone: str = Field(
        description="The primary phone number of the location. Ensure it is the phone number of the main location. This should be positioned higher than other phone numbers. Only include the number but retain its formatting. Strip all leading or traling words like 'Phone'",
    )
    fax: str = Field(
        description="The primary fax number of the location. Only include the number but retain its formatting by stripping all leading or traling words like 'Fax'. When picking an element, ensure the element you use is LABELED as a FAX number on the page via text or an icon. If this is not the case, this value MUST be left as NULL. Never assume unlabeled numbers are the fax number.",
    )


JobPostingSchema = {
    "job_id": {
        "type": "string",
        "description": "Unique alphanumeric identifier for the job posting.",
    },
    "company_name": {
        "type": "string",
        "description": "Name of the company offering the job.",
    },
    "company_description": {
        "type": "string",
        "description": "A brief description of the company within the job post.",
    },
    "level": {
        "type": "string",
        "description": "The tier of the job within the company's structure.",
    },
    "department": {
        "type": "string",
        "description": "The department or team name within the company for the job position.",
    },
    "job_title": {
        "type": "string",
        "description": "The entire job title, including team name or specialization if present in the title.",
    },
    "job_description": {
        "type": "string",
        "description": "Comprehensive job description including all its sentences.",
    },
    "location": {"type": "string", "description": "Entire location of the job."},
    "salary_range": {
        "type": "object",
        "properties": {
            "min": {"type": "string", "description": "Minimum salary offered."},
            "max": {"type": "string", "description": "Maximum salary offered."},
            "currency": {
                "type": "string",
                "description": "The currency of the salary.",
            },
        },
    },
    "date_posted": {
        "type": "string",
        "description": "Date posted, only if present on the page.",
    },
    "apply_url": {
        "type": "string",
        "description": "The URL where applicants can apply for the job.",
    },
    "work_hours": {
        "type": "string",
        "description": "The expected work hours for the job.",
    },
    "job_benefits": {
        "type": "string",
        "description": "A list of benefits provided with the job.",
    },
    "qualifications": {
        "type": "string",
        "description": "A list of required qualifications for the job.",
    },
    "preferred_qualifications": {
        "type": "string",
        "description": "A list of preferred (but not mandatory) qualifications for the job.",
    },
    "role": {
        "type": "string",
        "description": "Details about the role including responsibilities and required skills.",
    },
    "skills": {
        "type": "string",
        "description": "A list of knowledge, skills or abilities required for the job.",
    },
    "education": {
        "type": "string",
        "description": "Listed requirements for education or past experience",
    },
    "recruiter_email": {
        "type": "string",
        "description": "Email address of the recruiter or hiring manager for contact.",
    },
    "application_deadline": {
        "type": "string",
        "description": "The deadline for submitting job applications.",
    },
    "employment_type": {
        "type": "string",
        "description": "The type of employment (e.g., full-time, part-time, contract).",
    },
    "tags": {
        "type": "array",
        "description": "Keywords or phrases related to the job for categorization and searchability.",
    },
}


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
    url: str = Field(
        description="URL link to the award recognition",
    )


class AttorneySchema(BaseModel):
    website: str = Field(description="URL of the attorney's profile page")
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
    pdf_url: str = Field(
        description="Link to a PDF bio of the attorney",
    )
    photo_url: str = Field(description="Link to the photo of the attorney")
    news: List[str] = Field(
        description="Links to news articles involving the attorney", default=[]
    )


class AttorneyJobPostingSchema(BaseModel):
    website: str = Field(
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


def get_fetch_schema(fetch_id: FetchId) -> Union[Dict[str, Any], Type[BaseModel]]:
    fetch_schemas: Dict[str, Union[Dict[str, Any], Type[BaseModel]]] = {
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
