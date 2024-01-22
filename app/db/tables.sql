
-- ************************************** "public".alembic_version

CREATE TABLE "public".alembic_version
(
 version_num varchar(32) NOT NULL,
 CONSTRAINT alembic_version_pkc PRIMARY KEY ( version_num )
);


-- ************************************** "public".animal

CREATE TABLE "public".animal
(
 "id"            uuid NOT NULL,
 identifier    varchar(254) NULL,
 name          varchar(254) NULL,
 sex           varchar(50) NULL,
 height        float NULL,
 type          animal_type NOT NULL,
 color         varchar(128) NULL,
 description   varchar(128) NULL,
 image         varchar(128) NULL,
 road          varchar(254) NULL,
 city          varchar(254) NULL,
 "state"         varchar(254) NULL,
 zip           varchar(254) NULL,
 country       varchar(254) NULL,
 date_of_birth date NOT NULL,
 date_of_death date NULL,
 active        boolean NOT NULL DEFAULT true,
 CONSTRAINT animal_pkey PRIMARY KEY ( "id" )
);



COMMENT ON COLUMN "public".animal.type IS 'Dog,
    Cat,
    Horse,
    Bird,
    Rabbit,
    Rodent,
    Reptile,
    Amphibian,
    Fish,
    Ferret,
    Guinea Pig,
    Hamster,
    Exotic Mammal,
    Farm/Livestock,
    Other';
COMMENT ON COLUMN "public".animal.active IS 'This should default to true';



-- ************************************** animal_weight_history

CREATE TABLE animal_weight_history
(
 "id"          uuid NOT NULL,
 weight      float NOT NULL,
 change_date timestamp NOT NULL,
 animal_id   uuid NOT NULL

);

CREATE INDEX FK_1 ON animal_weight_history
(
 animal_id
);


-- ************************************** animal_log

CREATE TABLE animal_log
(
 "id"               uuid NOT NULL,
 animal_id        uuid NOT NULL,
 appointment_id   uuid NULL,
 "date"             timestamp NOT NULL,
 activty          activity_types NOT NULL,
 comments         text NULL,
 procedures       text NULL,
 medication       text NULL,
 food_name        text NULL,
 medication_brand text NULL

);

CREATE INDEX FK_1 ON animal_log
(
 animal_id
);

CREATE INDEX FK_2 ON animal_log
(
 appointment_id
);



COMMENT ON COLUMN animal_log.activty IS 'This could be multiple activities.
Someone might just come in to buy food for their dog, or someone might be buying food after an appointment. Or someone might just have had an appointment


There might also be operations

check-up, operation, sale,  vaccination, dental, grooming, emergency, consultation, imaging, other, phone, Bath, Feces, Injury, Exercise, Food, Nails, Wash, Urine, Vomit, Deworming, Water, Sleep, Seizure, Season, Medication';
COMMENT ON COLUMN animal_log.medication IS 'Text area that holds what medication was perscribed for the animal';
COMMENT ON COLUMN animal_log.food_name IS 'They could get multiple foods at one time';
COMMENT ON COLUMN animal_log.medication_brand IS 'This can be a list of medication brands since there could be multiple medications perscribed';

-- ************************************** "public".animal_user_association

CREATE TABLE "public".animal_user_association
(
 animal_id uuid NULL,
 user_id   uuid NULL,
 CONSTRAINT animal_user_association_animal_id_fkey FOREIGN KEY ( animal_id ) REFERENCES "public".animal ( "id" ),
 CONSTRAINT animal_user_association_user_id_fkey FOREIGN KEY ( user_id ) REFERENCES "public".user_model ( "id" )
);



-- ************************************** "public".appointment

CREATE TABLE "public".appointment
(
 "id"                uuid NOT NULL,
 user_id           uuid NOT NULL,
 schedule_id       uuid NOT NULL,
 appointment_time  timestamp NOT NULL,
 activity_duration interval minute NOT NULL

);

CREATE INDEX FK_1 ON "public".appointment
(
 user_id
);

CREATE INDEX FK_2 ON "public".appointment
(
 schedule_id
);

-- ************************************** "public".clinic

CREATE TABLE "public".clinic
(
 "id"              uuid NOT NULL,
 name            varchar(250) NOT NULL,
 email           varchar(250) NOT NULL,
 road            varchar(254) NOT NULL,
 city            varchar(254) NOT NULL,
 "state"           varchar(254) NOT NULL,
 zip             varchar(254) NOT NULL,
 country         varchar(254) NOT NULL,
 phone           varchar(20) NOT NULL,
 description     text NULL,
 website         varchar(250) NULL,
 specialisation  specialisation_type NULL,
 animal_types    animal_type NOT NULL,
 organization_id uuid NOT NULL

);

CREATE INDEX FK_1 ON "public".clinic
(
 organization_id
);



COMMENT ON COLUMN "public".clinic.specialisation IS 'Will be a list of these enums  

Canine Medicine,
    Feline Medicine,
    Equine Medicine,
    Avian Medicine,
    Exotic Animal Medicine,
    Dental Specialist,
    Orthopedic Surgeon,
    Ophthalmologist,
    Dermatologist,
    Behavioral Specialist,
    Radiology,
    Nutritionist,
    Emergency and Critical Care,
    Internal Medicine,
    Surgery,
    Anesthesiology,
    Pathology,
    Rehabilitation Therapist,
    Public Health,
    Zoological Medicine,
    Other';
COMMENT ON COLUMN "public".clinic.animal_types IS 'Will be a list of these animals
 Dog,
    Cat,
    Horse,
    Bird,
    Rabbit,
    Rodent,
    Reptile,
    Amphibian,
    Fish,
    Ferret,
    Guinea Pig,
    Hamster,
    Exotic Mammal,
    Farm/Livestock,
    Other';


-- ************************************** "public".Organization

CREATE TABLE "public".Organization
(
 "id"              uuid NOT NULL,
 name            varchar(250) NOT NULL,
 hashed_password varchar(128) NOT NULL,
 road            varchar(254) NOT NULL,
 city            varchar(254) NOT NULL,
 "state"           varchar(254) NOT NULL,
 zip             varchar(254) NOT NULL,
 country         varchar(254) NOT NULL,
 BSP             varchar(250) NULL,
 phone_number    varchar(20) NOT NULL,
 description     text NULL,
 website         varchar(250) NULL,
 email           varchar(250) NULL

);

-- ************************************** "public".schedule

CREATE TABLE "public".schedule
(
 "id"              uuid NOT NULL,
 "date"            date NOT NULL,
 opening_time    time NOT NULL,
 closing_time    time NOT NULL,
 staff_clinic_id  NOT NULL

);

CREATE INDEX FK_1 ON "public".schedule
(
 staff_clinic_id
);


-- ************************************** "public".staff

CREATE TABLE "public".staff
(
 "id"              uuid NOT NULL,
 name            varchar(254) NOT NULL,
 hashed_password varchar(128) NOT NULL,
 description     text NULL,
 email           varchar(250) NOT NULL,
 phone_number    varchar(128) NULL,
 specialisation  specialisation_type NULL

);



COMMENT ON COLUMN "public".staff.specialisation IS 'Will be a list of these enums   
 Canine Medicine,
    Feline Medicine,
    Equine Medicine,
    Avian Medicine,
    Exotic Animal Medicine,
    Dental Specialist,
    Orthopedic Surgeon,
    Ophthalmologist,
    Dermatologist,
    Behavioral Specialist,
    Radiology,
    Nutritionist,
    Emergency and Critical Care,
    Internal Medicine,
    Surgery,
    Anesthesiology,
    Pathology,
    Rehabilitation Therapist,
    Public Health,
    Zoological Medicine,
    Other';


-- ************************************** "public".staffClinic

CREATE TABLE "public".staffClinic
(
 "id"         NOT NULL,
 staff_id  uuid NOT NULL,
 clinic_id uuid NOT NULL,
 role      role_type NOT NULL

);

CREATE INDEX FK_1 ON "public".staffClinic
(
 clinic_id
);

CREATE INDEX FK_2 ON "public".staffClinic
(
 staff_id
);



COMMENT ON COLUMN "public".staffClinic.role IS 'Veterinarian,
    Veterinary Technician,
    Receptionist,
    Groomer,
    Animal Care Assistant,
    Laboratory Technician,
    Administrative Staff,
    Emergency Response Team,
    Specialist,
    Intern,
    Other';

-- ************************************** "public".user_model

CREATE TABLE "public".user_model
(
 "id"              uuid NOT NULL,
 name            varchar(254) NULL,
 email           varchar(254) NOT NULL,
 hashed_password varchar(128) NOT NULL,
 phone_number    varchar(128) NULL,
 road            varchar(254) NULL,
 city            varchar(254) NULL,
 "state"           varchar(254) NULL,
 zip             varchar(254) NULL,
 country         varchar(254) NULL,
 active          boolean NOT NULL,
 CONSTRAINT user_model_pkey PRIMARY KEY ( "id" )
);

CREATE UNIQUE INDEX ix_user_model_email ON "public".user_model USING btree
(
 email
);



COMMENT ON COLUMN "public".user_model.active IS 'default this to true when created';







