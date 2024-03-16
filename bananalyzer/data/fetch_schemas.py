from typing import Dict, Type, Union, Any

from pydantic import BaseModel, Field

from bananalyzer.data.schemas import FetchId

"""
This file contains mapping of fetch_id to fetch schema to avoid duplicate schemas in examples.json
"""

CONTACT_SCHEMA_GOAL = "Fetch the main hospital location contact information on the current page. There may be multiple location information or sub location information on the page. Only fetch the main location information which should be at the top of the page."


class ContactSchema(BaseModel):
    name: str = Field(
        description="Name of the location, facility, or the service provided by the clinic. Typically available at the top of the page or in the contact section. Do NOT use the address as the name which may be street/ state like 'Henry Adams, SF'. Double check that this is not the case"
    )
    address: str = Field(
        description="The COMPLETE address of the location using inner text of address elements. This value MUST be the combination of the building name or medical center name, street, city, state, and ZIP. EXAMPLE: `John Ivy Medical Center\n199 Test Street\nTest, CA 94103.` Concatenate multiple elements together as needed and retain formatting if possible. The building name may be placed above the other address elements. You MUST include the building name if it is available and presented this way. Do not forget ANY of the address elements. Filter out extra words at the begining like 'Address:' or extra words at the end like 'Phone', 'Fax', 'Directions', etc. Do not use value from additional locations.",
    )
    phone: str = Field(
        description="The primary phone number of the primary location. Ensure it is the phone number of the main location. This should be positioned higher than other phone numbers. Only include the number but retain its formatting. Strip all leading or traling words like 'Phone'. Do not phone value from related locations. Ensure the used phone value is positioned close to other contact fields.",
    )
    fax: str = Field(
        description="The primary FAX number of the location. Only include the number but retain its formatting by stripping all leading or traling words like 'Fax'. Ensure the fax number you select is LABELED as a FAX number on the page via text or an icon. If there is no number labeled as fax on the page, this value MUST be left as NULL. Never assume unlabeled numbers are the fax number. Do not use value from related locations.",
    )


GOVERNMENT_CONTRACT_GOAL = "Fetch the main government contract/notice/solicitation information on the current website."


class File(BaseModel):
    title: str
    url: str


class GovernmentContractSchema(BaseModel):
    id: str = Field(description="Unique identifier for the contract")
    title: str = Field(description="Title or name of the contract")
    description: str = Field(
        description="Description or synopsis field. Combine the solicitation summary and additional instructions section / process.",
    )
    location: str = Field(
        description="Location of the issuer. May be a combination of city and state",
    )
    type: str = Field(
        description="Type of contract. May be placed under `Solicitation Type`, `Opportunity Type`, `Market Type`, etc. Not a 'status' field",
    )
    category: str = Field(description="Category the contract falls under if given")

    posted_date: str = Field(
        description="Date the contract was made available for bidding. NOT the 'effective', 'start', or 'award' date.",
    )
    due_date: str = Field(
        description="Date the contract closes for bidding. NOT the end term date.",
    )

    buyer_name: str = Field(
        description="Name of the company, organization, or agency that issued the contract. NOT a person's name."
    )
    buyer_contact_name: str = Field(
        description="Name of the specific individual that is leading the contract, if available"
    )
    buyer_contact_number: str = Field(description="Contact number of the issuer")
    buyer_contact_email: str = Field(description="Contact email of the issuer")

    attachments: list[File] = Field(
        default_factory=list,
        description="A list of all of the files/documents attached to the contract (e.g. hyperlinks to PDF's)",
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
    "job_benefits": {
        "type": "string",
        "description": "A list of benefits provided with the job.",
    },
    "qualifications": {
        "type": "string",
        "description": "A list of required qualifications or certifications for the job.",
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
    practice_areas_main: list[str] = Field(
        description="Primary practice areas of the attorney"
    )
    practice_areas_all: list[str] = Field(description="Complete list of practice areas")
    specialties: list[str] = Field(description="Specialized industry sectors")
    email: str = Field(description="Email address of the attorney")
    location: str = Field(description="Office location of the attorney")
    phone: str = Field(
        description="Direct phone number of the attorney",
    )
    bio: str = Field(description="Main bio description of the attorney")
    experience: list[AttorneyExperience] = Field(
        description="Past work history at other law firms"
    )
    matters: str = Field(description="List of past cases and work done by the attorney")
    bar_admissions: list[AttorneyBarAdmission] = Field(
        description="Bar admissions of the attorney"
    )
    law_school: list[AttorneyEducation] = Field(
        description="Law school information of the attorney"
    )
    other_schools: list[AttorneyEducation] = Field(
        description="Other education details of the attorney"
    )
    awards: list[AttorneyAward] = Field(
        description="Awards and recognitions received by the attorney"
    )
    pdf_url: str = Field(
        description="Link to a PDF bio of the attorney",
    )
    photo_url: str = Field(description="Link to the photo of the attorney")
    news: list[str] = Field(
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
    locations: list[str] = Field(
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
        "contract": GovernmentContractSchema,
        "manufacturing_commerce": ManufacturingCommerceSchema,
        "forum": ForumSchema,
        "attorney": AttorneySchema,
        "attorney_job_listing": AttorneyJobPostingSchema,
    }

    if fetch_id not in fetch_schemas:
        raise ValueError(f"Invalid fetch_id: {fetch_id}")

    return fetch_schemas[fetch_id]
