"""create_pet_modelbrands

Revision ID: 84caa38f4010
Revises: 
Create Date: 2024-01-23 18:42:21.211098

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "84caa38f4010"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum(
        "check_up",
        "operation",
        "sale",
        "vaccination",
        "dental",
        "grooming",
        "emergency",
        "consultation",
        "imaging",
        "other",
        "phone",
        "Bath",
        "Feces",
        "Injury",
        "Exercise",
        "Food",
        "Nails",
        "Wash",
        "Urine",
        "Vomit",
        "Deworming",
        "Water",
        "Sleep",
        "Seizure",
        "Season",
        "Medication",
        name="activitytypes",
    ).create(op.get_bind())
    sa.Enum(
        "Dog",
        "Cat",
        "Horse",
        "Bird",
        "Rabbit",
        "Rodent",
        "Reptile",
        "Amphibian",
        "Fish",
        "Ferret",
        "Guinea_Pig",
        "Hamster",
        "Exotic_Mammal",
        "Farm_Livestock",
        "Other",
        name="animaltype",
    ).create(op.get_bind())
    op.create_table(
        "animal",
        sa.Column("identifier", sa.String(length=254), nullable=True),
        sa.Column("name", sa.String(length=254), nullable=True),
        sa.Column("sex", sa.String(length=50), nullable=True),
        sa.Column("height", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column(
            "animal_types",
            postgresql.ENUM(
                "Dog",
                "Cat",
                "Horse",
                "Bird",
                "Rabbit",
                "Rodent",
                "Reptile",
                "Amphibian",
                "Fish",
                "Ferret",
                "Guinea_Pig",
                "Hamster",
                "Exotic_Mammal",
                "Farm_Livestock",
                "Other",
                name="animaltype",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("color", sa.String(length=128), nullable=True),
        sa.Column("description", sa.String(length=128), nullable=True),
        sa.Column("image", sa.String(length=128), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("date_of_death", sa.Date(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("road", sa.String(length=254), nullable=True),
        sa.Column("city", sa.String(length=254), nullable=True),
        sa.Column("state", sa.String(length=254), nullable=True),
        sa.Column("zip", sa.String(length=254), nullable=True),
        sa.Column("country", sa.String(length=254), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "organization",
        sa.Column("name", sa.String(length=250), nullable=False),
        sa.Column("BSP", sa.String(length=250), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("website", sa.String(length=250), nullable=True),
        sa.Column("email", sa.String(length=250), nullable=True),
        sa.Column("road", sa.String(length=254), nullable=True),
        sa.Column("city", sa.String(length=254), nullable=True),
        sa.Column("state", sa.String(length=254), nullable=True),
        sa.Column("zip", sa.String(length=254), nullable=True),
        sa.Column("country", sa.String(length=254), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "staff",
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "specialisation",
            postgresql.ENUM(name="specialisationtype", create_type=False),
            nullable=True,
        ),
        sa.Column("first_name", sa.String(length=254), nullable=True),
        sa.Column("last_name", sa.String(length=254), nullable=True),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("mobile_number", sa.String(length=20), nullable=True),
        sa.Column("hashed_password", sa.String(length=128), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("road", sa.String(length=254), nullable=True),
        sa.Column("city", sa.String(length=254), nullable=True),
        sa.Column("state", sa.String(length=254), nullable=True),
        sa.Column("zip", sa.String(length=254), nullable=True),
        sa.Column("country", sa.String(length=254), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_staff_email"), "staff", ["email"], unique=True)
    op.create_table(
        "user_model",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("first_name", sa.String(length=254), nullable=True),
        sa.Column("last_name", sa.String(length=254), nullable=True),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("mobile_number", sa.String(length=20), nullable=True),
        sa.Column("hashed_password", sa.String(length=128), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("road", sa.String(length=254), nullable=True),
        sa.Column("city", sa.String(length=254), nullable=True),
        sa.Column("state", sa.String(length=254), nullable=True),
        sa.Column("zip", sa.String(length=254), nullable=True),
        sa.Column("country", sa.String(length=254), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_model_email"), "user_model", ["email"], unique=True)
    op.create_table(
        "animal_user_association",
        sa.Column("animal_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column("user_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["animal_id"],
            ["animal.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user_model.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "animal_weight_history",
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("change_date", sa.DateTime(), nullable=False),
        sa.Column("animal_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["animal_id"],
            ["animal.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "clinic",
        sa.Column("name", sa.String(length=250), nullable=False),
        sa.Column("email", sa.String(length=250), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("website", sa.String(length=250), nullable=True),
        sa.Column(
            "specialisation",
            postgresql.ENUM(
                "Canine_Medicine",
                "Feline_Medicine",
                "Equine_Medicine",
                "Avian_Medicine",
                "Exotic_Animal_Medicine",
                "Dental_Specialist",
                "Orthopedic_Surgeon",
                "Ophthalmologist",
                "Dermatologist",
                "Behavioral_Specialist",
                "Radiology",
                "Nutritionist",
                "Emergency_and_Critical_Care",
                "Internal_Medicine",
                "Surgery",
                "Anesthesiology",
                "Pathology",
                "Rehabilitation_Therapist",
                "Public_Health",
                "Zoological_Medicine",
                "Other",
                name="specialisationtype",
                create_type=False,
            ),
            nullable=True,
        ),
        sa.Column(
            "animal_types",
            postgresql.ENUM(
                "Dog",
                "Cat",
                "Horse",
                "Bird",
                "Rabbit",
                "Rodent",
                "Reptile",
                "Amphibian",
                "Fish",
                "Ferret",
                "Guinea_Pig",
                "Hamster",
                "Exotic_Mammal",
                "Farm_Livestock",
                "Other",
                name="animaltype",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("organization_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("road", sa.String(length=254), nullable=True),
        sa.Column("city", sa.String(length=254), nullable=True),
        sa.Column("state", sa.String(length=254), nullable=True),
        sa.Column("zip", sa.String(length=254), nullable=True),
        sa.Column("country", sa.String(length=254), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "staff_clinic",
        sa.Column("staff_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("clinic_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column(
            "role",
            postgresql.ENUM(
                "Veterinarian",
                "Veterinary_Technician",
                "Receptionist",
                "Groomer",
                "Animal_Care_Assistant",
                "Laboratory_Technician",
                "Administrative_Staff",
                "Emergency_Response_Team",
                "Specialist",
                "Intern",
                "Other",
                name="roletype",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["clinic_id"],
            ["clinic.id"],
        ),
        sa.ForeignKeyConstraint(
            ["staff_id"],
            ["staff.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "schedule",
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("opening_time", sa.Time(), nullable=False),
        sa.Column("closing_time", sa.Time(), nullable=False),
        sa.Column("staff_clinic_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["staff_clinic_id"],
            ["staff_clinic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "appointment",
        sa.Column("user_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("schedule_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("appointment_time", sa.DateTime(), nullable=False),
        sa.Column("activity_duration", sa.Interval(), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedule.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user_model.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "animal_log",
        sa.Column("animal_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("appointment_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column(
            "activity",
            postgresql.ENUM(
                "check_up",
                "operation",
                "sale",
                "vaccination",
                "dental",
                "grooming",
                "emergency",
                "consultation",
                "imaging",
                "other",
                "phone",
                "Bath",
                "Feces",
                "Injury",
                "Exercise",
                "Food",
                "Nails",
                "Wash",
                "Urine",
                "Vomit",
                "Deworming",
                "Water",
                "Sleep",
                "Seizure",
                "Season",
                "Medication",
                name="activitytypes",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("procedures", sa.Text(), nullable=True),
        sa.Column("medication", sa.Text(), nullable=True),
        sa.Column("food_name", sa.Text(), nullable=True),
        sa.Column("medication_brand", sa.Text(), nullable=True),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["animal_id"],
            ["animal.id"],
        ),
        sa.ForeignKeyConstraint(
            ["appointment_id"],
            ["appointment.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    sa.Enum(
        "Dog",
        "Cat",
        "Horse",
        "Bird",
        "Rabbit",
        "Rodent",
        "Reptile",
        "Amphibian",
        "Fish",
        "Ferret",
        "Guinea Pig",
        "Hamster",
        "Exotic Mammal",
        "Farm/Livestock",
        "Other",
        name="animal_types",
    ).drop(op.get_bind())
    sa.Enum(
        "check-up",
        "operation",
        "sale",
        "vaccination",
        "dental",
        "grooming",
        "emergency",
        "consultation",
        "imaging",
        "other",
        "phone",
        "Bath",
        "Feces",
        "Injury",
        "Exercise",
        "Food",
        "Nails",
        "Wash",
        "Urine",
        "Vomit",
        "Deworming",
        "Water",
        "Sleep",
        "Seizure",
        "Season",
        "Medication",
        name="activitytype",
    ).drop(op.get_bind())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum(
        "check-up",
        "operation",
        "sale",
        "vaccination",
        "dental",
        "grooming",
        "emergency",
        "consultation",
        "imaging",
        "other",
        "phone",
        "Bath",
        "Feces",
        "Injury",
        "Exercise",
        "Food",
        "Nails",
        "Wash",
        "Urine",
        "Vomit",
        "Deworming",
        "Water",
        "Sleep",
        "Seizure",
        "Season",
        "Medication",
        name="activitytype",
    ).create(op.get_bind())
    sa.Enum(
        "Dog",
        "Cat",
        "Horse",
        "Bird",
        "Rabbit",
        "Rodent",
        "Reptile",
        "Amphibian",
        "Fish",
        "Ferret",
        "Guinea Pig",
        "Hamster",
        "Exotic Mammal",
        "Farm/Livestock",
        "Other",
        name="animal_types",
    ).create(op.get_bind())
    op.drop_table("animal_log")
    op.drop_table("appointment")
    op.drop_table("schedule")
    op.drop_table("staff_clinic")
    op.drop_table("clinic")
    op.drop_table("animal_weight_history")
    op.drop_table("animal_user_association")
    op.drop_index(op.f("ix_user_model_email"), table_name="user_model")
    op.drop_table("user_model")
    op.drop_index(op.f("ix_staff_email"), table_name="staff")
    op.drop_table("staff")
    op.drop_table("organization")
    op.drop_table("animal")
    sa.Enum(
        "Dog",
        "Cat",
        "Horse",
        "Bird",
        "Rabbit",
        "Rodent",
        "Reptile",
        "Amphibian",
        "Fish",
        "Ferret",
        "Guinea_Pig",
        "Hamster",
        "Exotic_Mammal",
        "Farm_Livestock",
        "Other",
        name="animaltype",
    ).drop(op.get_bind())
    sa.Enum(
        "check_up",
        "operation",
        "sale",
        "vaccination",
        "dental",
        "grooming",
        "emergency",
        "consultation",
        "imaging",
        "other",
        "phone",
        "Bath",
        "Feces",
        "Injury",
        "Exercise",
        "Food",
        "Nails",
        "Wash",
        "Urine",
        "Vomit",
        "Deworming",
        "Water",
        "Sleep",
        "Seizure",
        "Season",
        "Medication",
        name="activitytypes",
    ).drop(op.get_bind())
    # ### end Alembic commands ###