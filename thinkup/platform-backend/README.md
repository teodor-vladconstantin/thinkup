# Changelog

All notable changes to this project will be documented in this file.

## [v2.0] ``31-3-2022``

### Added

- Entity Classes (Project, Material/s, Goal/s, File)
- *Description* field to User Class
- `DYNAMODB` CRUD Ops for multiple Entities (Project, Goal, Material)
- `S3` CRUD Ops for multiple Entities (Files, )
- `API` CRUD Ops for multiple Entities (User, Project, Goal, Material)
- JSONEncoders for Project, Goal, Material

## [v2.1] ``05-03-2026`` (Latest Hotfix)

### Fixed

- **Public Project Access**: Removed authentication requirement for `GET /projects/<id>` endpoint. This fixes the issue where public project pages were returning `401 Unauthorized` for non-logged-in users.
- **Security Improvements**: Added explicit ownership checks (`createdBy` or `adminList`) for `DELETE` and `PUT` operations on projects to prevent unauthorized modifications.
- **Logging**: Enhanced logging in `main.py` and `view_projects.py` for better debugging.

## v1.0  ``16-2-2022``

### First "official" Version

- Entity Classes (Student, Sponsor, Competitor, Mentor & Tech)
- Permissions Class
- Settings Class
- JSONEncoder Class (helps with JSON encoding the entities)
- DataBase connection
- CRUD Ops for DataBase
- API Requests (`GET`, `POST`, `PUT`, `DELETE`)

[v2.0]: https://github.com/ThinkUpAcademy/platform-backend/compare/v1.0...v2.0
