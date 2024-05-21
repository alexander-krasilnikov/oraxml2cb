--------------------------------------------------------
--  File created - Saturday-May-18-2024   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Table DATAPOINT_ARCHIVE
--------------------------------------------------------

  CREATE TABLE "ADMIN"."DATAPOINT_ARCHIVE" 
   (	"UUID" NUMBER(9,0), 
	"DP_ID" VARCHAR2(20 BYTE), 
	"DP_TIMESTAMP" VARCHAR2(30 BYTE), 
	"DP_DATA" "SYS"."XMLTYPE" , 
	"ARCHIVE_DATE" DATE DEFAULT sysdate
   ) ;
--------------------------------------------------------
--  DDL for Index DATAPOINT_ARCHIVE_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "ADMIN"."DATAPOINT_ARCHIVE_PK" ON "ADMIN"."DATAPOINT_ARCHIVE" ("UUID") 
  ;
--------------------------------------------------------
--  DDL for Trigger DATAPOINT_ARCHIVE_TRG
--------------------------------------------------------

  CREATE OR REPLACE EDITIONABLE TRIGGER "ADMIN"."DATAPOINT_ARCHIVE_TRG" 
BEFORE INSERT ON DATAPOINT_ARCHIVE
FOR EACH ROW 
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF INSERTING AND :NEW.UUID IS NULL THEN
      SELECT DATAPOINT_ARCHIVE_SEQ.NEXTVAL INTO :NEW.UUID FROM SYS.DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
/
ALTER TRIGGER "ADMIN"."DATAPOINT_ARCHIVE_TRG" ENABLE;
--------------------------------------------------------
--  Constraints for Table DATAPOINT_ARCHIVE
--------------------------------------------------------

  ALTER TABLE "ADMIN"."DATAPOINT_ARCHIVE" MODIFY ("UUID" NOT NULL ENABLE);
  ALTER TABLE "ADMIN"."DATAPOINT_ARCHIVE" MODIFY ("DP_ID" NOT NULL ENABLE);
  ALTER TABLE "ADMIN"."DATAPOINT_ARCHIVE" MODIFY ("DP_TIMESTAMP" NOT NULL ENABLE);
  ALTER TABLE "ADMIN"."DATAPOINT_ARCHIVE" MODIFY ("ARCHIVE_DATE" NOT NULL ENABLE);
  ALTER TABLE "ADMIN"."DATAPOINT_ARCHIVE" MODIFY ("DP_DATA" NOT NULL ENABLE);
  ALTER TABLE "ADMIN"."DATAPOINT_ARCHIVE" ADD CONSTRAINT "DATAPOINT_ARCHIVE_PK" PRIMARY KEY ("UUID")
  USING INDEX  ENABLE;
