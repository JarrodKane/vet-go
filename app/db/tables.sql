-- public.alembic_version definition

-- Drop table

-- DROP TABLE public.alembic_version;

CREATE TABLE public.alembic_version (
	version_num varchar(32) NOT NULL,
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);


-- public.animal definition

-- Drop table

-- DROP TABLE public.animal;


CREATE TABLE "public".animal
(
 "id"            uuid NOT NULL,
 identifier    varchar(254) NULL,
 name          varchar(254) NULL,
 age           integer NULL,
 sex           varchar(50) NULL,
 weight        varchar(128) NULL,
 height        varchar(128) NULL,
 type          varchar(128) NOT NULL,
 color         varchar(128) NULL,
 description   varchar(128) NULL,
 image         varchar(128) NULL,
 road          varchar(254) NULL,
 city          varchar(254) NULL,
 "state"         varchar(254) NULL,
 zip           varchar(254) NULL,
 country       varchar(254) NULL,
 date_of_birth date NOT NULL,
 CONSTRAINT animal_pkey PRIMARY KEY ( "id" )
);




-- public.user_model definition

-- Drop table

-- DROP TABLE public.user_model;

CREATE TABLE public.user_model (
	id uuid NOT NULL,
	email varchar(254) NOT NULL,
	hashed_password varchar(128) NOT NULL,
	"name" varchar(254) NULL,
	phone_number varchar(128) NULL,
	road varchar(254) NULL,
	city varchar(254) NULL,
	state varchar(254) NULL,
	zip varchar(254) NULL,
	country varchar(254) NULL,
	CONSTRAINT user_model_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_user_model_email ON public.user_model USING btree (email);


-- public.animal_user_association definition

-- Drop table

-- DROP TABLE public.animal_user_association;

CREATE TABLE public.animal_user_association (
	animal_id uuid NULL,
	user_id uuid NULL,
	CONSTRAINT animal_user_association_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animal(id),
	CONSTRAINT animal_user_association_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_model(id)
);



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



CREATE TABLE "public".clinic
(
 "id"             uuid NOT NULL,
 name           varchar(250) NOT NULL,
 email          varchar(250) NOT NULL,
 road           varchar(254) NOT NULL,
 city           varchar(254) NOT NULL,
 "state"          varchar(254) NOT NULL,
 zip            varchar(254) NOT NULL,
 country        varchar(254) NOT NULL,
 phone          varchar(20) NOT NULL,
 description    text NULL,
 website        varchar(250) NULL,
 specialisation text NULL,
 org_id         uuid NOT NULL

);

CREATE INDEX FK_1 ON "public".clinic
(
 org_id
);





CREATE TABLE "public".staffClinic
(
 "id"         NOT NULL,
 staff_id  uuid NOT NULL,
 clinic_id uuid NOT NULL,
 role      varchar(50) NOT NULL

);

CREATE INDEX FK_1 ON "public".staffClinic
(
 clinic_id
);

CREATE INDEX FK_2 ON "public".staffClinic
(
 staff_id
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
 specialisation  text NULL

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




















