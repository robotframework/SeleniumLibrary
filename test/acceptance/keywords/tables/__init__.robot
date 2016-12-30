*** Settings ***
Resource        table_resource.robot
Suite Setup     Go To Page "tables/tables.html"
Force Tags      Known Issue Internet Explorer
