"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
import uuid

import enum
from sqlalchemy import String, ForeignKey, Boolean, Table, Column, Enum, Date, Float, DateTime, Text, Time, Integer,Interval, Numeric
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from enum import Enum as PyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# NEED THIS IN ORDER TO CREATE ENUMS WITHOUT ISSUE
# https://github.com/sqlalchemy/alembic/issues/278#issuecomment-1671727631
import alembic_postgresql_enum






class ActivityTypes(enum.Enum):
    check_up = "check-up"
    operation = "operation"
    sale = "sale"
    vaccination = "vaccination"
    dental = "dental"
    grooming = "grooming"
    emergency = "emergency"
    consultation = "consultation"
    imaging = "imaging"
    other = "other"
    phone = "phone"
    Bath = "Bath"
    Feces = "Feces"
    Injury = "Injury"
    Exercise = "Exercise"
    Food = "Food"
    Nails = "Nails"
    Wash = "Wash"
    Urine = "Urine"
    Vomit = "Vomit"
    Deworming = "Deworming"
    Water = "Water"
    Sleep = "Sleep"
    Seizure = "Seizure"
    Season = "Season"
    Medication = "Medication"



class AnimalType(enum.Enum):
    Dog = "Dog"
    Cat = "Cat"
    Horse = "Horse"
    Bird = "Bird"
    Rabbit = "Rabbit"
    Rodent = "Rodent"
    Reptile = "Reptile"
    Amphibian = "Amphibian"
    Fish = "Fish"
    Ferret = "Ferret"
    Guinea_Pig = "Guinea Pig"
    Hamster = "Hamster"
    Exotic_Mammal = "Exotic Mammal"
    Farm_Livestock = "Farm/Livestock"
    Other = "Other"


class SpecialisationType(enum.Enum):
    Canine_Medicine = "Canine Medicine"
    Feline_Medicine = "Feline Medicine"
    Equine_Medicine = "Equine Medicine"
    Avian_Medicine = "Avian Medicine"
    Exotic_Animal_Medicine = "Exotic Animal Medicine"
    Dental_Specialist = "Dental Specialist"
    Orthopedic_Surgeon = "Orthopedic Surgeon"
    Ophthalmologist = "Ophthalmologist"
    Dermatologist = "Dermatologist"
    Behavioral_Specialist = "Behavioral Specialist"
    Radiology = "Radiology"
    Nutritionist = "Nutritionist"
    Emergency_and_Critical_Care = "Emergency and Critical Care"
    Internal_Medicine = "Internal Medicine"
    Surgery = "Surgery"
    Anesthesiology = "Anesthesiology"
    Pathology = "Pathology"
    Rehabilitation_Therapist = "Rehabilitation Therapist"
    Public_Health = "Public Health"
    Zoological_Medicine = "Zoological Medicine"
    Other = "Other"

class RoleType(enum.Enum):
    Veterinarian = "Veterinarian"
    Veterinary_Technician = "Veterinary Technician"
    Receptionist = "Receptionist"
    Groomer = "Groomer"
    Animal_Care_Assistant = "Animal Care Assistant"
    Laboratory_Technician = "Laboratory Technician"
    Administrative_Staff = "Administrative Staff"
    Emergency_Response_Team = "Emergency Response Team"
    Specialist = "Specialist"
    Intern = "Intern"
    Other = "Other"



Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    created_at: Mapped[DateTime] = Column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted: Mapped[bool] = Column(Boolean, default=False)
    version: Mapped[int] = Column(Integer, default=0)


class AddressModel(BaseModel):
    __abstract__ = True
    road: Mapped[str] = mapped_column(String(254), nullable=True)
    city: Mapped[str] = mapped_column(String(254), nullable=True)
    state: Mapped[str] = mapped_column(String(254), nullable=True)
    zip: Mapped[str] = mapped_column(String(254), nullable=True)
    country: Mapped[str] = mapped_column(String(254), nullable=True)
    phone_number = mapped_column(String(20), nullable=False)


class UserModel(AddressModel):
    __abstract__ = True
    first_name: Mapped[str] = mapped_column(String(254), nullable=True)
    last_name: Mapped[str] = mapped_column(String(254), nullable=True)
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    mobile_number: Mapped[str] = mapped_column(String(20), nullable=True)
    hashed_password = mapped_column(String(128), nullable=False)
    active = mapped_column(Boolean, nullable=False, default=True)



# #  Many to many association table
# association_table = Table(
#     "animal_user_association",
#     Base.metadata,
#     Column("animal_id", ForeignKey("animal.id")),
#     Column("user_id", ForeignKey("user_model.id")),
# )

class AnimalUserAssociation(BaseModel):
    __tablename__ = "animal_user_association"

    animal_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('animal.id'), nullable=True)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('user_model.id'), nullable=True)




class User(UserModel):
    __tablename__ = "user_model"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    animals: Mapped[list] = relationship(
        "Animal",
        secondary=AnimalUserAssociation.__tablename__,
        back_populates="owners",
    )




# An animal might belong to multiple users
# An user might have multiple animals

class Animal(AddressModel):
    __tablename__ = "animal"

    identifier: Mapped[str] = mapped_column(String(254), nullable=True)
    name: Mapped[str] = mapped_column(String(254), nullable=True)
    sex: Mapped[str] = mapped_column(String(50), nullable=True)
    height: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)  # Adjust Numeric precision and scale
    animal_types = mapped_column(Enum(AnimalType), nullable=False)
    color: Mapped[str] = mapped_column(String(128), nullable=True)
    description: Mapped[str] = mapped_column(String(128), nullable=True)
    image: Mapped[str] = mapped_column(String(128), nullable=True)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    date_of_death: Mapped[Date] = mapped_column(Date, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    owners: Mapped[list] = relationship(
        "User",
        secondary=AnimalUserAssociation.__tablename__,
        back_populates="animals",
    )




class AnimalWeightHistory(BaseModel):
    __tablename__ = "animal_weight_history"


    weight: Mapped[float] = mapped_column(Float, nullable=False)
    change_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    animal_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('animal.id'), nullable=False)

class AnimalLog(BaseModel):
    __tablename__ = "animal_log"


    animal_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('animal.id'), nullable=False)
    appointment_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('appointment.id'), nullable=True)
    date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    activity: Mapped[str] = mapped_column(Enum(ActivityTypes), nullable=False)
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    procedures: Mapped[str] = mapped_column(Text, nullable=True)
    medication: Mapped[str] = mapped_column(Text, nullable=True)
    food_name: Mapped[str] = mapped_column(Text, nullable=True)
    medication_brand: Mapped[str] = mapped_column(Text, nullable=True)
    




class Appointment(BaseModel):
    __tablename__ = "appointment"


    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('user_model.id'), nullable=False)
    schedule_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('schedule.id'), nullable=False)
    appointment_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    activity_duration: Mapped[Interval] = mapped_column(Interval, nullable=False)


class Clinic(AddressModel):
    __tablename__ = "clinic"

    name = mapped_column(String(250), nullable=False)
    email = mapped_column(String(250), nullable=False)
    description = mapped_column(Text, nullable=True)
    website = mapped_column(String(250), nullable=True)
    specialisation = mapped_column(Enum(SpecialisationType, create_type=False), nullable=True)
    animal_types = mapped_column(Enum(AnimalType, create_type=False), nullable=False)
    organization_id = mapped_column(UUID(as_uuid=False), ForeignKey('organization.id'), nullable=False)

class Organization(AddressModel):
    __tablename__ = "organization"

    name = mapped_column(String(250), nullable=False)
    BSP = mapped_column(String(250), nullable=True)
    description = mapped_column(Text, nullable=True)
    website = mapped_column(String(250), nullable=True)
    email = mapped_column(String(250), nullable=True)


class Schedule(BaseModel):
    __tablename__ = "schedule"

    date = mapped_column(Date, nullable=False)
    opening_time = mapped_column(Time, nullable=False)
    closing_time = mapped_column(Time, nullable=False)
    staff_clinic_id = mapped_column(UUID(as_uuid=False), ForeignKey('staff_clinic.id'), nullable=False)


class Staff(UserModel):
    __tablename__ = "staff"

    description = mapped_column(Text, nullable=True)
    specialisation = mapped_column(Enum(SpecialisationType, create_type=False), nullable=True)

class StaffClinic(BaseModel):
    __tablename__ = "staff_clinic"

    staff_id = mapped_column(UUID(as_uuid=False), ForeignKey('staff.id'), nullable=False)
    clinic_id = mapped_column(UUID(as_uuid=False), ForeignKey('clinic.id'), nullable=False)
    role = mapped_column(Enum(RoleType, create_type=False), nullable=False)






