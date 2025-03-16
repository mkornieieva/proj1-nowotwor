/*
Created: 09.03.2025
Modified: 10.03.2025
Project: Rozpoznawanie nowotworów
Model: Nowotwór
Author: Grupa projektowa
Database: Oracle 19c
*/


-- Create tables section -------------------------------------------------

-- Table data

CREATE TABLE "data"(
  "id" Integer NOT NULL,
  "filename" Varchar2(225 ),
  "image_data" Blob NOT NULL,
  "annotation_xml" Varchar2(255 ) NOT NULL,
  "status" Varchar2(30 )
        CHECK ("status" IN ('pending', 'processed')),
  "uploaded_at" Timestamp(6)
)
/

-- Add keys for table data

ALTER TABLE "data" ADD CONSTRAINT "PK_data" PRIMARY KEY ("id")
/


-- Table ProcessedImages

CREATE TABLE "ProcessedImages"(
  "proc_image_id" Integer NOT NULL,
  "filename" Varchar2(225 ),
  "image_data" Blob NOT NULL,
  "processing_date" Timestamp(6),
  "id" Integer NOT NULL
)
/

-- Add keys for table ProcessedImages

ALTER TABLE "ProcessedImages" ADD CONSTRAINT "PK_ProcessedImages" PRIMARY KEY ("id","proc_image_id")
/

-- Table ProcessedAnnotations

CREATE TABLE "ProcessedAnnotations"(
  "id_proc_annotat" Integer NOT NULL,
  "x_min" Integer NOT NULL,
  "x_max" Integer NOT NULL,
  "y_min" Integer NOT NULL,
  "y_max" Integer NOT NULL,
  "created_at" Timestamp(6),
  "id" Integer NOT NULL
)
/

-- Add keys for table ProcessedAnnotations

ALTER TABLE "ProcessedAnnotations" ADD CONSTRAINT "PK_ProcessedAnnotations" PRIMARY KEY ("id_proc_annotat","id")
/

-- Table AnalysisResult

CREATE TABLE "AnalysisResult"(
  "analysis_id" Integer NOT NULL,
  "x_min" Integer NOT NULL,
  "x_max" Integer NOT NULL,
  "y_min" Integer NOT NULL,
  "y_max" Integer NOT NULL,
  "confidence" Float(126),
  "id" Integer NOT NULL,
  "proc_image_id" Integer NOT NULL
)
/

-- Add keys for table AnalysisResult

ALTER TABLE "AnalysisResult" ADD CONSTRAINT "PK_AnalysisResult" PRIMARY KEY ("id","proc_image_id","analysis_id")
/


-- Create foreign keys (relationships) section -------------------------------------------------

ALTER TABLE "ProcessedImages" ADD CONSTRAINT "Obraz_jest_przetwarzany" FOREIGN KEY ("id") REFERENCES "data" ("id")
/




ALTER TABLE "ProcessedAnnotations" ADD CONSTRAINT "Przetwarzanie_XML" FOREIGN KEY ("id") REFERENCES "data" ("id")
/



ALTER TABLE "AnalysisResult" ADD CONSTRAINT "Analiza_stworzona_przez_model" FOREIGN KEY ("id", "proc_image_id") REFERENCES "ProcessedImages" ("id", "proc_image_id")
/